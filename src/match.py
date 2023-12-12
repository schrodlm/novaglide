"""_summary_
"""
import pygame
from pygame import Vector2
from ball import Ball




class Match():
    def __init__(self,game):
        self.game = game
        self.match_time = 5*60
        self.score = (0,0)
        self.tiebreak = False

        self.entities = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.last_tick = pygame.time.get_ticks()
        self.ttime = self.clock.tick()
        self.clock.tick(60)
        self.keys_pressed = pygame.key.get_pressed()

        self.playing = True



class Match1v1(Match):

    def __init__(self, game, p1, p2):
        super().__init__(game)
        self.p1 = p1
        self.p2 = p2
        self.ball = Ball(400,400,self.game.config)
        self.entities.add(self.ball, self.p1, self.p2)
        self.p1.set_up(self)
        self.p2.set_up(self)

    def draw(self):
        self.game.display.fill((150,150,150))
        if pygame.sprite.collide_circle(self.p1,self.ball) or pygame.sprite.collide_circle(self.p2,self.ball) :
            # 1. Calculate the collision normal
            collision_normal = self.ball.rect.center - Vector2(self.game.player.rect.center)
            collision_normal.normalize_ip()  # Normalize the vector to have a magnitude of 1

            # 2. Determine the new speed of the ball
            speed_magnitude = 20  # You can adjust this value as needed
            self.ball.speed = collision_normal * speed_magnitude
    
        self.dt = self.clock.tick(60) / 1000
        self.p1.update(self.dt)
        self.p2.update(self.dt)
        self.ball.update()

        for e in self.entities: #update blocks etc.
            self.game.display.blit(e.image, e.rect)
        
        self.game.screen.blit(self.game.display, (0,0))
        pygame.display.update()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def match_loop(self):

        while self.playing:
        # main game loop
            self.check_events()
            self.game.Tick()
            self.draw()
            self.game.reset_keys()