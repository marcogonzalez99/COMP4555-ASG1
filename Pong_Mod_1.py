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
        height = random.randint(25, 150)
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

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(wall_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
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

        time_counter = game_font.render(
            str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(
            center=(screen_width/2, screen_height/2 + 50))
        pygame.draw.rect(screen, background_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

    def stop_ball(self):
        self.active = False
        self.speed_x *= 0
        self.speed_y *= 0
        self.rect.center = (screen_width/2, screen_height/2)


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
        if self.rect.top < ball_group.sprite.rect.y - 15:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y + 15:
            self.rect.y -= self.speed
        self.constrain()


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Drawing the games objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.end_game()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            pygame.mixer.Sound.play(opponent_score)
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            pygame.mixer.Sound.play(score_sound)
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game_font.render(
            str(self.player_score), True, accent_color)
        opponent_score = game_font.render(
            str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(
            midleft=(screen_width/2 + 40, screen_height/2))
        opponent_score_rect = opponent_score.get_rect(
            midright=(screen_width/2 - 40, screen_height/2))
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

    def end_game(self):
        if self.player_score == 5:
            msg = game_font.render("Player Won", False, accent_color)
            screen.blit(msg, (285, 100))
            self.ball_group.sprite.stop_ball()
        if self.opponent_score == 5:
            msg = game_font.render("CPU Won", False, accent_color)
            screen.blit(msg, (305, 100))
            self.ball_group.sprite.stop_ball()


# General Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 720
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Global Varaibles
background_color = pygame.Color('#2F373F')
accent_color = (0, 0, 0)
game_font = pygame.font.Font("freesansbold.ttf", 24)
middle_strip = pygame.Rect(screen_width/2-2, 0, 4, screen_height)
game_active = False
# Sound
pong_sound = pygame.mixer.Sound("Sounds/pong.ogg")
score_sound = pygame.mixer.Sound('Sounds/score.ogg')
wall_sound = pygame.mixer.Sound('Sounds/wall.ogg')
opponent_score = pygame.mixer.Sound('Sounds/other_score.ogg')

# Game Objects
player = Player('Images/Paddle.png', screen_width-20, screen_height/2, 6)
opponent = Opponent('Images/Paddle.png', 20, screen_width/2, 6)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Images/ball.png', screen_width/2,
            screen_height/2, 5, 5, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

# Game Logo
game_logo = pygame.image.load("Images/pong_logo.png")
game_logo_rect = game_logo.get_rect(center=(360, 240))

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
                if event.key == pygame.K_1:
                    player.paddleMod()
                if event.key == pygame.K_2:
                    opponent.paddleMod()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement += player.speed
                if event.key == pygame.K_DOWN:
                    player.movement -= player.speed
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ball.reset_ball()
                ball.restart_counter()
                game_active = True

    if game_active:
        # Background Stuff
        screen.fill(background_color)
        pygame.draw.rect(screen, accent_color, middle_strip)

        # Run the Game
        game_manager.run_game()
    else:
        screen.fill(background_color)
        intro_message = game_font.render(f"Welcome to", False, accent_color)
        intro_message_rect = intro_message.get_rect(center=(360, 120))
        screen.blit(intro_message, intro_message_rect)

        start_message = game_font.render(
            f"Press Space to Start", False, accent_color)
        start_message_rect = start_message.get_rect(center=(360, 360))
        screen.blit(start_message, start_message_rect)

        screen.blit(game_logo, game_logo_rect)

    # Rendering
    pygame.display.flip()
    clock.tick(120)
