from House import House
from Battery import Battery
from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, switchoutliers
from grid import gridplotter
import random

# set paths to data files
housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'

# load in data
houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)
scores = []
highest_score = 1000
highest = []
for attempt in range(1000):
    # load houses object in a list
    houses = []
    for house in houseslist:

        # clean up data
        temp = house.replace(' ', '').split(',')
        temp = [float(i) for i in temp]
        houses.append(House((temp[0], temp[1]), temp[2]))

    # load batteries in a dict with index as key and object as value
    batteries = {}
    for i in range(len(batterieslist)):
        battery = batterieslist[i]
        batteries[i] = Battery((battery[0], battery[1]), battery[2], i)

    # calculate distances to all batteries form houses
    for house in houses:
        house.calc_distances(batteries)

    # calculate all distances to houses from batteries
    for battery in batteries:
        batteries[battery].calculate_distances(houses)

    # let batteries choose its closest house in turn
    # i = 0
    skipcheck = 0
    while skipcheck != len(batteries):

        # set current to current batteries object
        current = batteries[random.choice(list(batteries.keys()))]

        # get closest house to current
        house = current.get_closest_house()

        # try to add it to the house
        try:
            if current.capacity_check(house):
                current.add_house(house)
                skipcheck = 0
            else:
                skipcheck += 1
        except:
            skipcheck = 5

        # update the index for next battery
        # i += 1
        # if i == 5:
        #     i = 0

    # get all houses not assigned
    houses_left = get_houses_left(houses)

    # loop for all houses in houses left
    for house in houses_left:

        # loop for batteries
        for battery in batteries:
            current = batteries[battery]

            # check if house can still be added to battery
            if current.capacity_check(house):
                house.isconnected = True
                current.add_house(house)

    # update houses left
    houses_left = get_houses_left(houses)

    # if houses left is not empty, check if some houses can be shuffled to add last house
    if len(houses_left) != 0:

        # loop over all batteries
        for battery in batteries:

            # calculate the capacity needed
            most_capacity = batteries[battery]
            cap_needed = houses_left[0].output - (most_capacity.capacity - most_capacity.currentload)

            # get house with lowest output that, if removed, will allow the house left to be added
            lowest = [100, 1]
            for house in most_capacity.connected_houses:
                if house.output > cap_needed and house.output < lowest[0]:
                    lowest = [house.output, house]

            # check if the house selected above can fit in an other battery
            try:
                for battery in batteries:
                    # if it fits, add it to the battery, remove it from the current battery
                    # and add the house left to the current battery
                    if batteries[battery].capacity_check(lowest[1]) and batteries[battery] != most_capacity:
                        batteries[battery].add_house(lowest[1])
                        most_capacity.remove_house(lowest[1])
                        most_capacity.add_house(houses_left[0])
                        break
            except:
                break

    # update houses left
    houses_left = get_houses_left(houses)
    if len(houses_left) > 0:
        continue

    outliers = get_outliers(batteries)
    #switchoutliers(outliers, houses, batteries)

    # get results in json format
    result = makejson(batteries)

    # calculate number of cables
    all_cables = get_all_cables(result)

    print(f'With dubble cables, loop {attempt}. Number of cables: {len(all_cables)}. Total cost: {9 * len(all_cables)}')
    #gridplotter(result, batterypath, housespath)
    scores.append(len(all_cables))

    if len(all_cables) < highest_score:
        highest_score = len(all_cables)
        highest = result

print(sorted(scores))
gridplotter(highest, batterypath, housespath)
