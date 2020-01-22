# NOT USED FOR HIGH SCORES

from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, manhatten_distance, connect_houses,\
    update_battery_location, innit_data, save_highscore
from grid import gridplotter
import random
import json
import copy

highscore_file = '../Scores/wijk3_score_advanced4.txt'
housespath = '../Data/wijk3_huizen.csv'
batterypath = '../Data/wijk3_batterijen.csv'

# load houses and batteries 
houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)

# initialize the data
batteries, houses = innit_data(houseslist, batterieslist, True, {})

highest = []
highest_score = 1000
for i in range(10000):
    batteries, houses = innit_data(houseslist, batterieslist, False, batteries)
    batteries, houses, houses_left = connect_houses(batteries, houses)

    if len(houses_left) > 0:
            continue

    result = makejson(batteries)
    score = len(get_all_cables(result))
    if score < highest_score:
        highest_score = score
        highest = result
        print(f'NEW HIGHEST SCORE: {highest_score} at loop {i}')
        best = copy.deepcopy(batteries)

print(highest_score)
batteries = best


for i in range(100):
    batteries_new = update_battery_location(batteries)
    result = makejson(batteries_new)
    score = len(get_all_cables(result))

    if score > highest_score:
        batteries = batteries_new
        highest_score = score
        highest = result
    

    j = 0
    while True:
        batteries, houses = innit_data(houseslist, batterieslist, False, batteries)
        batteries, houses, houses_left = connect_houses(batteries, houses)
        if len(houses_left) > 0:
            continue

        result = makejson(batteries)
        score = len(get_all_cables(result))
        if score < highest_score:
            highest_score = score
            highest = result
            print(f'NEW HIGHEST SCORE: {highest_score} at loop {i}')
            best = copy.deepcopy(batteries)
            break
        j += 1
        if j == 100000:
            print('no better found, exiting')
            break
    if j == 100000:
        break
    batteries = best


gridplotter(highest)
save_highscore(highscore_file, highest)