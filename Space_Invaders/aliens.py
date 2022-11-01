import pygame
from settings import Settings

class Alien(pygame.sprite.Sprite):
    def __init__(self, colour, x, y, level_num):
        super().__init__()

        # Load Settings
        level_settings = Settings()

        # set colour
        file_path = 'Images/alien/' + colour + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        # set value
        values = level_settings.get_value(level_num, "values")
        self.value = values[colour]


    def update(self, direction):
        self.rect.x += direction


class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('Images/alien/extra.png').convert_alpha()

        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.speed
