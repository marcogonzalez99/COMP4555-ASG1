from random import choice, randint
import pygame
import sys
import obstacle
from player import Player
from aliens import Alien, Extra
from laser import Laser
from settings import Settings


class Game:
    def __init__(self):
        # Load Settings
        self.level_settings = Settings()

        # Setting the state of the game to start at level 1
        self.level_num = 1

        # Get level settings
        level = self.level_settings.get_level(1)
        rows = level["rows"]
        cols = level["cols"]

        # Player Setup
        self.player_sprite = Player((screen_width/2, screen_height), screen_width, 5, self.level_num)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # Health and Score setup
        self.lives = 3
        self.life_surface = pygame.image.load(
            "Images/misc/player.png").convert_alpha()
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
        
        # Create the level 1 layout for the game
        self.alien_setup(rows, cols)
        self.alien_direction = self.alien_speed
        self.alien_lasers = pygame.sprite.Group()

        # Sound setup
        self.set_sounds()

        # Extra - Bonus Alien
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)
        
        # Win Condition
        self.level_won = False
        self.win_timer = 0

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

    # Function to setup the aliens for the game
    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=50):
        # Get level settings
        level = self.level_settings.get_level(self.level_num)
        self.alien_speed = level["alien_speed"]
        aliens = level["aliens"]

        for row_index, row in enumerate(range(rows)):
            # get alien colour for row
            alien_colour = aliens[row % len(aliens)]
            
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                        
                alien_sprite = Alien(alien_colour, x, y, self.level_num)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            # We are adding state management here as well to change speed
            if alien.rect.right >= screen_width:
                self.alien_direction = -1.0 * self.alien_speed
                self.alien_move_down(self.alien_speed)
            elif alien.rect.left <= 0:
                self.alien_direction = self.alien_speed
                self.alien_move_down(self.alien_speed)

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
                        game_state.set_state("game_over")

        # Aliens Hitting Obstacle
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    game_state.set_state("game_over")

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

    def win_check(self):
        if self.level_won:
            self.next_round()
            self.level_won = False
    
    def next_round(self):
        # This function manages the state of the round, allows us to access state and alter it easily
        if self.level_num == 5:
            # end game
            game_state.set_state("game_over")
            self.alien_setup(rows=0, cols=0)
        else:
            self.level_num += 1
            game_state.set_state("main")

        # Get level settings
        level = self.level_settings.get_level(self.level_num)
        rows = level["rows"]
        cols = level["cols"]

        # Update player sprite
        self.player.remove(self.player_sprite)
        player_sprite = Player((screen_width/2, screen_height), screen_width, 5, self.level_num)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Update alien setup
        self.alien_setup(rows, cols)
        self.win_timer = 0

        # Update sounds
        self.music.stop()
        self.set_sounds()

    def victory_message(self):
        if not self.aliens.sprites():
            self.win_timer += 1
            if self.win_timer < 100:
                victory_surface = self.font.render('You Won', False, 'white')
                victory_rect = victory_surface.get_rect(
                    center=(screen_width/2, screen_height/2))
                screen.blit(victory_surface, victory_rect)
            elif 100 < self.win_timer < 200:
                victory_surface = self.font.render('Next Level Starting', False, 'white')
                victory_rect = victory_surface.get_rect(
                    center=(screen_width/2, screen_height/2))
                screen.blit(victory_surface, victory_rect)
            elif 200 < self.win_timer < 275:
                victory_surface = self.font.render('3', False, 'white')
                victory_rect = victory_surface.get_rect(
                    center=(screen_width/2, screen_height/2))
                screen.blit(victory_surface, victory_rect)
            elif 275 < self.win_timer < 350:
                victory_surface = self.font.render('2', False, 'white')
                victory_rect = victory_surface.get_rect(
                    center=(screen_width/2, screen_height/2))
                screen.blit(victory_surface, victory_rect)
            elif 350 < self.win_timer < 425:
                victory_surface = self.font.render('1', False, 'white')
                victory_rect = victory_surface.get_rect(
                    center=(screen_width/2, screen_height/2))
                screen.blit(victory_surface, victory_rect)
            if self.win_timer > 425:
                self.level_won = False
                self.next_round()

    def set_sounds(self):
        # Get level attributes
        level = self.level_settings.get_level(self.level_num)
        bgm_path = level["bgm_path"]
        explosion_fx_path = level["explosion_fx_path"]
        laser_fx_path = level["laser_fx_path"]

        self.music = pygame.mixer.Sound(bgm_path)
        self.music.set_volume(0.1)
        self.music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound(laser_fx_path)
        self.laser_sound.set_volume(0.1)
        self.explosion_sound = pygame.mixer.Sound(explosion_fx_path)
        self.explosion_sound.set_volume(0.1)
                
    def run(self):
        # Updates
        self.player.update()
        self.extra.update()
        self.alien_lasers.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker() #Work on this to change the game speed
        self.extra_alien_timer()
        self.collision_checks()
        self.win_check()

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
        self.tv = pygame.image.load('Images/misc/tv.png').convert_alpha()
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
        self.set_state("intro")

    def set_state(self, state):
        self.state = state
        if self.state == "intro":
            # Intro text
            self.intro_message = game_font.render("Click to Start", False, 'white')
            self.intro_rect = self.intro_message.get_rect(
                center=(screen_width/2, screen_height/2 + 150))

        if self.state == "main":
            # Get specific level data
            bg_path = game.level_settings.get_value(game.level_num, "bg_path")
            self.bg = pygame.image.load(bg_path)
            self.bg = pygame.transform.scale(self.bg, (screen_width, screen_height))
        
            # Level text
            self.level_message = game_font.render(f"Level {game.level_num}", False, 'white')
            self.level_rect = self.level_message.get_rect(
                center=(screen_width/2, 25))

        if self.state == "game_over":
            # Outro text
            self.game_over_message = game_font.render("Game Over", False, 'white')
            self.game_over_rect = self.game_over_message.get_rect(
                center=(screen_width/2, screen_height/2 + 100))

            self.game_over_message_1 = game_font.render(f"Final Score: {game.score}", False, 'white')
            self.game_over_rect_1 = self.game_over_message_1.get_rect(
                center=(screen_width/2, screen_height/2 + 125))

    def state_manager(self):
        if self.state == "intro":
            self.intro()
        if self.state == "main":
            self.main()
        if self.state == "game_over":
            self.game_over()
    
    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.set_state("main") # start game

        screen.fill((30, 30, 30))
        screen.blit(self.intro_message, self.intro_rect)
        screen.blit(game_logo, game_logo_rect)
        crt.draw()
        pygame.display.flip()

    def main(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
            # force advance level
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.aliens.empty()
                    game.next_round()
                
        screen.fill((30, 30, 30))
        screen.blit(self.bg, (0, 0))
        screen.blit(self.level_message, self.level_rect)
        game.run()
        crt.draw()
        pygame.display.flip()

    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        screen.blit(game_logo,game_logo_rect)
        screen.blit(self.game_over_message, self.game_over_rect)
        screen.blit(self.game_over_message_1, self.game_over_rect_1)
        crt.draw()
        pygame.display.flip()

if __name__ == '__main__':
    # General Setup
    pygame.init()
    clock = pygame.time.Clock()

    # Font
    game_font = pygame.font.Font('Pixeltype.ttf', 40)

    # Game Screen
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")

    # Images
    game_logo = pygame.image.load('Images/misc/game_logo.png')
    game_logo_rect = game_logo.get_rect(
        center=(screen_width/2, screen_height/2 - 100))

    game_state = GameState()
    game = Game()
    crt = CRT()
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 1200)

    while True:
        game_state.state_manager()
        clock.tick(75)
