import json
from grid import *

with open('../Data/wijk1_score.txt') as json_file:
    wijk1 = json.load(json_file)
with open('../Data/wijk2_score.txt') as json_file:
    wijk2 = json.load(json_file)
with open('../Data/wijk3_score.txt') as json_file:
    wijk3 = json.load(json_file)

housespath = '../Data/wijk1_huizen.csv'
batterypath = '../Data/wijk1_batterijen.csv'
gridplotter(wijk1, batterypath, housespath)
    
housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'
gridplotter(wijk2, batterypath, housespath)

housespath = '../Data/wijk3_huizen.csv'
batterypath = '../Data/wijk3_batterijen.csv'
gridplotter(wijk3, batterypath, housespath)