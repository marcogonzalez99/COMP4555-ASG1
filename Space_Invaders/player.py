import pygame
from laser import Laser
from settings import Settings

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed, level_num):
        super().__init__()
        
        # Load Settings
        level_settings = Settings()

        # Get level attributes
        level = level_settings.get_level(level_num)
        player_path = level["player_path"]
        laser_fx_path = level["laser_fx_path"]

        # To change the design of the ship
        self.image = pygame.image.load(player_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 500
        self.lasers = pygame.sprite.Group()

        # Set laser sound
        self.laser_sound = pygame.mixer.Sound(laser_fx_path)
        self.laser_sound.set_volume(0.15)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constrain(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x:
            self.rect.right = self.max_x

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    def update(self):
        self.get_input()
        self.constrain()
        self.recharge()
        self.lasers.update()
