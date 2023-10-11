import pygame
from pygame.math import Vector2

# Initialize game
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720

# Set up display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Iceball")


# --------------------------PLAYER-----------------------------------

class Player:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.size = 40

    def move(self, dx, dy):
        self.position += dx, dy

    def draw(self):
        pygame.draw.circle(SCREEN, "red", self.position, self.size)


# --------------------------BALL-----------------------------------

class Ball:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.speed = Vector2(0, 0)
        self.size = 20
        print(self.position.x)
        print(self.position.y)

    def move(self):
        self.position += self.speed

    def draw(self):
        pygame.draw.circle(SCREEN, "blue", self.position, self.size)

    def checkAndHandleRebound(self):
        if self.position.x <= 0 or self.position.x >= WIDTH:
            self.speed.x = -self.speed.x
        if self.position.y <= 0 or self.position.y >= HEIGHT:
            self.speed.y = -self.speed.y


def checkCollision(p, b):
    return p.position.distance_to(b.position) < b.size


# -------------------------- MAIN-----------------------------------

def main():
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    player = Player(WIDTH // 2, HEIGHT // 2)
    ball = Ball(100, 100)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("purple")
        player.draw()
        ball.draw()
        if checkCollision(player, ball):
            ball.speed = Vector2(8, 8)

        ball.checkAndHandleRebound()

        # moving the ball
        ball.move()

        # moving the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -300*dt)
        if keys[pygame.K_s]:
            player.move(0, 300*dt)
        if keys[pygame.K_a]:
            player.move(-300*dt, 0)
        if keys[pygame.K_d]:
            player.move(300*dt, 0)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
