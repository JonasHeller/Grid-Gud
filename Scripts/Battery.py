class Battery():
    def __init__(self, coord, capacity):
        self.coord = coord
        self.capacity = capacity
        self.currentload = 0
        self.connected_houses = []

    def add_house(self, house):

        # add house to connected houses list and flag house as connected
        self.connected_houses.append(house)
        self.currentload += house.output
        house.isconnected = True

    def remove_house(self, house):

        # remove house form connected houses list and flag house as disconnected
        self.connected_houses.remove(house)
        self.currentload -= house.output
        house.isconnected = False
    
    def capacity_check(self, house):

        # check if house can be connected
        if self.currentload + house.output > self.capacity:
            return False
        else:
            return True

    def calculate_distances(self, houses):
        self.distances = []

        # looop over houses
        for house in houses:

            # calculate manhattan distance to houses
            self.distances.append((abs(self.coord[0] - house.coord[0]) + abs(self.coord[1] - house.coord[1]), house))
        
        # sort houses on distance
        self.distances.sort(key=lambda tup: tup[0])

    def get_closest_house(self):

        # get closest house that is not connected
        for house in self.distances:
            if house[1].isconnected == True:

                # if battery is connected, remove it from the list
                # this makes the loops shorter on every iteration
                self.distances.remove(house)
            else:
                return house[1]
    
    def __str__(self):
        return str(self.coord) + ', ' + str(self.capacity) + ', ' + str(self.currentload) + ', ' + str(len(self.connected_houses))