from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import random
from helpers import innit_data, update_battery_location, connect_houses, get_all_cables, save_highscore
from grid import gridplotter

highscore_file = '../Data/wijk2_score.txt'
housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'

houseslist = loadhouse(housespath)

battery_options = [
    {'price' : 900, 'capacity': 450}, 
    {'price' : 1350, 'capacity': 900}, 
    {'price' : 1800, 'capacity': 1800}
]

total_cap = 0
battery_combo = []
price = 0

while total_cap < 7500:
    battery = random.choice(battery_options)
    total_cap += battery['capacity']
    price += battery['price']
    battery_combo.append([100, 100, battery['capacity']])

batteries, houses = innit_data(houseslist, battery_combo, True, {})

for battery in batteries:
    print(batteries[battery])
print(price, total_cap)

batteries, houses, houses_left = connect_houses(batteries, houses)

# update battery location 100 times
for i in range(100):
    # safe previous coordinates
    previous_coord = [batteries[i].coord for i in batteries]

    # update battery location to middle of its cluster
    batteries = update_battery_location(batteries)
    highest_score = 1000
    highest = []

    # try to get a high score
    for j in range(1000):
        print(j)

        # clean batteries and houses for next loop
        batteries, houses = innit_data(houseslist, battery_combo, False, batteries)

        # make connections
        batteries, houses, houses_left = connect_houses(batteries, houses)

        # if there are houses left, try again
        if len(houses_left) > 0:
            continue
            
        # make result and get all cables
        result = makejson(batteries)
        all_cables = get_all_cables(result)

        # update highest score for current battery location
        if len(all_cables) < highest_score:
            highest_score = len(all_cables)
            highest = result
            
    highest = makejson(batteries)
    # get score for highest of the battery location
    all_cables = get_all_cables(highest)

    # update highest scores overall
    if len(all_cables) < highest_score_overall and len(all_cables) != 0:
        highest_score_overall = len(all_cables)
        highest_overall = highest
        print(f'NEW HIGHEST SCORE: {len(all_cables)}')

    print(f'{len(get_all_cables(highest))} for attempt {i}. Starting with {len(get_all_cables(makejson(batteries)))}')

# get results in json format
result = highest_overall

# calculate number of cables
all_cables = get_all_cables(result)

print(len(all_cables))
    
for i in range(len(result)):
    print(result[i]['locatie'])

gridplotter(result)

save_highscore(highscore_file, result)