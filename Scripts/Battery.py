class Battery():
    def __init__(self, coord, capacity):
        self.coord = coord
        self.capacity = capacity
        self.currentload = 0
        self.connected_houses = []

    def add_house(self, house):
        self.connected_houses.append(house)
        self.currentload += house.output

    def remove_house(self, house):
        self.connected_houses.remove(house)
        self.currentload -= house.output
    
    def capacity_check(self, house):
        if self.currentload + house.output > self.capacity:
            return False
        else:
            return True
    
    def __str__(self):
        return str(self.coord) + ', ' + str(self.capacity) + ', ' + str(self.currentload) + ', ' + str(len(self.connected_houses))