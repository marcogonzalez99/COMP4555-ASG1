import pygame
from settings import *

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