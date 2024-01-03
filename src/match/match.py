"""_summary_
"""
import datetime
import pygame
from pygame import Vector2
from game_objects.ball import Ball
from match.match_stats import MatchStats

pygame.init()

class Match():
    def __init__(self, config):
        self.match_duration = 5*60
        self.score = (0,0)
        self.tiebreak = False
        self.config = config
        self.entities = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.last_tick = pygame.time.get_ticks()
        self.ttime = self.clock.tick()
        self.clock.tick(60)
        self.playing = True
         # Define goals as rectangles
        goal_width = 20  # Width of the goal, adjust as needed
        goal_height = 100  # Height of the goal, adjust as needed
        self.max_height, self.max_width = self.config["resolution"]["height"], self.config["resolution"]["width"]
        self.goal1 = pygame.Rect(0, (self.max_height - goal_height) // 2, goal_width, goal_height)
        self.goal2 = pygame.Rect(self.max_width - goal_width, (self.max_height - goal_height) // 2, goal_width, goal_height)

        # Define borders
        self.display = pygame.Surface((self.max_width,self.max_height))
        self.border = self.display.get_rect()

        self.mpos_1 = (0,0)
        self.mpos_2 = (0,0)
        self.start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        self.elapsed_time = 0
        self.dash_time_1 = 0
        self.hook_time_1 = 0
        self.dash_time_2 = 0
        self.hook_time_2 = 0
        self.remaining_time = self.match_duration
class Match1v1(Match):

    def __init__(self, config, p1, p2, ball, p1_id, p2_id):
        super().__init__(config)
        self.p1_id = p1_id
        self.p2_id = p2_id
        self.p1 = p1
        self.p2 = p2
        self.ball = ball
        self.entities.add(self.ball, self.p1, self.p2)
        #Stat class initialized
        self.match_stats = MatchStats(entities=self.entities)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def reset_ball(self):
        self.ball.x = self.max_width // 2
        self.ball.y = self.max_height // 2
        # Reset the ball's speed
        # You can set this to an initial speed or to zero
        self.ball.speed = Vector2(0, 0)
        # Update the ball's rect to reflect the new position
        self.ball.setRect()


    def update_game_state(self):

    # Check for ball collision with goals
        if self.goal1.colliderect(self.ball.rect):
            # Ball has entered goal 1
            # Update score and reset ball position, etc.
            self.score = (self.score[0], self.score[1] + 1)
            self.match_stats.add_goal(self.p1)
            self.reset_ball()

        if self.goal2.colliderect(self.ball.rect):
            # Ball has entered goal 2, increment score for player 1
            self.score = (self.score[0] + 1, self.score[1])
            self.match_stats.add_goal(self.p2)
            self.reset_ball()

        
        if pygame.sprite.collide_circle(self.p1,self.ball) or pygame.sprite.collide_circle(self.p2,self.ball) :
            # 1. Calculate the collision normal
            if pygame.sprite.collide_circle(self.p1, self.ball):
                collision_normal = self.ball.rect.center - Vector2(self.p1.rect.center)
                self.match_stats.add_touch(self.p1)
            else:
                collision_normal = self.ball.rect.center - Vector2(self.p2.rect.center)
                self.match_stats.add_touch(self.p2)
                
            collision_normal.normalize_ip()  # Normalize the vector to have a magnitude of 1

            # 2. Determine the new speed of the ball
            speed_magnitude = 20  # You can adjust this value as needed
            self.ball.speed = collision_normal * speed_magnitude
        
        self.dt = self.clock.tick(60) / 1000
          
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.remaining_time = max(self.match_duration - self.elapsed_time, 0)

        self.p1.update(self.dt, None, pygame.mouse.get_pos(), self.elapsed_time)
        self.p2.update(self.dt)
        self.ball.update(self.border)
        
        #calculating cooldowns for both players
        #Player_1
        self.dash_time_1 = 10 - abs(self.elapsed_time - self.p1.dash_cooldown_started)
        self.hook_time_1 = 20 - abs(self.elapsed_time - self.p1.hook_cooldown_started)
        self.dash_time_1 = max(0,self.dash_time_1)
        self.dash_time_1 = min(self.dash_time_1, 10)
        self.hook_time_1 = max(0,self.hook_time_1)
        self.hook_time_1 = min(self.hook_time_1, 20)
        if self.p1.dash_cooldown_started == 0:
            self.dash_time_1 = 0
        if self.p1.hook_cooldown_started == 0:
            self.hook_time_1 = 0
        #Player_2
        self.dash_time_2 = 10 - abs(self.elapsed_time - self.p2.dash_cooldown_started)
        self.hook_time_2 = 20 - abs(self.elapsed_time - self.p2.hook_cooldown_started)
        self.dash_time_2 = max(0,self.dash_time_2)
        self.dash_time_2 = min(self.dash_time_2, 10)
        self.hook_time_2 = max(0,self.hook_time_2)
        self.hook_time_2 = min(self.hook_time_2, 20)
        if self.p2.dash_cooldown_started == 0:
            self.dash_time_2 = 0
        if self.p2.hook_cooldown_started == 0:
            self.hook_time_2 = 0
    

    def end_match(self):
        # Determine the winner based on the score
        if self.score[0] > self.score[1]:
            self.match_stats.set_winner(self.p2)
        elif self.score[0] < self.score[1]:
            self.match_stats.set_winner(self.p1)

        # Stop the game loop
        self.playing = False

    def get_match_stats(self):
        return self.match_stats

    def share_state(self):
        return [self.remaining_time, self.score[0], self.score[1],
            self.p1.x, self.p1.y, self.mpos_1[0],self.mpos_1[1], 
            self.mpos_2[0],self.mpos_2[1]]

    def match_loop(self):
        # main game loop
        self.check_events()
        self.update_game_state()
            # Update the timer
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert milliseconds to seconds
        if self.elapsed_time >= self.match_duration:
            self.end_match()