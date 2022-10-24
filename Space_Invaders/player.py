import pygame
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load("Images/player.png")
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 50

        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound('Sounds/audio_laser.wav')
        self.laser_sound.set_volume(0.1)

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
