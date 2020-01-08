import random
from House import House
from Battery import Battery
from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables
from grid import gridplotter

# set path to the datafiles
housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'

# load in data
houses = loadhouse(housespath)
batterijennew = loadbattery(batterypath)

# loop until a random solution has been found
while True:

    # store the batteries in a dictionary with coords as key and class as value
    batterydict = {}
    for battery in batterijennew:
        batterydict[(battery[0], battery[1])] = Battery((battery[0], battery[1]), battery[2])

    # store houses in a dictionary with coords as key an class as value
    housesdict = {}
    for house in houses:

        # clean the data
        temp = house.replace(' ', '').split(',')
        temp = [float(i) for i in temp]
        housesdict[(temp[0], temp[1])] = House((temp[0], temp[1]), temp[2])

    # loop over all batteries
    for battery in batterydict:

        # loop until the capcity of the battery is reached
        while True:

            # try to get a random choice
            try:
                temp = random.choice(list(housesdict.keys()))

            # if no houses left, break from the loop
            except:
                break

            # check if the battery as enough capacity left and add the house
            if batterydict[battery].capacity_check(housesdict[temp]):
                batterydict[battery].add_house(housesdict[temp])

                # remove house from availible houses
                del housesdict[temp]

            # else check if one last house can be added
            else:
                deletelist = []

                # loop over houses left and check if houses can be added
                for houseleft in housesdict:
                    if batterydict[battery].capacity_check(housesdict[houseleft]):

                        # add houses 
                        batterydict[battery].add_house(housesdict[houseleft])
                        deletelist.append(houseleft)
                
                # remove added houses from houses dict and break out of the loop
                for item in deletelist:
                    del housesdict[item]
                break

    # sometimes the houses don't fit in the batteries
    # this tries to shuffle some around

    # get a house that is left
    for item in housesdict:
        house_left = housesdict[item]

        # loop over batteries
        for battery in batterydict:

            # get the capacity needed to add the house to current battery
            most_capacity = batterydict[battery]
            cap_needed = house_left.output - (most_capacity.capacity - most_capacity.currentload)

            # get house with lowest output that, if removed, will allow the house left to be added
            lowest = [100, 1]
            for house in most_capacity.connected_houses:
                if house.output > cap_needed and house.output < lowest[0]:
                    lowest = [house.output, house]

            # check if the house selected above can fit in an other battery
            try:
                for battery in batterydict:

                    # if it fits, add it to the battery, remove it from the current battery
                    # and add the house left to the current battery
                    if batterydict[battery].capacity_check(lowest[1]):
                        batterydict[battery].add_house(lowest[1])
                        most_capacity.remove_house(lowest[1])
                        most_capacity.add_house(house_left)
                        break
            except:
                break

    # if all houses are assigned, stop the loop
    if len(list(housesdict.keys())) == 0:
        break

# get the results in json format
result = makejson(batterydict)

# make the plot
gridplotter(result, batterypath, housespath)

# get the prices
all_cables = get_all_cables(result)
print(f"amount of cables: {len(all_cables)} and the costs: {9 * len(all_cables)}")
