from re import A
from tkinter import Y
import pygame
import sys
import random


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    # Paddle Mod - Changes the size of the paddle depending on what key was pressed
    def paddleMod(self):
        height = random.randint(25, 200)
        self.image = pygame.transform.scale(self.image, (10, height))
        self.rect.height = height


class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0
        self.message_time = 0
        self.redirect_on = False

    def update(self, player):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions(player)
            self.message_time_get()
        else:
            self.restart_counter()

    def speedMod(self, input):
        original_speed_x = self.speed_x
        original_speed_y = self.speed_y
        if input == 0:
            self.speed_x /= 1.1
            self.speed_y /= 1.1
        elif input == 1:
            self.speed_x *= 1.1
            self.speed_y *= 1.1
    def message_time_get(self):
        return self.message_time

    def collisions(self, player):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(wall_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.redirect_mod(player)
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_x < 0:
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_x > 0:
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.message_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2, screen_height/2)

    def restart_counter(self):
        global current_time
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = game1_font.render(
            str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(
            center=(screen_width/2+1, screen_height/2 + 110))
        pygame.draw.rect(screen, background_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

    def stop_ball(self):
        self.active = False
        self.speed_x *= 0
        self.speed_y *= 0
        self.rect.center = (screen_width/2, screen_height/2)

    # Brian's Mod - allows player to control redirect of ball
    def redirect_mod(self, player):
        # Only perform redirect if enabled
        if self.redirect_on:
            # If player is moving oposite direction of ball_speed_y, reverse ball_speed_y
            if (player.speed > 0 and self.speed_y < 0) or (player.speed < 0 and self.speed_y > 0):
                self.speed_y *= -1

    # Toggle redirect on and off
    def toggle_redirect_mod(self):
        if self.redirect_on:
            self.redirect_on = False
        else:
            self.redirect_on = True


class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.speed = speed

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y - 12:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y + 12:
            self.rect.y -= self.speed
        self.constrain()


class Barrier(Block):
    def __init__(self, path, x_pos, y_pos):
        super().__init__(path, x_pos, y_pos)
        

class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self, player):
        # Drawing the games objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update(player)
        self.end_game()
        self.reset_ball()
        self.draw_score()
        self.encouragement_message()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width and self.opponent_score < 5:
            self.opponent_score += 1
            pygame.mixer.Sound.play(opponent_score)
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0 and self.player_score < 5:
            self.player_score += 1
            pygame.mixer.Sound.play(score_sound)
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game1_font.render(
            str(self.player_score), True, accent_color)
        opponent_score = game1_font.render(
            str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(
            midleft=(screen_width/2 + 20, screen_height/2))
        opponent_score_rect = opponent_score.get_rect(
            midright=(screen_width/2 - 20, screen_height/2))
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

    # display active mods
    def display_mode(self):
        if ball.redirect_on:
            msg = game_font.render("Redirect Mode On", False, accent_color)
            screen.blit(msg, (screen_width/4 - msg.get_width()/2, 20))
    # Latonia's Mod - encouragement message at start of each round
    def encouragement_message(self):
        light_grey = (200, 200, 200)
        current_time = pygame.time.get_ticks()
        if self.player_score > self.opponent_score and self.player_score < 5 and current_time - self.ball_group.sprite.message_time_get() < 700:
            encouragement_text = game_font.render(
                f"Nice, Keep it p!", False, light_grey)
            screen.blit(encouragement_text, (screen_width/2 -
                        encouragement_text.get_width()/2, 100))
        elif self.player_score < self.opponent_score and self.opponent_score < 5 and current_time - self.ball_group.sprite.message_time_get() < 700:
            encouragement_text = game_font.render(
                f"Don't Give Up!", False, light_grey)
            screen.blit(encouragement_text, (screen_width/2 -
                        encouragement_text.get_width()/2, 100))

    def end_game(self):
        if self.player_score == 5:
            msg = game_font.render("Player Won", False, accent_color)
            screen.blit(msg, (285, 100))
            self.ball_group.sprite.stop_ball()
        if self.opponent_score == 5:
            msg = game_font.render("CPU Won", False, accent_color)
            screen.blit(msg, (305, 100))
            self.ball_group.sprite.stop_ball()

    # Wall mods - places a barrier in a randomly generated location for the session
    def despawnBarrier(self):
        paddle_group.remove(barrier)

    def spawnBarrier(self):
        paddle_group.add(barrier)


# General Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Global Varaibles
background_color = pygame.Color('#2F373F')
accent_color = (0, 0, 0)
game_font = pygame.font.Font("Pixeltype.ttf", 100)
game1_font = pygame.font.Font("Pixeltype.ttf", 50)
middle_strip = pygame.Rect(screen_width/2-2, 0, 4, screen_height)
game_active = False

# Sound
pong_sound = pygame.mixer.Sound("Sounds/pong.ogg")
score_sound = pygame.mixer.Sound("Sounds/score.ogg")
wall_sound = pygame.mixer.Sound("Sounds/wall.ogg")
opponent_score = pygame.mixer.Sound("Sounds/other_score.ogg")
win_sound = pygame.mixer.Sound("Sounds/win.ogg")
lose_sound = pygame.mixer.Sound("Sounds/lose.ogg")

# Game Objects
player = Player('Images/Paddle.png', screen_width-20, screen_height/2, 7)
opponent = Opponent('Images/Paddle.png', 20, screen_width/2, 7)
barrier = Barrier('Images/Paddle.png', random.randint(20, screen_width-20), random.randint(0, screen_height))
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Images/ball.png', screen_width/2,
            screen_height/2, 7, 7, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

# Game Logo
game_logo = pygame.image.load("Images/pong_logo.png")
game_logo_rect = game_logo.get_rect(
    center=(screen_width/2, screen_height/2 - 50))

game_manager = GameManager(ball_sprite, paddle_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.movement -= player.speed
                if event.key == pygame.K_DOWN:
                    player.movement += player.speed
                if event.key == pygame.K_ESCAPE:
                    game_active = False
                if event.key == pygame.K_1:
                    player.paddleMod()
                if event.key == pygame.K_2:
                    opponent.paddleMod()
                if event.key == pygame.K_3:
                    ball.toggle_redirect_mod()
                if event.key == pygame.K_4:
                    game_manager.spawnBarrier()
                if event.key == pygame.K_5:
                    game_manager.despawnBarrier()
                if event.key == pygame.K_6:
                    ball.speedMod(0)
                elif event.key == pygame.K_7:
                    ball.speedMod(1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement += player.speed
                if event.key == pygame.K_DOWN:
                    player.movement -= player.speed
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_manager.player_score = 0
                game_manager.opponent_score = 0
                ball.reset_ball()
                ball.restart_counter()
                game_active = True

    if game_active:
        # Background Stuff
        screen.fill(background_color)
        pygame.draw.rect(screen, accent_color, middle_strip)

        # Run the Game
        game_manager.run_game(player)
        game_manager.display_mode()
        if game_manager.player_score == 5:
            game_manager.player_score = 0
            game_manager.opponent_score = 0
            game_active = False
        if game_manager.opponent_score == 5:
            game_manager.player_score = 0
            game_manager.opponent_score = 0
            game_active = False

    else:
        screen.fill(background_color)
        intro_message = game_font.render(f"Welcome to", False, accent_color)
        intro_message_rect = intro_message.get_rect(
            center=(screen_width/2, 100))
        screen.blit(intro_message, intro_message_rect)

        start_message = game_font.render(
            f"Press Space to Start", False, accent_color)
        start_message_rect = start_message.get_rect(
            center=(screen_width/2, screen_height - 200))

        paddle_mod_message = game1_font.render(
            f"Paddle Mod (Keys 1 and 2)", False, accent_color)
        paddle_mod_message_rect = paddle_mod_message.get_rect(
            topleft=(10, screen_height - 80))

        redirect_mod_message = game1_font.render(
            f"Redirect Mod (Key 3)", False, accent_color)
        redirect_mod_message_rect = redirect_mod_message.get_rect(
            topleft=(10, screen_height - 40))

        encourage_mod_message = game1_font.render(
            f"Encourage Mod ", False, accent_color)
        encourage_mod_message_rect = encourage_mod_message.get_rect(
            topright=(screen_width, screen_height - 40))

        wall_mod_message = game1_font.render(
            f"Wall Mod (Keys 4 and 5)", False, accent_color)
        wall_mod_message_rect = wall_mod_message.get_rect(
            topright=(screen_width, screen_height - 120))

        speed_mod_message = game1_font.render(
            f"Speed Mod (Keys 6 and 7)", False, accent_color)
        speed_mod_message_rect = speed_mod_message.get_rect(
            topright=(screen_width, screen_height - 80))

        screen.blit(paddle_mod_message, paddle_mod_message_rect)
        screen.blit(redirect_mod_message, redirect_mod_message_rect)
        screen.blit(encourage_mod_message, encourage_mod_message_rect)
        screen.blit(wall_mod_message, wall_mod_message_rect)
        screen.blit(speed_mod_message, speed_mod_message_rect)
        screen.blit(start_message, start_message_rect)
        screen.blit(game_logo, game_logo_rect)

    # Rendering
    pygame.display.flip()
    clock.tick(120)
