# NOT USED FOR HIGH SCORES

from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, manhatten_distance, connect_houses,\
    update_battery_location, safe, innit_data
from grid import gridplotter
import random
import json

housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'

# load batteries and houses from files
houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)

# place houses and batteries (random), make connections
batteries, houses = innit_data(houseslist, batterieslist, True, {})
batteries, houses, houses_left = connect_houses(batteries, houses)

# get battery setup
for i in range(100000):
    batteries = update_battery_location(batteries)
    batteries, houses, houses_left = connect_houses(batteries, houses)
    if i % 10000 == 0:
        print(i)

highest = []
highest_score = 1000

# update battery location 100000 times
for j in range(100000):

    # load batteries dict and houses list, and connect them
    batteries, houses = innit_data(houseslist, batterieslist, False, batteries)
    batteries, houses, houses_left = connect_houses(batteries, houses)

    # if houses don't fit, continue with next loop and try again
    if len(houses_left) > 0:
        continue

    # make paths and get score
    result = makejson(batteries)
    score = len(get_all_cables(result))

    # check for highest score
    if score < highest_score:
        highest_score = score
        highest = result
        print(highest_score)

    # give update to user every 1000 loops
    if j % 1000 == 0:
        print(j)

# show plot
gridplotter(highest)
print(highest_score)

