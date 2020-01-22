from House import House
from Battery import Battery
from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, manhatten_distance, connect_houses, \
    connect_houses_from_houses, save_highscore, scores_plot
from grid import gridplotter
import random
import json

# set paths to data files
highscore_file = '../Data/wijk3_score.txt'
housespath = '../Data/wijk3_huizen.csv'
batterypath = '../Data/wijk3_batterijen.csv'

# load in data
houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)
scores = []
highest_score = 1000
highest = []
attempt = 0

for i in range(1000):
    attempt += 1
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

    #batteries, houses, houses_left = connect_houses(batteries, houses)
    batteries, houses, houses_left = connect_houses(batteries, houses)
    if len(houses_left) > 0:
        continue

    # get results in json format
    result = makejson(batteries)

    # calculate number of cables
    all_cables = get_all_cables(result)


    #gridplotter(result, batterypath, housespath)
    scores.append(len(all_cables))

    if len(all_cables) < highest_score:
        #get_outliers(batteries)
        print(f'With double cables, loop {attempt}. Number of cables: {len(all_cables)}. Total cost: {9 * len(all_cables)}')
        highest_score = len(all_cables)
        highest = result
    if int(attempt % 10000) == 0:
        print(attempt)

print(sorted(scores))

gridplotter(highest)

save_highscore(highscore_file, highest)

scores_plot(scores)