from random import choice, randint
import pygame
import sys
from player import Player
import obstacle
from aliens import Alien, Extra
from laser import Laser


class Game:
    def __init__(self):
        # Player Setup
        player_sprite = Player(
            (screen_width/2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and Score setup
        self.lives = 3
        self.life_surface = pygame.image.load(
            "Images/player.png").convert_alpha()
        self.life_x_start_pos = screen_width - \
            (self.life_surface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('Pixeltype.ttf', 40)

        # Obstacle Setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [
            num * (screen_width/self.obstacle_amount)for num in range(self.obstacle_amount)]
        self.create_multiple_objects(
            *self.obstacle_x_positions, x_start=screen_width/15, y_start=560)

        # Alien Setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

        # Extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)

        # Audio
        music = pygame.mixer.Sound('Sounds/music.wav')
        music.set_volume(0.1)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound('Sounds/audio_laser.wav')
        self.laser_sound.set_volume(0.1)
        self.explosion_sound = pygame.mixer.Sound('Sounds/audio_explosion.wav')
        self.explosion_sound.set_volume(0.1)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(
                        self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_objects(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=50):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 3:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -2
                self.alien_move_down(1)
            elif alien.rect.left <= 0:
                self.alien_direction = 2
                self.alien_move_down(1)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def collision_checks(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Obstacle
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # Aliens
                aliens_hit = pygame.sprite.spritecollide(
                    laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()
                # Extra
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 1000
                    laser.kill()

        # Alien Lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # Obstacle
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # Player
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # Aliens Hitting Obstacle
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.life_x_start_pos + \
                (live * self.life_surface.get_size()[0] + 10)
            screen.blit(self.life_surface, (x, 8))

    def display_score(self):
        score_message = self.font.render(
            f"Score: {self.score}", False, 'white')
        score_rect = score_message.get_rect(topleft=(10, 10))
        screen.blit(score_message, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surface = self.font.render('You Won', False, 'white')
            victory_rect = victory_surface.get_rect(
                center=(screen_width/2, screen_height/2))
            screen.blit(victory_surface, victory_rect)

    def run(self):
        # Updates
        self.player.update()
        self.extra.update()
        self.alien_lasers.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()
        # Drawings
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.alien_lasers.draw(screen)
        self.aliens.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()


class CRT:
    def __init__(self):
        self.tv = pygame.image.load('Images/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(
            self.tv, (screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height/line_height)

        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos),
                             (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))


class GameState():
    def __init__(self):
        self.state = "intro"

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = "main_game"

        # Intro text
        intro_message = game_font.render(
            "Click to Start", False, 'white')
        intro_rect = intro_message.get_rect(
            center=(screen_width/2, screen_height/2 + 150))

        screen.fill((30, 30, 30))
        screen.blit(intro_message, intro_rect)
        screen.blit(game_logo, game_logo_rect)

        crt.draw()
        pygame.display.flip()

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = "outro"

        screen.fill((30, 30, 30))
        game.run()
        crt.draw()
        pygame.display.flip()

    def outro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.alien_setup(rows=6, cols=8)
                self.state = "intro"

        # Outro text
        outro_message = game_font.render(
            "Game Over", False, 'white')
        outro_rect = outro_message.get_rect(
            center=(screen_width/2, screen_height/2 + 50))

        outro_message_1 = game_font.render(
            "Click To Try Again", False, 'white')
        outro_rect_1 = outro_message_1.get_rect(
            center=(screen_width/2, screen_height/2 + 100))

        screen.fill((30, 30, 30))
        screen.blit(outro_message, outro_rect)
        screen.blit(outro_message_1, outro_rect_1)
        crt.draw()
        pygame.display.flip()

    def state_manager(self):
        if self.state == "intro":
            self.intro()
        if self.state == "main_game":
            self.main_game()
        if self.state == "outro":
            self.outro()


if __name__ == '__main__':
    # General Setup
    pygame.init()
    clock = pygame.time.Clock()
    game_state = GameState()

    # Game Screen
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")

    # Images
    game_logo = pygame.image.load('Images/game_logo.png')
    game_logo_rect = game_logo.get_rect(
        center=(screen_width/2, screen_height/2 - 100))

    # Font
    game_font = pygame.font.Font('Pixeltype.ttf', 40)
    game = Game()
    crt = CRT()
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 1200)

    while True:
        game_state.state_manager()
        clock.tick(75)
