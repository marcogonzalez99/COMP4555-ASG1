import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, level):
        super().__init__()
        file_path = 'Space_invaders/' + 'Images/' + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.level = level
        if self.level == 1:
            if color == 'red':
                self.value = 50

    def update(self, direction):
        self.rect.x += direction


class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('Space_invaders/Images/extra.png').convert_alpha()

        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.speed
