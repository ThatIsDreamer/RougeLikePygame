import pygame
from itertools import cycle

def get_image(sheet, width, hieght, x, y):
    # pygame.SRCALPHA
    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, hieght))
    image = pygame.transform.scale(image, (128, 128))

    return image



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, walls):
        super().__init__(group)
        all_anims = ["Character_Right.png", "Character_Down.png",  "Character_Left.png", "Character_Up.png"]
        self.animations = []
        for i in range(4):
            self.animations.append([get_image(pygame.image.load(f'Assets/Characters/{all_anims[i]}'), 32, 32, j * 32, 0) for j in range(4)])
        self.animations.append([get_image(pygame.image.load(f'Assets/Characters/{all_anims[1]}'), 32, 32, j * 32, 0) for j in range(1)])
        self.image = self.animations[0][0]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.curranimation = 3
        self.curr_sprite = 0
        self.walls = walls

    def move(self, dx=0, dy=0):
        if dx != 0:
            self.rect.x += dx
            if pygame.sprite.spritecollide(self, self.walls, False):
                if dx > 0:
                    self.rect.right = min(
                        wall.rect.left for wall in pygame.sprite.spritecollide(self, self.walls, False))
                elif dx < 0:
                    self.rect.left = max(
                        wall.rect.right for wall in pygame.sprite.spritecollide(self, self.walls, False))

        if dy != 0:
            self.rect.y += dy
            if pygame.sprite.spritecollide(self, self.walls, False):
                if dy > 0:
                    self.rect.bottom = min(
                        wall.rect.top for wall in pygame.sprite.spritecollide(self, self.walls, False))
                elif dy < 0:
                    self.rect.top = max(
                        wall.rect.bottom for wall in pygame.sprite.spritecollide(self, self.walls, False))


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.move(self.direction.x * self.speed, self.direction.y * self.speed)

        if self.direction[0] > 0:
            self.curranimation = 0
        if self.direction[1] > 0:
            self.curranimation = 1
        if self.direction[0] < 0:
            self.curranimation = 2
        if self.direction[1] < 0:
            self.curranimation = 3
        if self.direction[0] == 0 and self.direction[1] == 0:
            self.curranimation = 4

        self.curr_sprite += 0.03

        if self.curr_sprite >= len(self.animations[self.curranimation]) - 1:
            self.curr_sprite = 0
        self.image = self.animations[self.curranimation][int(self.curr_sprite)]