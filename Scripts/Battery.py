class Battery():
    def __init__(self, coord, capacity):
        self.coord = coord
        self.capacity = capacity
        self.currentload = 0
        self.connected_houses = []

    def add_house(self, house):
        self.connected_houses.append(house)
        self.currentload += house.output
        house.isconnected = True

    def remove_house(self, house):
        self.connected_houses.remove(house)
        self.currentload -= house.output
    
    def capacity_check(self, house):
        if self.currentload + house.output > self.capacity:
            return False
        else:
            return True

    def calculate_distances(self, houses):
        self.distances = []
        for house in houses:
            self.distances.append((abs(self.coord[0] - house.coord[0]) + abs(self.coord[1] - house.coord[1]), house))
        self.distances.sort(key=lambda tup: tup[0])

    def get_closest_house(self):
        for house in self.distances:
            if house[1].isconnected == True:
                self.distances.remove(house)
            else:
                return house[1]
    
    def __str__(self):
        return str(self.coord) + ', ' + str(self.capacity) + ', ' + str(self.currentload) + ', ' + str(len(self.connected_houses))