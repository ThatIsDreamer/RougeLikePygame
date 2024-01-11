import math

import pygame
import Player

def get_image(sheet, width, hieght, x, y):
    # pygame.SRCALPHA
    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, hieght))
    image = pygame.transform.scale(image, (64, 64))

    return image


pygame.mixer.init()
hit_sound = pygame.mixer.Sound("Assets/SFX/skeleton_hit.wav")

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, group, walls, player):
        super().__init__(group)

        self.HP = 2

        all_anims = ["skeleton_v2_1.png", "skeleton_v2_2.png",  "skeleton_v2_3.png", "skeleton_v2_4.png"]
        self.animations = [[], []]
        for i in range(4):
            self.animations[1].append(get_image(pygame.image.load(f'Assets/Characters/{all_anims[i]}'), 16, 16, 0, 0))
        for i in range(4):
            im = pygame.image.load(f'Assets/Characters/{all_anims[i]}')
            im = pygame.transform.flip(im, True, False)
            self.animations[0].append(get_image(im, 16, 16, 0, 0))
        self.image = self.animations[0][0]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.currsprite = 0
        self.speed = 0.9
        self.curranimation = 0
        self.walls = walls
        self.p_x = -0
        self.p_y = -0
        self.mask = pygame.mask.from_surface(self.image)
        self.player = player
        self.cooldown = False
        self.cooldown_counter = 0

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

    def player_move(self, player_x, player_y):
        self.p_x = player_x
        self.p_y = player_y

    def update(self):
        temp_x = self.p_x - self.rect.x
        temp_y = self.p_y - self.rect.y
        distance = math.sqrt(temp_x ** 2 + temp_y ** 2)
        if distance > 0:
            temp_x, temp_y = temp_x / distance, temp_y / distance
        if distance <= 500:
            self.move(temp_x * self.speed, temp_y * self.speed)

        if self.p_x > self.rect.x:
            self.currsprite = 1
        else:
            self.currsprite = 0

        self.curranimation += 0.01
        if self.curranimation > 3:
            self.curranimation = 0

        self.image = self.animations[self.currsprite][int(self.curranimation)]
        self.mask = pygame.mask.from_surface(self.image)

        if self.cooldown:
            self.cooldown_counter += 0.01

        if round(self.cooldown_counter) == 3:
            self.cooldown = False
            self.cooldown_counter = 0

        if pygame.sprite.collide_mask(self, self.player) and not self.cooldown:
            self.cooldown = True
            self.player.get_damage()

    def get_damage(self):
        self.HP -= 1
        pygame.mixer.Sound.play(hit_sound)

        for animid, animation in enumerate(self.animations):
            for frameid,  frame in enumerate(animation):
                self.animations[animid][frameid] = self.tint_surface(frame, (64, 0, 0))

    def tint_surface(self, surface, tint_color):
        surface = surface.copy()
        surface.fill(tint_color, None, pygame.BLEND_RGB_ADD)
        return surface
