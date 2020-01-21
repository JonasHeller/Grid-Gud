from grid import gridplotter
from House import House
import json
from loadfiles import loadhouse
from helpers import manhatten_distance

def pathing_test():
    with open('../Scores/wijk3_score_advanced1.txt') as json_file:
        data = json.load(json_file)
    gridplotter(data)

def test_modulo():
    for j in range(10000):
        print(j % 1000)
        if j % 1000 == 0:
            print('HET WERKT')

def calc_average(path):
    houseslist = loadhouse(path)

    houses = []
    for house in houseslist:

        # clean up data
        temp = house.replace(' ', '').split(',')
        temp = [float(i) for i in temp]
        houses.append(House((temp[0], temp[1]), temp[2]))

    average = 0
    for house in houses:
        shortest = 100
        for neighbor in houses:
            if neighbor == house:
                continue
            distance = manhatten_distance(house.coord, neighbor.coord)
            if distance < shortest:
                shortest = distance
        average += shortest

    print(average/150, average)

calc_average('../Data/wijk3_huizen.csv')
