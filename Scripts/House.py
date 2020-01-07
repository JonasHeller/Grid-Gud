class House():
    def __init__(self, coord, output):
        self.coord = coord
        self.output = output

    def calc_distances(self, batteries):
        self.distances = []
        for battery in batteries:
            self.distances.append(abs(self.coord[0] - battery[0]) + abs(self.coord[1] - battery[1]))
        print(self.distances)

    def __str__(self):
        return str(self.coord) + ',' + str(self.output)