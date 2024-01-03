import pygame
import numpy as np 
from pygame import Vector2
# --------------------------PLAYER-----------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self, name, x, y, config,radius = 40, color = "red", server = False):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.config = config
        # width and height
        self.radius = radius
        self.x, self.y = x, y
        self.coord_initial = Vector2(x, y)
        self.hook_coords = Vector2(x, y)
        self.hook_initial = Vector2(x, y)
        self.coords_current = Vector2(x, y)
        self.dash_started = Vector2(x, y)
        self.dash_coords = Vector2(x, y)
        self.dash_destination = Vector2(x, y)
        self.hook_cooldown_started = 0
        self.hook_on_cooldown = False
        self.dash_cooldown_started = 0
        self.dash_on_cooldown = False

        self.dashed_already = 0
        self.dash_length = 8
        self.hooking = False
        self.end_hook = False
        self.pull = False
        self.dashing = False
        
        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)
        
        if not server:
            self.image = pygame.Surface((2 * self.radius, 2 * self.radius)
                                        , pygame.SRCALPHA)  # make it transparent
            self.image = self.image.convert_alpha()
            
            pygame.draw.circle(self.image, color,
                (self.radius, self.radius), self.radius)

        self.name = name

    def update(self, dt, display, mouse_pos, time, keys):
        #display can be None on the server side so that
        #TODO: fix diagonal movement, has to be divided by sqrt2
        if keys[pygame.K_w] and not self.pull:
            self.move(0, -500*dt)
        if keys[pygame.K_s] and not self.pull:
            self.move(0, 500*dt)
        if keys[pygame.K_a] and not self.pull:
            self.move(-500*dt, 0)
        if keys[pygame.K_d] and not self.pull:
            self.move(500*dt, 0)
        if (keys[pygame.K_SPACE] and self.hooking is False 
            and not self.pull and not self.hook_on_cooldown):
            #runs in the first tick after presing backspace
            self.hook_cooldown_started = time
            self.hook_on_cooldown = True
            self.hooking = True
            self.hook_coords.x = self.x
            self.hook_coords.y = self.y
            self.hook_initial.x = mouse_pos[0]
            self.hook_initial.y = mouse_pos[1]
            hook_wall = self.intersect_vector_rectangle(self.hook_coords,
                                            self.hook_initial)
            self.hook_initial.x = hook_wall.x
            self.hook_initial.y = hook_wall.y
            self.hook(dt, display)
        if self.end_hook:
            #runs after it reaches boarder
            self.end_hook = False
            self.hooking = False
        if self.hooking:
            #runs after casting until reaching border
            self.hook(dt, display)
        if self.pull:
            self.pull_player(dt)
        if keys[pygame.K_LSHIFT] and not self.dash_on_cooldown:
            self.dash_cooldown_started = time
            self.dash_destination.x = mouse_pos[0]
            self.dash_destination.y = mouse_pos[1]
            self.dash(dt)
        self.check_cooldowns(time)

    #TODO: border width to config
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x - self.radius < 0:
            self.x = 5 + self.radius
        elif self.x + self.radius > self.config["resolution"]["width"]:
            self.x = self.config["resolution"]["width"] - self.radius -5
        if self.y - self.radius < 0:
            self.y = 5 + self.radius
        elif self.y + self.radius > self.config["resolution"]["height"]:
            self.y = self.config["resolution"]["height"] - self.radius -5
        self.setRect()

    #TODO: poradne vyresit jak se bude nastavovat pozice
    def setRect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def hook(self, dt, display):
        direction = self.hook_initial - self.hook_coords
        self.hook_coords += 1200*dt*(direction.normalize())
        if not self.hook_invarint():
            #begin pulling after geting out of boundary
            self.end_hook = True
            self.pull = True
            self.coords_current.x = self.x
            self.coords_current.y = self.y
        else:
            if display is not None:
                pygame.draw.line(display, "orange4", (self.x, self.y),
                            (self.hook_coords.x, self.hook_coords.y),3)

    
    def pull_player(self,dt):
        direction = self.hook_initial - self.coords_current
        self.coords_current += 1200*dt*(direction.normalize())
        self.x = self.coords_current.x
        self.y = self.coords_current.y
        #make a seperate method
        if not self.invariant():
            self.pull = False
        self.setRect()
        
    def intersect_vector_rectangle(self, point_a: Vector2, point_b: Vector2):
        #this method finds the point where vector between two points
        #intersects with the border
        t_1 = (-point_a.x)/(point_b.x - point_a.x)
        t_2 = (1280 - point_a.x)/(point_b.x - point_a.x)
        t_3 = (-point_a.y)/(point_b.y - point_a.y)
        t_4 = (720 - point_a.y)/(point_b.y - point_a.y)
        positive_solution = []
        for t in (t_1,t_2,t_3,t_4):
            if t>0:
                positive_solution.append(t)
        final_t = min(positive_solution)
        return Vector2(point_a.x + final_t*(point_b.x - point_a.x),
                       point_a.y + final_t*(point_b.y - point_a.y))
        
    def invariant(self):
        #ensures that the player stays inside the game
        if self.x - self.radius < 0:
            self.x = self.config["match"]["border_width"] + self.radius
            return False
        if self.x + self.radius > self.config["resolution"]["width"]:
            self.x = (self.config["resolution"]["width"]
                      - self.radius - self.config["match"]["border_width"])
            return False
        if self.y - self.radius < 0:
            self.y = self.config["match"]["border_width"] + self.radius
            return False
        if self.y + self.radius > self.config["resolution"]["height"]:
            self.y = (self.config["resolution"]["height"] -
                      self.radius - self.config["match"]["border_width"])
            return False
        return True
    def hook_invarint(self):
        #determines whether hook is out of bounds
        if (self.hook_coords.x < 0 or
            self.hook_coords.x > self.config["resolution"]["width"]
            or self.hook_coords.y < 0 or
            self.hook_coords.y > self.config["resolution"]["height"]):
            return False
        return True
    
    def dash(self, dt):
        if self.dashed_already == 0:
            self.dash_started.x = self.x
            self.dash_started.y = self.y
            self.coords_current.x = self.x
            self.coords_current.y = self.y
        if self.dashed_already < self.dash_length:
            direction = self.dash_destination - self.dash_started
            self.coords_current += 1600*dt*(direction.normalize())
            self.hooking = False
            self.end_hook = False
            self.pull = False
            self.dashing = True
            self.x = self.coords_current.x
            self.y = self.coords_current.y
            #make a seperate method
            if not self.invariant():
                self.dashing = False
            self.setRect()
            self.dashed_already += 1
        if self.dashed_already == self.dash_length:
            self.dashed_already = 0
            self.dash_on_cooldown = True
            
    def check_cooldowns(self, time):
        if time - self.dash_cooldown_started > 10:
            self.dash_on_cooldown = False
        if time - self.hook_cooldown_started > 20:
            self.hook_on_cooldown = False


        
if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")