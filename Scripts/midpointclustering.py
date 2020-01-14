from House import House
from Battery import Battery
from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, switchoutliers, manhatten_distance
from grid import gridplotter
import random
import json


highscore_file = '../Data/wijk2_score_advanced1.txt'
housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'

houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)

houses = []
for house in houseslist:

    # clean up data
    temp = house.replace(' ', '').split(',')
    temp = [float(i) for i in temp]
    houses.append(House((temp[0], temp[1]), temp[2]))

batteries = []
for i in range(len(batterieslist)):
    cap = batterieslist[i][2]
    coord = (random.randint(0,50), random.randint(0,50))
    batteries.append(coord, cap, i)

# calculate distances to all batteries form houses
for house in houses:
    house.calc_distances(batteries)

# calculate all distances to houses from batteries
for battery in batteries:
    batteries[battery].calculate_distances(houses)





