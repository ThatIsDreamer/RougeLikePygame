import pygame
import Database
import Weapon


def get_image(sheet, width, hieght, x, y):
    # pygame.SRCALPHA
    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, hieght))
    image = pygame.transform.scale(image, (144, 144))

    return image


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, group, walls, player, weapon=None):
        super().__init__(group)

        self.group = group
        self.pos = pos
        self.weapon = weapon

        self.animations = []
        img = get_image(pygame.image.load('Assets/Characters/chest.png'), 32, 32, 0, 0)
        img = pygame.transform.scale(img, (84, 84))
        self.animations.append(img)
        d = {32: 64, 64: 32}
        s = 32
        for i in range(6):
            img = get_image(pygame.image.load(f'Assets/Characters/chest.png'), 32, 32, 0, s)
            img = pygame.transform.scale(img, (84, 84))
            s = d[s]
            self.animations.append(img)
        img = get_image(pygame.image.load(f'Assets/Characters/chest.png'), 32, 32, 0, 96)
        img = pygame.transform.scale(img, (84, 84))
        self.animations.append(img)
        self.image = self.animations[0]
        self.rect = self.image.get_rect(center=pos)
        self.player = player
        self.curranimation = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.opened = False
        self.opening = False
        self.content = Database.select_weapon()

    def try_to_open(self):
        if pygame.sprite.collide_mask(self, self.player) and not self.opened:
            self.opening = True
            #Мда артем такое забыть добавить....
            # self.opened = True
            # Гений, это в update уже есть

    def update(self):
        if self.opening:
            self.curranimation += 0.04
            if int(self.curranimation) < 7:
                self.image = self.animations[int(self.curranimation)]
            else:
                self.image = self.animations[7]
                self.opening = False
                self.opened = True
                self.player.score += 500
                if self.player.HP != 0:
                    self.player.HP += 3
                self.weapon.print()
