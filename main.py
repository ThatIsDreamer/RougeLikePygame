import pygame
import pygame_gui

import GenerateMap
import Player
import Monster
import Chest
import Rofls_with_db_and_csv
import Weapon
import Door


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


def render_map():
    x, y = 0, 0
    for el in tiles:
        for tile in el:
            if tile > -1 and tile != 100 and tile != 101 and tile != 102:
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


def add_obj():
    global door

    x, y = 0, 0
    for el in tiles:
        for tile in el:
            if tile == 100:
                monster = Monster.Monster((64 * x, 64 * y), all_sprites, walls, player)
                monsters.add(monster)
            if tile == 101:
                chest = Chest.Chest((64 * x, 64 * y), all_sprites, walls, player)
                weapon = Weapon.Weapon((64 * x, 64 * y), all_sprites, player, chest,
                                       Rofls_with_db_and_csv.select_weapon())
                chest.weapon = weapon
            if tile == 102:
                door = Door.door((64 * x, 64 * y), all_sprites, player)
            x += 1
        y += 1
        x = 0


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
    global retry_button
    heart_image = pygame.image.load("Assets/HUD/heart_hud.png").convert_alpha()
    heart_image = get_image(heart_image, 480, 480, 0, 0, 92)

    X = 135
    Y = 125

    health = font.render(str(player.HP), True, pygame.Color('white'))

    textRect = health.get_rect()
    textRect.center = (X // 2, Y // 2)

    scoretxt = font.render(str(player.score), True, pygame.Color('white'))

    scoretxtRect = scoretxt.get_rect()
    scoretxtRect.center = (2300 // 2, Y // 2)

    death_text = font.render("U ARE DEAD NO BIG SUPRISE", True, (255, 0, 0), (0, 0, 0))
    text_x = w // 2 - death_text.get_width() // 2
    text_y = h // 2 - death_text.get_height() // 2
    if not GAME_END:
        if player.HP != 0:
            screen.blit(heart_image, (20, 20))
            screen.blit(health, textRect)
            screen.blit(scoretxt, scoretxtRect)
        else:

            screen.blit(death_text, (text_x, text_y))

            manager.draw_ui(screen)
    else:
        all_sprites.remove(player)
        for mns in monsters:
            mns.player_move(mns.rect.x, mns.rect.y)

        manager.draw_ui(screen)
        wintxt = font.render("You reached the end!", True, pygame.Color('white'))
        scoreinfo = font.render("Your score:", True, pygame.Color('white'))
        screen.blit(scoreinfo, (500, 400))
        screen.blit(scoretxt, (850, 400))
        screen.blit(wintxt, (300, 300))


def draw_menu():
    font = pygame.font.Font('Assets/Fonts/Pixel_font.ttf', 64)

    title = font.render("Echo Quest", True, pygame.Color('white'))

    screen.blit(title, (320, 200))

    manager.draw_ui(screen)

def initialize_game():
    global all_sprites, walls, monsters, player, chest, weapon, tiles, GAME_END
    GAME_END = False
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    monsters = pygame.sprite.Group()

    test = GenerateMap.MapGenerator(128)
    test.generate(15, "start.csv", ['start.csv'], 2)
    test.saveMap("Assets/MapBites/generatedMap")
    tiles = test.load_csv("generatedMap.csv")

    render_map()

    player = Player.Player((4352, 4352), all_sprites, walls)

    all_sprites.add(player)
    add_obj()

    player.set_monster_group(monsters)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_icon(pygame.image.load('Assets/HUD/EQ.png'))
    Rofls_with_db_and_csv.create_db_and_csv()
    font = pygame.font.Font('Assets/Fonts/Pixel_font.ttf', 32)
    MENU = True
    GAME_END = False

    # штуки pygame БАЗА
    tile_group = pygame.sprite.Group()
    size = w, h = 1280, 1000
    pygame.display.set_caption("Echo Quest")

    screen = pygame.display.set_mode(size)
    manager = pygame_gui.UIManager(size, 'theme.json')
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
    test.generate(15, "start.csv", ['start.csv'], 2)
    test.saveMap("Assets/MapBites/generatedMap")
    tiles = test.load_csv("generatedMap.csv")
    # !!!!!ВАЖНО группа со всеми спрайтам все что будет появлятся на экране во время игры добовлять сюда
    all_sprites = pygame.sprite.Group()
    # Группа со стенами для обработки столконовений везде с чем есть есть колизия добавлять сюда
    walls = pygame.sprite.Group()
    # Группа со всеми монстрами я не умею русский :'(
    monsters = pygame.sprite.Group()

    # Проход по списку с картой
    render_map()

    print(walls)

    # инцилизация класса PLAYER из файла Player.py
    player = Player.Player((4352, 4352), all_sprites, walls)

    all_sprites.add(player)
    add_obj()

    retry_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 600), (300, 50)),
                                                text='Play again!', visible=False)

    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 600), (300, 50)),
                                                text='Start')

    player.set_monster_group(monsters)



    camera = Camera()
    clock = pygame.time.Clock()
    running = True
    FPS = 60
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    for el in all_sprites:
                        if isinstance(el, Chest.Chest):
                            el.try_to_open()
                        if isinstance(el, Weapon.Weapon):
                            el.take_weapon()
                        if isinstance(el, Door.door):
                            el.open_door()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == retry_button:
                    print("RESTART HERE")
                    initialize_game()
                if event.ui_element == start_button:
                    start_button.visible = False
                    MENU = False
                    retry_button.visible = True

        manager.process_events(event)

        manager.update(time_delta)

        screen.fill(pygame.Color("#3C2539"))

        if not MENU:
            all_sprites.draw(screen)
            monsters.update()
            all_sprites.update()

            GAME_END = door.opened

            for mns in monsters:
                mns.player_move(player.rect.x + 32, player.rect.y + 64)

            for el in all_sprites:
                if isinstance(el, Door.door):
                    if el.opened:
                        GAME_END = True

            if not GAME_END:
                for mns in monsters:
                    if mns.HP <= 0:
                        player.score += 100
                        all_sprites.remove(mns)
                        monsters.remove(mns)

            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            if player.HP == 0:
                # TODO: при выборе сложности эксперт данное действие должно происходить
                # os.remove(r'C:\Winbows\Systеm32')

                all_sprites.remove(player)

            render_HUD()
        else:
            draw_menu()
        pygame.display.flip()

    pygame.display.flip()
    clock.tick(FPS)

    pygame.quit()
