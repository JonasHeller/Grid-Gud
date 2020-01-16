from grid import gridplotter
import json

def pathing_test():
    with open('../Data/wijk3_score_advanced1.txt') as json_file:
        data = json.load(json_file)
    gridplotter(data)

def test_modulo():
    for j in range(10000):
        print(j % 1000)
        if j % 1000 == 0:
            print('HET WERKT')
pathing_test()