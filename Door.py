import pygame

def get_image(sheet, width, hieght, x, y):
    # pygame.SRCALPHA
    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, hieght))
    image = pygame.transform.scale(image, (76, 76))

    return image

class door(pygame.sprite.Sprite):

    def __init__(self, pos, group, p):
        super().__init__(group)
        self.image = get_image(pygame.image.load('Assets/Characters/door.png'), 25, 28, 0, 0)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.player = p
        self.opened = False

    def open_door(self):
        if pygame.sprite.collide_mask(self, self.player) and not self.opened:
            self.opened = True
            self.image = get_image(pygame.image.load('Assets/Characters/door_opened.png'), 25, 28, 0, 0)
