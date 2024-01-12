import pygame
import math

def get_image(sheet, width, hieght, x, y):

    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, hieght))
    image = pygame.transform.scale(image, (144, 144))

    return image

pygame.mixer.init()
hit_sound = pygame.mixer.Sound("Assets/SFX/hit.wav")


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, walls):
        super().__init__(group)

        self.HP = 5

        self.radius = 80

        self.animations = []
        for i in range(3, 7):
            self.animations.append(
                [get_image(pygame.image.load(f'Assets/Characters/player.png'), 48, 48, j * 48, i * 48) for j in
                 range(6)])
        self.animations.append(
            [get_image(pygame.image.load(f'Assets/Characters/player.png'), 48, 48, j * 48, 48) for j in range(1)])

        self.animations[3] = self.animations[1].copy()
        for i in range(len(self.animations[3])):
            self.animations[3][i] = pygame.transform.flip(self.animations[3][i], True, False)

        self.attack_animations = []
        for i in range(7, 9):
            self.attack_animations.append(
                [get_image(pygame.image.load(f'Assets/Characters/player.png'), 48, 48, j * 48, i * 48) for j in
                 range(4)])
        self.attack_animations.append([])
        for i in range(len(self.attack_animations[0])):
            self.attack_animations[-1].append(pygame.transform.flip(self.attack_animations[0][i], True, False))
        self.attack_animations.append(
            [get_image(pygame.image.load(f'Assets/Characters/player.png'), 48, 48, j * 48, 6 * 48) for j in
             range(4)])


        self.is_attacking = False


        self.image = self.animations[0][0]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.curranimation = 3
        self.curr_sprite = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.score = 0

        self.walls = walls

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

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.is_attacking = True

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

    def tint_surface(self, surface, tint_color):
        surface = surface.copy()
        #surface.fill(tint_color, None, pygame.BLEND_RGB_ADD)
        return surface

    def set_monster_group(self, monsters):
        self.monsters = monsters


    def update(self):
        self.input()
        self.move(self.direction.x * self.speed, self.direction.y * self.speed)



        if self.is_attacking and not self.cooldown:
            self.cooldown = True
            if self.collide_with_monsters():
                self.collide_with_monsters().get_damage()
            else:
                for monster in pygame.sprite.spritecollide(self, self.monsters, False):
                    monster.get_damage()



        #animations
        if not self.is_attacking:
            # right
            if self.direction[0] > 0:
                self.curranimation = 1
            # down
            if self.direction[1] > 0:
                self.curranimation = 0
            # up
            if self.direction[0] < 0:
                self.curranimation = 3
            # left
            if self.direction[1] < 0:
                self.curranimation = 2
            if self.direction[0] == 0 and self.direction[1] == 0:
                self.curranimation = 4

            self.curr_sprite += 0.03

            if self.curr_sprite >= len(self.animations[self.curranimation]) - 1:
                self.curr_sprite = 0
            self.image = self.animations[self.curranimation][int(self.curr_sprite)]
        else:

            self.curr_sprite += 0.029
            if self.direction[0] == 0 and self.direction[1] == 0:
                self.curranimation = 0
            else:
                if self.direction[1] < 0:
                    self.curranimation = 1
                elif self.direction[0] > 0:
                    self.curranimation = 0
                elif self.direction[0] < 0:
                    self.curranimation = 2
                else:
                    self.curranimation = 3

            if self.curr_sprite >= len(self.attack_animations[self.curranimation]) - 1:
                self.curr_sprite = 0
                self.is_attacking = False
                self.cooldown = False
            self.image = self.attack_animations[self.curranimation][int(self.curr_sprite)]
        self.mask = pygame.mask.from_surface(self.image)

    # Вот эту д******ю ты делаешь по собственному желанию согласно статье 157 УК РФ
    # погадите что это за статья????
    # Статья 157 УК РФ предусматривает уголовную ответственность за уклонение от уплаты алиментов.
    # все понятно
    # github лучше telegram!!!
    # вот да
    def get_damage(self):


        for animid, animation in enumerate(self.animations):
            for frameid,  frame in enumerate(animation):
                self.animations[animid][frameid] = self.tint_surface(frame, (255, 0, 0))

        for animid, animation in enumerate(self.attack_animations):
            for frameid,  frame in enumerate(animation):
                self.attack_animations[animid][frameid] = self.tint_surface(frame, (255, 0, 0))


        if self.HP != 0:
            pygame.mixer.Sound.play(hit_sound)
            self.HP -= 1


    def collide_with_monsters(self):
        for monster in self.monsters:
            distance = ((self.rect.x - monster.rect.centerx) ** 2 + (self.rect.y - monster.rect.centery) ** 2) ** 0.5
            if distance <= self.radius:
                return monster
        return None