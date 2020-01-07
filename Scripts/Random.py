import random
from House import House
from Battery import Battery
from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables
from grid import gridplotter

houses = loadhouse('../Data/wijk1_huizen.csv')
batterijennew = loadbattery('../Data/wijk1_batterijen.csv')

while True:
    batterydict = {}
    for battery in batterijennew:
        batterydict[(battery[0], battery[1])] = Battery((battery[0], battery[1]), battery[2])

    housesdict = {}
    for house in houses:
        temp = house.replace(' ', '').split(',')
        temp = [float(i) for i in temp]

        housesdict[(temp[0], temp[1])] = House((temp[0], temp[1]), temp[2])

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

    for item in housesdict:
        house_left = housesdict[item]

        # biggest means most capacity left
        for battery in batterydict:
            most_capacity = batterydict[battery]
            cap_needed = house_left.output - (most_capacity.capacity - most_capacity.currentload)

            lowest = [100, 1]
            for house in most_capacity.connected_houses:
                if house.output > cap_needed and house.output < lowest[0]:
                    lowest = [house.output, house]

            try:
                for battery in batterydict:
                    if batterydict[battery].capacity_check(lowest[1]):
                        batterydict[battery].add_house(lowest[1])
                        most_capacity.remove_house(lowest[1])
                        most_capacity.add_house(house_left)
                        break
            except:
                break
    if len(list(housesdict.keys())) == 0:
        break

result = makejson(batterydict)
pp.pprint(result)

gridplotter(result)

all_cables = get_all_cables(result)
print(f"amount of cables: {len(all_cables)} and the costs: {9 * len(all_cables)}")
