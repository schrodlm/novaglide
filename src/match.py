"""_summary_
"""
import pygame
from pygame import Vector2
from ball import Ball
from match_stats import MatchStats

pygame.init()

class Match():
    def __init__(self,display):
        self.display = display
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


         # Define goals as rectangles
        goal_width = 20  # Width of the goal, adjust as needed
        goal_height = 100  # Height of the goal, adjust as needed
        self.goal1 = pygame.Rect(0, (self.display.get_height() - goal_height) // 2, goal_width, goal_height)
        self.goal2 = pygame.Rect(self.display.get_width() - goal_width, (self.display.get_height() - goal_height) // 2, goal_width, goal_height)

        # Define borders
        self.border = self.display.get_rect()

        self.font = pygame.font.Font(None, 36)

         # Initialize the match timer
        self.match_duration = 5  # 5 minutes in seconds
        self.start_time = pygame.time.get_ticks()  # Get the current time in milliseconds




class Match1v1(Match):

    def __init__(self, display, p1, p2, ball):
        super().__init__(display)
        self.p1 = p1
        self.p2 = p2
        self.ball = ball
        self.entities.add(self.ball, self.p1, self.p2)
        self.p1.set_up(self)
        self.p2.set_up(self)


        #Stat class initialized
        self.match_stats = MatchStats(entities=self.entities)

    def draw(self):
        self.display.fill((150,150,150))
        
        # Render and draw the score
        score_text = f"{self.score[0]} - {self.score[1]}"
        score_surface = self.font.render(score_text, True, (255, 255, 255))  # White text
        score_x = self.display.get_width() // 2 - score_surface.get_width() // 2
        score_y = 10  # 10 pixels from the top
        self.display.blit(score_surface, (score_x, score_y))

        self.dt = self.clock.tick(60) / 1000
        self.p1.update(self.dt, self.display, pygame.mouse.get_pos())
        self.p2.update(self.dt)
        self.ball.update(self.border)
            
        for e in self.entities: #update blocks etc.
            self.display.blit(e.image, e.rect)
        

            # Draw goals
        pygame.draw.rect(self.display, (255, 255, 255), self.goal1)  # White goal
        pygame.draw.rect(self.display, (255, 255, 255), self.goal2)  # White goal

        # Draw the playfield border
        border_thickness = 5
        pygame.draw.rect(self.display, (255, 255, 255), self.border, border_thickness)

         # Display the timer
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        remaining_time = max(self.match_duration - elapsed_time, 0)
        timer_surface = self.font.render(f"Time Left: {int(remaining_time)}s", True, (255, 255, 255))
        self.display.blit(timer_surface, (10, 10))  # Adjust position as needed



    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def reset_ball(self):
        center_x = self.display.get_width() // 2
        center_y = self.display.get_height() // 2
        self.ball.x = center_x
        self.ball.y = center_y

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


    def match_loop(self):
        # main game loop
            self.check_events()
            self.update_game_state()
            self.draw()

             # Update the timer
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert milliseconds to seconds
            if elapsed_time >= self.match_duration:
                self.end_match()