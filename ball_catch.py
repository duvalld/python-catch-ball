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
        self._game_count = 1
        self._missed = 0
        self._score = 0
        self._game_history_list = []
        # initial ball instances
        self._balls = [
            Ball((100, 0), 3),
            Ball((300,0), 3)
        ]
        # font setup
        self._font = pygame.font.SysFont('Arial', 30)
        # game sound Setup
        # background music
        self._bg_music = pygame.mixer.Sound('python-catch-ball/sound/nba_sound.mp3')
        self._bg_music.set_volume(.1)
        self._bg_music.play(loops = -1)
        # sound when player catch a ball
        self._score_effect = pygame.mixer.Sound("python-catch-ball/sound/score_effect.mp3")
        self._score_effect.set_volume(.1)
        # game over sound
        self._gameover_sound = pygame.mixer.Sound("python-catch-ball/sound/gameoverbuzzer.wav")
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
                # remove balls that collide to the floor
                self._balls.remove(ball_i)
                # add new ball instance to balls list
                self._balls.append(Ball((randint(50, 300), -50), self._ball_speed))
                # if player missed 3 balls call gameover method
                if self._missed >= 3:
                    self.game_history()
                    self.game_over()
            # ball collide to player
            elif ball_i._rect.colliderect(self._player._rect):
                # remove balls that collide to the player
                self._balls.remove(ball_i)
                # add new ball instance to balls list
                self._balls.append(Ball((randint(50, 300), -50), self._ball_speed))
                # increse ball movement speed by .1
                self._ball_speed += .1
                # increse score count per ball
                self._score += 1
                # play sound effect for every catched ball
                self._score_effect.play()
    # gameover method, handles gameover state
    def game_over(self):
        # clear balls on screen
        self._balls.clear()
        # reinitialize balls
        self._balls = [
            Ball((100, 0), 3),
            Ball((300,0), 3)
        ]
        # play game over sound
        self._gameover_sound.play()
        # intialize game over text
        self._gameover_text = self._font.render("GAME OVER", True, (200, 200, 200))
        # intialize final score text
        self._score_text = self._font.render(f"Score: {self._score}", True, "white")
        # initialize play again text
        self._play_again_text = self._font.render("Press SPACE to play again...", True, (200, 200, 200))
        # initialize error text
        self._error_text = self._font.render("Press Space Only", True, (255, 0, 0))
        # stop background music
        self._bg_music.stop()
        
        # change background color to black
        screen.fill("black")
        # render gameover text to screen
        screen.blit(self._gameover_text, ((screen_width / 2) - (self._gameover_text.get_width() / 2), screen_height / 2 - self._gameover_text.get_height() / 2))
        # render final score text to screen
        screen.blit(self._score_text, ((screen_width / 2) - (self._gameover_text.get_width() / 2), (screen_height / 2) + self._gameover_text.get_height()))
        # Render play again text
        screen.blit(self._play_again_text, (10, screen_height - self._play_again_text.get_height()))
        # render Game Score history
        game_history_position_height = 10
        for game_history_i in self._game_history_list:
            self._game_history_text = self._font.render(f"Game: {game_history_i[0]} Score: {game_history_i[1]}", True, "white")
            screen.blit(self._game_history_text, (10, game_history_position_height))
            game_history_position_height += self._game_history_text.get_height() + 5
        # reset game score and missed count
        self._score = 0
        self._missed = 0
        # update game screen
        pygame.display.update()
        # play again input
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_input = False
                        self._bg_music.play(loops= -1)
                        self._ball_speed = 3
                        self._game_count += 1
                        
                    else:
                        screen.blit(self._error_text, (10, screen_height - self._play_again_text.get_height()-self._error_text.get_height()))
                        pygame.display.update()
    # populate game history list
    def game_history(self):
        self._game_history_list.append([self._game_count, self._score])
        
    # Welcome Screen
    def welcom_screen(self):
        screen.fill("lightblue")
        screen.blit(self._player._image, self._player._rect)
        screen.blit(self._floor._image, self._floor._rect)
        self._welcome_text = self._font.render("Catch Ball!", True, (255, 165, 0))
        screen.blit(self._welcome_text, ((screen_width / 2) - (self._welcome_text.get_width() / 2), 200))
        font_welcome = pygame.font.SysFont('Arial', 15)
        welcome_text_list = [
            "Dash and catch your way to a high score",
            "in this heart-pounding ball-catching game,",
            "but watch out miss three, and it's game over!"
        ]
        welcome_text_pos_height = 200 + self._welcome_text.get_height() + 5
        for t in welcome_text_list:
            self._mechanics_text = font_welcome.render(t, True, (0, 0, 0))
            screen.blit(self._mechanics_text, ((screen_width / 2) - (self._mechanics_text.get_width() / 2), welcome_text_pos_height))
            welcome_text_pos_height += self._mechanics_text.get_height() + 5

        pygame.display.update()
        sleep(5)
    
    # method where we render game elements to screen and call other game methods
    def run(self):
        # set background to color lightblue
        screen.fill("lightblue")
        # render player model on game screen
        screen.blit(self._player._image, self._player._rect)
        # render floor model on game
        screen.blit(self._floor._image, self._floor._rect)
        self._score_text = self._font.render(f"Score: {self._score}", True, "white")
        # render score text on game screen
        screen.blit(self._score_text, (5, 5))
        self._missed_text = self._font.render(f"Missed: {self._missed}", True, "red")
        # render missed ball on game screen
        screen.blit(self._missed_text, (screen_width - self._missed_text.get_width(), 5))
        self._game_count_text = self._font.render(f"Game {self._game_count}", True, "orange")
        screen.blit(self._game_count_text, ((screen_width / 2) - (self._missed_text.get_width() / 2), 5))
        # call player movement method
        self._player.movement()
        # render ball object from balls list
        for ball in self._balls:
            screen.blit(ball._image, ball._rect)
        # call collission method
        self.collision()

# initialize Player Class
class Player:
    def __init__(self, speed, floor_height):
        # set player image
        self._image = pygame.image.load('python-catch-ball/image/player.png').convert_alpha()
        # transfrom player image scale
        self._image = pygame.transform.scale(self._image, (TILE_SIZE, TILE_SIZE * 2))
        # set rectangle object for player image that we can use for positioning and collision
        self._rect = self._image.get_rect(center = (screen.get_width() / 2,screen.get_height() - floor_height - (self._image.get_height() / 2)))
        # player movement per pixel
        self._speed = speed

    # Player movement method
    def movement(self):
        keys = pygame.key.get_pressed()
        # move player to left/righ when left/righ arrow key is pressed and limit movement when end of the screen has been reached
        if keys[pygame.K_RIGHT] and self._rect.right < screen.get_width():
            self._rect.x += self._speed
        elif keys[pygame.K_LEFT] and self._rect.left > 0 :
            self._rect.x -= self._speed

# Floor class intialization
class Floor:
    def __init__(self):
        # set floor image
        self._image = pygame.image.load('python-catch-ball/image/floor.png').convert_alpha()
        # transform floor image scale
        self._image = pygame.transform.scale(self._image, (TILE_SIZE * 15, TILE_SIZE * 5))
        # set rectangle object for floor positioning and collision
        self._rect = self._image.get_rect(bottomleft = (0,screen.get_height()))

# Ball class initialization
class Ball:
    def __init__(self, position, speed):
        # set ball image
        self._image = pygame.image.load('python-catch-ball/image/ball.png').convert_alpha()
        # transform ball image scale
        self._image = pygame.transform.scale(self._image, (TILE_SIZE, TILE_SIZE))
        # set rectangle object for ball positioning and collision
        self._rect = self._image.get_rect(topleft = position)
        # ball movement per pixel
        self._ball_speed = speed
    
    # ball movement method
    def move(self):
        # move ball on y axis based on ball speed
        self._rect.y += self._ball_speed

game = Game()
running = True

# welcome message
game.welcom_screen()

# Game loop
while running:
    # close game when close button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # call game run method
    game.run()
    # limit game Frame Rate to 60
    clock.tick(60)
    # update game screen per loop
    pygame.display.update()
    