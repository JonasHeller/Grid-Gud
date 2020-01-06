import re
import random

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


with open('../Data/wijk1_huizen.csv', 'r') as f:
    lines = f.read()
    houses = lines.split('\n')
    del houses[0]
    del houses[-1]

housesdict = {}
for house in houses:
    temp = house.replace(' ', '').split(',')
    temp = [float(i) for i in temp]
    
    housesdict[(temp[0], temp[1])] = House((temp[0], temp[1]), temp[2])

with open('../Data/wijk1_batterijen.csv', 'r') as f:
    lines = f.read()
    batterijen = lines.split('\n')
    del batterijen[0]
    del batterijen[-1]
    batterijennew = []
    for batterij in batterijen:
        batterij = re.findall(r'\d+', batterij)
        batterijennew.append([int(batterij[0]), int(batterij[1]), float(batterij[2] + '.' + batterij[3])])


batterydict = {}
for battery in batterijennew:
    batterydict[(battery[0], battery[1])] = Battery((battery[0], battery[1]), battery[2])

for battery in batterydict:
    while True:
        try:
            temp = random.choice(list(housesdict.keys()))
        except:
            break
        if batterydict[battery].capacity_check(housesdict[temp]):
            batterydict[battery].add_house(housesdict[temp])
            del housesdict[temp]
        else:
            deletelist = []
            for houseleft in housesdict:
                if batterydict[battery].capacity_check(housesdict[houseleft]):
                    batterydict[battery].add_house(housesdict[houseleft])
                    deletelist.append(houseleft)
            for item in deletelist:
                del housesdict[item]
            break

for item in batterydict:
    print(batterydict[item])
try:
    print(housesdict[next(iter(housesdict))])
except:
    print('none left')

print('________________________')

for item in housesdict:
    house_left = housesdict[item]

    # biggest means most capacity left
    for battery in batterydict:
        most_capacity = batterydict[battery]
        cap_needed = house_left.output - (most_capacity.capacity - most_capacity.currentload)
        print('BATTERY:', most_capacity)
        print('CAP_NEEDED:', cap_needed)

        lowest = [100, 1]
        for house in most_capacity.connected_houses:
            if house.output > cap_needed and house.output < lowest[0]:
                lowest = [house.output, house]
        print('LOWEST', lowest)

        try:
            for battery in batterydict:
                if batterydict[battery].capacity_check(lowest[1]):
                    print('eyo we zijn hier')
                    batterydict[battery].add_house(lowest[1])
                    most_capacity.remove_house(lowest[1])
                    most_capacity.add_house(house_left)
                    del housesdict[item]
                    print('break 1')
                    break
        except:
            print('break 2')
            break


print('_______________________')
for item in batterydict:
    print(batterydict[item])
try:
    print(housesdict[next(iter(housesdict))])
except:
    print('none left')

