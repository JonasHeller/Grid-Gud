import json
from grid import gridplotter
import pprint as pp

with open('../Scores/wijk1_score.txt') as json_file:
    wijk1 = json.load(json_file)
with open('../Scores/wijk2_score.txt') as json_file:
    wijk2 = json.load(json_file)
with open('../Scores/wijk3_score.txt') as json_file:
    wijk3 = json.load(json_file)



gridplotter(wijk1)
 
gridplotter(wijk2)

gridplotter(wijk3)