import pygame
import json

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, level):
        super().__init__()

        # Load Settings
        file = open("config.json")
        data = json.load(file)
        self.level_settings = data["level_settings"]

        file_path = 'Images/alien/' + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.level = level

        # Get level specific data
        for level in self.level_settings:
            if level["level"] == self.level:
                self.value = level[f"{color}_value"]

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
