# import game development module
import pygame
# import randinit for generating random numbers
from random import randint
# import sleep for delay
from time import sleep
# import exit for exiting the game
from sys import exit

# pixe reference for game element scaling
TILE_SIZE = 32
# initialize pygame library
pygame.init()
# set screen dimension
screen_width = 350
screen_height = 600
# creates pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
# variable for controlling frame rate
clock = pygame.time.Clock()

# Initialize Game Class
class Game:
    def __init__(self):
        self._floor = Floor()
        self._player = Player(8, self._floor._image.get_height())
        self._ball_speed = 3
        self._missed = 0
        self._score = 0
        # initial ball instances
        self._balls = [
            Ball((100, 0), 3),
            Ball((300,0), 3)
        ]
        # font setup
        self._font = pygame.font.SysFont('Arial', 30)
        # game sound Setup
        # background music
        self._bg_music = pygame.mixer.Sound('python-ball-catch/nba_sound.mp3')
        self._bg_music.set_volume(.1)
        self._bg_music.play(loops = -1)
        # sound when player catch a ball
        self._score_effect = pygame.mixer.Sound("python-ball-catch/score_effect.mp3")
        self._score_effect.set_volume(.1)
        # game over sound
        self._gameover_sound = pygame.mixer.Sound("python-ball-catch/gameoverbuzzer.wav")
        self._gameover_sound.set_volume(.1)
    # game collision method, handles missed balls and update score
    def collision(self):
        # ball list
        for ball_i in self._balls:
            # call move method for ball to move down
            ball_i.move()
            # ball collide to the floor
            if ball_i._rect.colliderect(self._floor._rect):
                # increse missed count
                self._missed += 1
                # remove balls that
                self._balls.remove(ball_i)
                self._balls.append(Ball((randint(50, 300), -50), self._ball_speed))
                if self._missed >= 3:
                    self.game_over()
            # ball collide to player
            elif ball_i._rect.colliderect(self._player._rect):
                self._balls.remove(ball_i)
                self._balls.append(Ball((randint(50, 300), -50), self._ball_speed))
                self._ball_speed += .1
                self._score += 1
                self._score_effect.play()
    # gameover method, handles gameover state
    def game_over(self):
        # play game over sound
        self._gameover_sound.play()
        # intialize game over text
        self._gameover_text = self._font.render("GAME OVER", True, (200, 200, 200))
        # intialize final score text
        self._score_text = self._font.render(f"Score: {self._score}", True, "white")
        # stop background music
        self._bg_music.stop()
        
        # change background color to black
        screen.fill("black")
        # render gameover text to screen
        screen.blit(self._gameover_text, ((screen_width / 2) - (self._gameover_text.get_width() / 2), screen_height / 2 - self._gameover_text.get_height() / 2))
        # render final score text to screen
        screen.blit(self._score_text, ((screen_width / 2) - (self._gameover_text.get_width() / 2), (screen_height / 2) + self._gameover_text.get_height()))
        
        game_over = True
        # reset game score and missed count
        self._score = 0
        self._missed = 0
        # update game screen
        pygame.display.update()
        # delay for 5 seconds
        sleep(5)
        # exit game
        pygame.quit
        exit()

    # method where we render game elements to screen and call other game methods
    def run(self):
        screen.fill("lightblue")
        screen.blit(self._player._image, self._player._rect)
        screen.blit(self._floor._image, self._floor._rect)
        self._score_text = self._font.render(f"Score: {self._score}", True, "white")
        screen.blit(self._score_text, (5, 5))
        self._missed_text = self._font.render(f"Missed: {self._missed}", True, "red")
        screen.blit(self._missed_text, (screen_width - self._missed_text.get_width(), 5))
        self._player.movement()
        for ball in self._balls:
            screen.blit(ball._image, ball._rect)
        self.collision()

# 
class Player:
    def __init__(self, speed, floor_height):
        self._image = pygame.image.load('python-ball-catch/player.png').convert_alpha()
        self._image = pygame.transform.scale(self._image, (TILE_SIZE, TILE_SIZE * 2))
        self._rect = self._image.get_rect(center = (screen.get_width() / 2,screen.get_height() - floor_height - (self._image.get_height() / 2)))
        self._speed = speed
        
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self._rect.right < screen.get_width():
            self._rect.x += self._speed
        elif keys[pygame.K_LEFT] and self._rect.left > 0 :
            self._rect.x -= self._speed
        
class Floor:
    def __init__(self):
        self._image = pygame.image.load('python-ball-catch/floor.png').convert_alpha()
        self._image = pygame.transform.scale(self._image, (TILE_SIZE * 15, TILE_SIZE * 5))
        self._rect = self._image.get_rect(bottomleft = (0,screen.get_height()))

class Ball:
    def __init__(self, position, speed):
        self._image = pygame.image.load('python-ball-catch/ball.png').convert_alpha()
        self._image = pygame.transform.scale(self._image, (TILE_SIZE, TILE_SIZE))
        self._rect = self._image.get_rect(topleft = position)
        self._ball_speed = speed
    
    def move(self):
        self._rect.y += self._ball_speed

game = Game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    game.run()
    clock.tick(60)
    pygame.display.update()
    