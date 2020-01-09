class House():
    def __init__(self, coord, output):
        self.coord = coord
        self.output = output
        self.isconnected = False
        self.batteryconnected = None

    def calc_distances(self, batteries):
        self.distances = {}
        for i in batteries:
            battery = batteries[i].coord
            self.distances[i] = abs(self.coord[0] - battery[0]) + abs(self.coord[1] - battery[1])

    def __str__(self):
        return str(self.coord) + ',' + str(self.output)