import pygame

pygame.init()
# Sound
pong_sound = pygame.mixer.Sound("./Sounds/pong.ogg")
score_sound = pygame.mixer.Sound("./Sounds/score.ogg")
wall_sound = pygame.mixer.Sound("./Sounds/wall.ogg")
win_sound = pygame.mixer.Sound("./Sounds/win.ogg")
lose_sound = pygame.mixer.Sound("./Sounds/lose.ogg")
other_score_sound = pygame.mixer.Sound("./Sounds/other_score.ogg")