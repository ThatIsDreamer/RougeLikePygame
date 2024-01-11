import pygame


def get_image(sheet, width, hieght, x, y):
    # pygame.SRCALPHA
    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, hieght))
    image = pygame.transform.scale(image, (144, 144))

    return image

# гойда


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, group, walls, player):
        super().__init__(group)
        self.animations = []
        img = get_image(pygame.image.load(f'Assets/Characters/chest.png'), 32, 32, 0, 0)
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

    def try_to_open(self):
        if pygame.sprite.collide_mask(self, self.player) and not self.opened:
            self.opening = True

    def update(self):
        if self.opening:
            self.curranimation += 0.04
            if int(self.curranimation) < 7:
                self.image = self.animations[int(self.curranimation)]
            else:
                self.image = self.animations[7]
                self.opening = False
                self.opened = False
                self.player.score += 500
