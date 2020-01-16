from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, manhatten_distance, connect_houses,\
    update_battery_location, innit_data
from grid import gridplotter
import random
import json
import copy

highscore_file = '../Scores/wijk3_score_advanced4.txt'
housespath = '../Data/wijk3_huizen.csv'
batterypath = '../Data/wijk3_batterijen.csv'

houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)

batteries, houses = innit_data(houseslist, batterieslist, True, {})