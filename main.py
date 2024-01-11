import pygame
import os
import GenerateMap
import Player
import Monster
import Chest


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - w // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - h // 2)


# изображение с частями карты
tile_image = pygame.image.load("Assets/Tiles/Dungeon_Tileset.png")


# функция для обрезки изображения
def get_image(sheet, width, height, x, y, scale=64):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(image, (scale, scale))
    return image


# класс квадрат
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

def render_HUD():

    heart_image = pygame.image.load("Assets/HUD/heart_hud.png").convert_alpha()
    heart_image = get_image(heart_image, 480, 480, 0, 0, 92)

    X = 135
    Y = 125
    font = pygame.font.Font('Assets/Fonts/Pixel_font.ttf', 32)
    health = font.render(str(player.HP), True, pygame.Color('white'))

    textRect = health.get_rect()
    textRect.center = (X // 2, Y // 2)


    death_text = font.render("U ARE DEAD NO BIG SUPRISE", True, (255, 0, 0), (0, 0, 0))
    text_x = w // 2 - death_text.get_width() // 2
    text_y = h // 2 - death_text.get_height() // 2

    if player.HP != 0:
        screen.blit(heart_image, (20, 20))
        screen.blit(health, textRect)
    else:
        screen.blit(death_text, (text_x, text_y))

if __name__ == "__main__":
    pygame.init()


    # штуки pygame БАЗА
    tile_group = pygame.sprite.Group()
    size = w, h = 1280, 1000
    screen = pygame.display.set_mode(size)
    screen.fill("white")

    # КОДЫ ОБОЗНАЧАЮЩИЕ КВАДРАТЫ СО СТЕНОЙ
    wall_tiles = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 41, 42, 43, 44, 45, 35, 25, 15]

    # подгрузка всех квадратиков
    tilesarr = []
    for i in range(10):
        temp = []
        for j in range(10):
            temp.append(get_image(tile_image, 16, 16, 16 * j, 16 * i))
        tilesarr.append(temp)

    # генерация рандномной карты -> все в файле GenerateMap.py
    test = GenerateMap.MapGenerator(128)
    test.generate(15, "start.csv", ['start.csv'])
    test.saveMap("Assets/MapBites/generatedMap")
    tiles = test.load_csv("generatedMap.csv")
    # !!!!!ВАЖНО группа со всеми спрайтам все что будет появлятся на экране во время игры добовлять сюда
    all_sprites = pygame.sprite.Group()
    # Группа со стенами для обработки столконовений везде с чем есть есть колизия добавлять сюда
    walls = pygame.sprite.Group()
    #Группа со всеми монстрами я не умею русский :'(
    monsters = pygame.sprite.Group()


    # Проход по списку с картой
    x, y = 0, 0
    for el in tiles:
        for tile in el:
            if tile > -1:
                i, j = 0, 0
                if tile > 9:
                    i, j = int(str(tile)[0]), int(str(tile)[1])
                else:
                    j = tile
                if tile != 78:
                    new_tile = Tile(tilesarr[i][j], (64 * x, 64 * y))
                else:
                    new_tile = Tile(tilesarr[2][3], (64 * x, 64 * y))
                tile_group.add(new_tile)
                all_sprites.add(new_tile)
                if tile in wall_tiles:
                    walls.add(new_tile)

            x += 1
        y += 1
        x = 0
    print(walls)

    # инцилизация класса PLAYER из файла Player.py
    player = Player.Player((4352, 4352), all_sprites, walls)
    monster = Monster.Monster((4452, 4352), all_sprites, walls, player)
    chest = Chest.Chest((4402, 4302), all_sprites, walls, player)



    all_sprites.add(player)
    all_sprites.add(monster)
    monsters.add(monster)

    player.set_monster_group(monsters)

    camera = Camera()
    clock = pygame.time.Clock()
    running = True
    FPS = 60
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    chest.try_to_open()

        screen.fill(pygame.Color("#3C2539"))
        # вот как раз обновление всех спрайтов и их отрисовка
        all_sprites.update()
        all_sprites.draw(screen)
        monster.player_move(player.rect.x + 32, player.rect.y + 64)

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        for mns in monsters:
            if mns.HP <= 0:
                player.score += 100
                all_sprites.remove(mns)
                monsters.remove(mns)
            print(mns.HP)


        if player.HP == 0:
            # TODO: при выборе сложности эксперт данное действие должно происходить
            # os.remove(r'C:\Winbows\Systеm32')

            all_sprites.remove(player)

        render_HUD()

        pygame.display.flip()
    pygame.display.flip()
    clock.tick(FPS)

    pygame.quit()
