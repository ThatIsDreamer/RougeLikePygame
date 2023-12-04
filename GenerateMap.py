import csv


class TileMap:
    def __init__(self, name, size, cnnnum=78):
        self.name = name
        self.size = size
        self.Tmap = [[-1 for i in range(size)] for i in range(size)]
        self.CONNECTIONNUMBER = cnnnum

    #сохроняет карту в файл csv  для дальнейшого использования
    def saveMap(self) -> None:
        with open(f"{self.name}.csv", mode='w') as f:
            for el in self.Tmap:
                print(*el, file=f, sep=',')

    def PlaceRoom(self, room_array, x, y):
        if x + len(room_array) > len(self.Tmap) or y + len(room_array[0]) > len(self.Tmap[0]):
            raise ValueError("Room does not fit at the given coordinates")

        # Place the room on the map
        for i in range(len(room_array)):
            for j in range(len(room_array[i])):
                self.Tmap[x + i][y + j] = room_array[i][j]

    def LoadCSV(self, path) -> list:
        loaded = []
        with open(path, encoding='utf8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for _, row in enumerate(reader):
                loaded.append([int(el) for el in row])
            return loaded

    def GetOpeningsCount(self) -> int:
        count = 0
        for el in self.Tmap:
            count += el.count(self.CONNECTIONNUMBER)
        return count // 6

    def GetFirstOpening(self):
        x, y = -1, -1
        found = False
        for i in range(len(self.Tmap)):
            for j in range(len(self.Tmap)):
                if self.Tmap[i][j] == self.CONNECTIONNUMBER:
                    y, x = j, i
                    found = True
            if found:
                break

        direction = None
        if y + 1 <= len(self.Tmap):
            if self.Tmap[y + 1][x] == self.CONNECTIONNUMBER:
                direction = "vertical"
            else:
                direction = "horizontal"

        return x, y, direction



    def GenerateMap(self, amount):
        #placing the start room
        self.PlaceRoom(self.LoadCSV("Assets/MapBites/start.csv"), 0,  0)
        print(self.GetOpeningsCount())
        for i in range(amount - 1):
            x, y, _ = self.GetFirstOpening()
            self.PlaceRoom(self.LoadCSV("Assets/MapBites/1.csv"), x - 1, y + 1)
        self.saveMap()
        return self.Tmap



test = TileMap("test", 32)
test.GenerateMap(4)

