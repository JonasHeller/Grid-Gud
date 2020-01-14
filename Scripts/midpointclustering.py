from House import House
from Battery import Battery
from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, switchoutliers, manhatten_distance, connect_houses,\
    update_battery_location    
from grid import gridplotter
import random
import json

def innit_data(houseslist, batterieslist, rand, batteries):
    houses = []
    for house in houseslist:

        # clean up data
        temp = house.replace(' ', '').split(',')
        temp = [float(i) for i in temp]
        houses.append(House((temp[0], temp[1]), temp[2]))

    if rand == False:
        coords = [batteries[i].coord for i in batteries]
    batteries = {}
    for i in range(len(batterieslist)):
        cap = batterieslist[i][2]
        if rand == True:
            coord = (random.randint(0,50), random.randint(0,50))
        else:
            coord = coords[i]
        batteries[i] = (Battery(coord, cap, i))

    # calculate distances to all batteries form houses
    for house in houses:
        house.calc_distances(batteries)

    # calculate all distances to houses from batteries
    for battery in batteries:
        batteries[battery].calculate_distances(houses)

    return batteries, houses


highscore_file = '../Data/wijk3_score_advanced1.txt'
housespath = '../Data/wijk3_huizen.csv'
batterypath = '../Data/wijk3_batterijen.csv'

houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)

highest_score = 1000
highest = []
attempt = 0

while highest_score > 610:
    
    batteries, houses = innit_data(houseslist, batterieslist, True, {})

    batteries, houses, houses_left = connect_houses(batteries, houses)

    if len(houses_left) > 0:
        attempt += 1
        continue

    # get results in json format
    result = makejson(batteries)

    # calculate number of cables
    all_cables = get_all_cables(result)

    if len(all_cables) < highest_score:
        highest_score = len(all_cables)
        highest = result
        print(len(all_cables))

print(highest_score)

for i in range(len(highest)):
    batteries[i].coord = highest[i]['locatie']

for i in batteries:
    print(batteries[i].coord)



highest_score_overall = 1000
highest_overall = []
for i in range(100):
    batteries = update_battery_location(batteries)
    highest_score = 1000
    highest = []
    for j in range(1000):
        batteries, houses = innit_data(houseslist, batterieslist, False, batteries)

        batteries, houses, houses_left = connect_houses(batteries, houses)
        if len(houses_left) > 0:
            continue
        
        result = makejson(batteries)
        all_cables = get_all_cables(result)

        if len(all_cables) < highest_score:
            highest_score = len(all_cables)
            highest = result

    all_cables = get_all_cables(highest)
    if len(all_cables) < highest_score_overall and len(all_cables) != 0:
        highest_score_overall = len(all_cables)
        highest_overall = highest
        print(f'NEW HIGHEST SCORE: {len(all_cables)}')
    print(f'{len(get_all_cables(highest))} for attempt {i}')


# get results in json format
result = highest_overall

# calculate number of cables
all_cables = get_all_cables(result)

print(len(all_cables))
    
for i in range(len(result)):
    print(result[i]['locatie'])

gridplotter(result)

with open(highscore_file, 'w') as outfile:
    json.dump(result, outfile)








