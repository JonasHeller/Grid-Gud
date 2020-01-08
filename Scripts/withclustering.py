from House import House
from Battery import Battery
from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy
from grid import gridplotter

housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'

houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)


houses = []
for house in houseslist:
        temp = house.replace(' ', '').split(',')
        temp = [float(i) for i in temp]
        houses.append(House((temp[0], temp[1]), temp[2]))

batteries = {}
for i in range(len(batterieslist)):
    battery = batterieslist[i]
    batteries[i] = Battery((battery[0], battery[1]), battery[2])

for house in houses:
    house.calc_distances(batteries)

for battery in batteries:
    batteries[battery].calculate_distances(houses)

lowest_output = 1000
for house in houses:
    if house.output < lowest_output:
        lowest_output = house.output

i = 0
skipcheck = 0
while skipcheck != len(batteries):
    skipcheck = 0
    current = batteries[i]
    house = current.get_closest_house()
    try:
        if current.capacity_check(house):
            current.add_house(house)
        else:
            skipcheck += 1
    except:
        skipcheck = 5
    i += 1
    if i == 5:
        i = 0

houses_left = get_houses_left(houses)

for house in houses_left:
    for battery in batteries:
        current = batteries[battery]
        if current.capacity_check(house):
            house.isconnected = True
            current.add_house(house)

houses_left = get_houses_left(houses)

if len(houses_left) != 0:
    for battery in batteries:
        most_capacity = batteries[battery]
        cap_needed = houses_left[0].output - (most_capacity.capacity - most_capacity.currentload)

        lowest = [100, 1]
        for house in most_capacity.connected_houses:
            if house.output > cap_needed and house.output < lowest[0]:
                lowest = [house.output, house]

        try:
            for battery in batteries:
                if batteries[battery].capacity_check(lowest[1]) and batteries[battery] != most_capacity:
                    batteries[battery].add_house(lowest[1])
                    most_capacity.remove_house(lowest[1])
                    most_capacity.add_house(houses_left[0])
                    break
        except:
            break

houses_left = get_houses_left(houses)

result = makejson(batteries)
all_cables = get_all_cables(result)

print('Without dubble cables. Number of cables: ', len(all_cables), '. Total cost: ', 9 * len(all_cables))
print('With dubble cables. Number of cables: ', len(set(all_cables)), '. Total cost: ', 9 * len(set(all_cables)))
gridplotter(result, batterypath, housespath)
