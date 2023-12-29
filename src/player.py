import pygame


# --------------------------PLAYER-----------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, config,radius = 40, color = "red"):
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        # width and height
        self.radius = radius
        self.x, self.y = x, y

        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)
        
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius)
                                    , pygame.SRCALPHA)  # make it transparent
        size = self.image.get_size()
        cropped_background = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.ellipse(cropped_background, (255, 255, 255, 255), (0, 0, *size))
        cropped_background.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.image = cropped_background.convert_alpha()
        
        pygame.draw.circle(self.image, color,
            (self.radius, self.radius), self.radius)


    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0, -300*dt)
        if keys[pygame.K_s]:
            self.move(0, 300*dt)
        if keys[pygame.K_a]:
            self.move(-300*dt, 0)
        if keys[pygame.K_d]:
            self.move(300*dt, 0)

    #TODO: vyresit poradne boundaries
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x < 0:
            self.x = self.config["resolution"]["width"]
        elif self.x > self.config["resolution"]["width"]:
            self. x = 0
        if self.y < 0:
            self.y = self.config["resolution"]["height"]
        elif self.y > self.config["resolution"]["height"]:
            self.y = 0
        self.setRect()

    #TODO: poradne vyresit jak se bude nastavovat pozice
    def setRect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def set_up(self, match):
        pass
# -------------------------- BOT -----------------------------------


class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y, config,radius = 40, color = "blue"):
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        # width and height
        self.radius = radius
        self.x, self.y = x, y

        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)

        self.image = pygame.Surface((2 * self.radius, 2 * self.radius)
                                    , pygame.SRCALPHA)  # make it transparent
        
        self.image = self.image.convert_alpha()
        
        pygame.draw.circle(self.image, color,
            (self.radius, self.radius), self.radius)
        
        self.ball = None
    
    def set_up(self, match):
        self.ball = match.ball

    def update(self, dt):
        # Basic AI logic to track the ball's y-coordinate
        if self.ball.y > self.y:
            self.move(dt, 1)  # Move down
        elif self.ball.y < self.y:
            self.move(dt, -1)  # Move up

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x < 0:
            self.x = self.config["resolution"]["width"]
        elif self.x > self.config["resolution"]["width"]:
            self. x = 0
        if self.y < 0:
            self.y = self.config["resolution"]["height"]
        elif self.y > self.config["resolution"]["height"]:
            self.y = 0
        self.setRect() 

    def setRect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)
        
if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")