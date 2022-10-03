import pygame

# Setting up the main window
screen_width = 720
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 10, screen_height/2 - 10, 20, 20)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 100)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 100)

background = pygame.Color('#2F373F')
light_grey = (200, 200, 200)
player_color = (175, 175, 175)
opponent_color = (200, 200, 200)
ball_color = (255, 255, 255)

# Game Variabes
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7

# Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 24)

# Sound
pong_sound = pygame.mixer.Sound("./Sounds/pong.ogg")
score_sound = pygame.mixer.Sound("./Sounds/score.ogg")
wall_sound = pygame.mixer.Sound("./Sounds/wall.ogg")
win_sound = pygame.mixer.Sound("./Sounds/win.ogg")
lose_sound = pygame.mixer.Sound("./Sounds/lose.ogg")
other_score_sound = pygame.mixer.Sound("./Sounds/other_score.ogg")

# Score Timer
score_time = True