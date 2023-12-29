import csv
import random



class MapGenerator:



    def __init__(self, size):
        self.size = size
        self.map = [[-1 for _ in range(size)] for _ in range(size)]



    def load_csv(self, path) -> list:
        path = "Assets/MapBites/" + path
        loaded = []
        with open(path, encoding='utf8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for _, row in enumerate(reader):
                loaded.append([int(el) for el in row])
            return loaded

    def place_room(self, room_array, x, y):
        if x + len(room_array) > len(self.map) or y + len(room_array[0]) > len(self.map[0]):
            raise ValueError("Room does not fit at the given coordinates")

        for i in range(len(room_array)):
            for j in range(len(room_array[i])):
                self.map[y + i][x + j] = room_array[i][j]

    def is_space_free(self, room, position):
        room_height = len(room)
        room_width = len(room[0]) if room_height > 0 else 0

        for i in range(room_height):
            for j in range(room_width):
                if (position[0] + i >= len(self.map) or
                        position[1] + j >= len(self.map[0]) or
                        self.map[position[0] + i][position[1] + j] != -1):
                    return False
        return True

    def can_fit_8x8_room(self, start_row, start_col, direction):
        rows = len(self.map)
        cols = len(self.map[0]) if rows > 0 else 0
        room_size = 8

        # Check if the room fits in the specified direction
        if direction == "top":
            if start_row - room_size + 1 < 0:
                return False
            for i in range(start_row, start_row - room_size, -1):
                for j in range(start_col, min(cols, start_col + room_size)):
                    if self.map[i][j] != -1:
                        return False

        elif direction == "bottom":
            if start_row + room_size > rows:
                return False
            for i in range(start_row, start_row + room_size):
                for j in range(start_col, min(cols, start_col + room_size)):
                    if self.map[i][j] != -1:
                        return False

        elif direction == "left":
            if start_col - room_size + 1 < 0:
                return False
            for i in range(start_row, min(rows, start_row + room_size)):
                for j in range(start_col, start_col - room_size, -1):
                    if self.map[i][j] != -1:
                        return False

        elif direction == "right":
            if start_col + room_size > cols:
                return False
            for i in range(start_row, min(rows, start_row + room_size)):
                for j in range(start_col, start_col + room_size):
                    if self.map[i][j] != -1:
                        return False

        else:
            raise ValueError("Invalid direction specified")

        return True

    def place_tunel(self, dir, sx, sy, ex, ey):
        horiz_room = [
            [2],
            [11],
            [21],
            [21],
            [21],
            [21],
            [21],
            [41],
        ]
        vert_room = [
            [20, 11, 11, 11, 11, 11, 11, 35]
        ]
        if dir == "horiz":
            for i in range(abs(ex - sx)):
                self.place_room(horiz_room, sx + i, sy)
        else:
            for i in range(abs(ey - sy)):
                self.place_room(vert_room, sx, sy + i)



    def saveMap(self, name) -> None:
        with open(f"{name}.csv", mode='w') as f:
            for el in self.map:
                print(*el, file=f, sep=',')

    def generate(self, amount, start_room_csv, rooms_as_csv):
        rooms = [self.load_csv(el) for el in rooms_as_csv]
        start_room = self.load_csv(start_room_csv)

        # Place the starting room
        self.place_room(start_room, self.size // 2, self.size // 2)
        self.prev_room = [start_room, self.size // 2, self.size // 2]
        self.prev_dir = ''


        while amount > 0:
            chosen_room = rooms[0]# Select a random room
            directions = ['top', 'bottom', 'left', 'right']
            opposite_dir = {
                "left": "right",
                "right": "left",
                "top": "bottom",
                "bottom": "top"
            }
            dir = random.choice(directions)
            while opposite_dir.get(dir, "") == self.prev_dir:
                dir = random.choice(directions)
            self.prev_dir = dir


            nx, ny = 0, 0
            tunnel_length = 4

            if dir == 'right':
                nx = self.prev_room[1] + tunnel_length + 7
                ny = self.prev_room[2]

                self.place_room(chosen_room, nx, ny)
                self.place_tunel("horiz", self.prev_room[1] + 7, self.prev_room[2], nx + 1, ny)

            elif dir == 'left':
                nx = self.prev_room[1] - tunnel_length - 7
                ny = self.prev_room[2]

                self.place_room(chosen_room, nx, ny)
                self.place_tunel("horiz", nx + 7, ny, self.prev_room[1] + 1, self.prev_room[2])


            elif dir == 'top':
                nx = self.prev_room[1]
                ny = self.prev_room[2] - tunnel_length - 7

                self.place_room(chosen_room, nx, ny)
                self.place_tunel("vert", nx, ny + 7, self.prev_room[1], self.prev_room[2] + 1)


            elif dir == 'bottom':
                nx = self.prev_room[1]
                ny = self.prev_room[2] + tunnel_length + 7

                self.place_room(chosen_room, nx, ny)
                self.place_tunel("vert", self.prev_room[1], self.prev_room[2] - 1, nx, ny + 1)


            print(self.can_fit_8x8_room(self.prev_room[1], self.prev_room[2], dir))
            self.saveMap(amount)
            self.prev_room = [chosen_room, nx, ny]
            amount -= 1
