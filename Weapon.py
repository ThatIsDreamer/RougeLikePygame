import pygame


def get_image(sheet, width, hieght, x, y):
    # pygame.SRCALPHA
    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, hieght))
    image = pygame.transform.scale(image, (144, 144))

    return image


class Weapon(pygame.sprite.Sprite):

    def __init__(self, pos, group, player, chest, weapon_stats):
        super().__init__(group)
        self.weapon_stats = weapon_stats
        self.player = player
        self.chest = chest
        self.pos = pos
        self.image = get_image(pygame.image.load(f'Assets/HUD/{self.weapon_stats[1]}.png'), 0, 0, 0, 0)
        self.image = pygame.transform.scale(self.image, (42, 42))
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = float(weapon_stats[2])

    def update(self):
        pass

    def take_weapon(self):
        if pygame.sprite.collide_mask(self, self.player) and self.chest.opened:
            temp = self.player.weapon_stats
            self.player.drop_weapon(self)
            self.weapon_stats = temp
            self.image = get_image(pygame.image.load(f'Assets/HUD/{self.weapon_stats[1]}.png'), 28, 28, 0, 0)
            self.image = pygame.transform.scale(self.image, (42, 42))
            self.mask = pygame.mask.from_surface(self.image)
            self.damage = float(self.weapon_stats[2])

    def print(self):
        self.image = get_image(pygame.image.load(f'Assets/HUD/{self.weapon_stats[1]}.png'), 28, 28, 0, 0)
        self.image = pygame.transform.scale(self.image, (42, 42))
        self.mask = pygame.mask.from_surface(self.image)
