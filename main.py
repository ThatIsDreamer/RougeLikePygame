import pygame
import GenerateMap
import Player




#Григойда
#изображение с частями карты
tile_image = pygame.image.load("Assets/Tiles/Dungeon_Tileset.png")

#функция для обрезки изображения
def get_image(sheet, width, height, x, y):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(image, (64, 64))
    return image

#класс квадрат
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)





if __name__ == "__main__":
    pygame.init()

    #штуки pygame БАЗА
    tile_group = pygame.sprite.Group()
    size = w, h = 1280, 1000
    screen = pygame.display.set_mode(size)
    screen.fill("white")



    #КОДЫ ОБОЗНАЧАЮЩИЕ КВАДРАТЫ СО СТЕНОЙ
    wall_tiles = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 41, 42, 43, 44, 45, 35, 25, 15]

    #подгрузка всех квадратиков
    tilesarr = []
    for i in range(10):
        temp = []
        for j in range(10):
            temp.append(get_image(tile_image, 16, 16, 16 * j, 16 * i))
        tilesarr.append(temp)

    #генерация рандномной карты -> все в файле GenerateMap.py
    test = GenerateMap.TileMap("test", 64)
    tiles = test.GenerateMap(5)

    #!!!!!ВАЖНО группа со всеми спрайтам все что будет появлятся на экране во время игры добовлять сюда
    all_sprites = pygame.sprite.Group()

    #Группа со стенами для обработки столконовений везде с чем есть есть колизия добавлять сюда
    walls = pygame.sprite.Group()

    #Проход по списку с картой можешь ишнорировать артем
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

    #инцилизация класса PLAYER из файла Player.py
    player = Player.Player((200, 200), all_sprites, walls)
    all_sprites.add(player)

    clock = pygame.time.Clock()
    running = True
    FPS = 30
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        # вот как раз обновление всех спрайтов и их отрисовка
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()

    pygame.display.flip()
    clock.tick(FPS)

    pygame.quit()
