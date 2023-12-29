import pygame


def get_image(sheet, width, hieght, x, y):
    # pygame.SRCALPHA
    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, hieght))
    image = pygame.transform.scale(image, (144, 144))

    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, walls):
        super().__init__(group)
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
        for i in range(7, 11):
            self.attack_animations.append(
                [get_image(pygame.image.load(f'Assets/Characters/player.png'), 48, 48, j * 48, i * 48) for j in
                 range(4)])
        self.is_attacking = False

        self.attack_animations[-1] = self.attack_animations[1].copy()
        for i in range(len(self.attack_animations[3])):
            self.attack_animations[3][i] = pygame.transform.flip(self.attack_animations[3][i], True, False)

        self.image = self.animations[0][0]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 1.2
        self.curranimation = 3
        self.curr_sprite = 0
        self.mask = pygame.mask.from_surface(self.image)

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

    def update(self):
        self.input()
        self.move(self.direction.x * self.speed, self.direction.y * self.speed)

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
            if self.curranimation == 4:
                self.curranimation = 3
            if self.curr_sprite >= len(self.attack_animations[self.curranimation]) - 1:
                self.curr_sprite = 0
                self.is_attacking = False
            self.image = self.attack_animations[self.curranimation][int(self.curr_sprite)]

    # Вот эту дрочильню ты делаешь по собственному желанию согласно статье 157 УК РФ
    def get_damage(self):
        pass
