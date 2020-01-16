from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, manhatten_distance, connect_houses,\
    update_battery_location, safe, innit_data
from grid import gridplotter
import random
import json

highscore_file = '../Scores/wijk2_score_advanced2.txt'
housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'

houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)

# place houses and batteries (random), make connections
batteries, houses = innit_data(houseslist, batterieslist, True, {})
batteries, houses, houses_left = connect_houses(batteries, houses)

for i in range(100000):
    batteries = update_battery_location(batteries)
    batteries, houses, houses_left = connect_houses(batteries, houses)
    if i % 10000 == 0:
        print(i)

highest = []
highest_score = 1000

for j in range(100000):
    batteries, houses = innit_data(houseslist, batterieslist, False, batteries)
    batteries, houses, houses_left = connect_houses(batteries, houses)
    if len(houses_left) > 0:
        continue

    result = makejson(batteries)
    score = len(get_all_cables(result))
    if score < highest_score:
        print('in de if bois')
        highest_score = score
        highest = result
        print(highest_score)

    if j % 1000 == 0:
        print(j)

gridplotter(highest)
print(highest_score)

