import pygame
import sys
import random


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball Border
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(wall_sound)
        ball_speed_y *= -1

    if ball.left <= 0:  # Player Scores
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:  # Opponent Scores
        pygame.mixer.Sound.play(other_score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    # Collisions
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0 + 5
    if player.bottom >= screen_height:
        player.bottom = screen_height - 5


def opponent_ai():
    if opponent.top < ball.y:  # This adjustment is for how strong the AI will be
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:  # This adjustment is for how strong the AI will be
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0 + 5
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height - 5


def ball_start():
    global ball_speed_x, ball_speed_y, score_time, player, opponent

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width/2-5, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (screen_width/2-5, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (screen_width/2-5, screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


def score_logic():
    if (player_score == 5):
        msg = game_font.render("Player Won", False, light_grey)
        screen.blit(msg, (290, 300))
        pygame.mixer.Sound.play(win_sound)
        game_end()
    if (opponent_score == 5):
        msg = game_font.render("CPU Won", False, light_grey)
        screen.blit(msg, (290, 300))
        game_end()


def game_end():
    global ball_speed_x, ball_speed_y
    ball_speed_x, ball_speed_y = 0, 0


# General Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 720
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong - Original")

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
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound('score.ogg')
wall_sound = pygame.mixer.Sound('wall.ogg')
win_sound = pygame.mixer.Sound("win.ogg")
lose_sound = pygame.mixer.Sound('lose.ogg')
other_score_sound = pygame.mixer.Sound('other_score.ogg')
# Score Timer
score_time = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_ai()

    # Visuals - In order from top to bottom
    screen.fill(background)
    pygame.draw.rect(screen, player_color, player)
    pygame.draw.rect(screen, opponent_color, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2,
                                            0), (screen_width/2, screen_height))

    score_logic()

    if score_time:
        ball_start()

    player_text = game_font.render(
        f"{player_score}", False, light_grey)
    screen.blit(player_text, (375, 240))

    opponent_text = game_font.render(
        f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (335, 240))

    pygame.display.flip()
    clock.tick(75)
