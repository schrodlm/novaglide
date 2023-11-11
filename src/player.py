import pygame
import settings

# --------------------------PLAYER-----------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, radius = 40, color = "red"):
        pygame.sprite.Sprite.__init__(self)

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
            self.x = settings.WIDTH
        elif self.x > settings.WIDTH:
            self. x = 0
        if self.y < 0:
            self.y = settings.HEIGHT
        elif self.y > settings.HEIGHT:
            self.y = 0
        self.setRect()        

    #TODO: poradne vyresit jak se bude nastavovat pozice
    def setRect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)
