import random
from House import House
import json
from Battery import Battery
import plotly.graph_objects as go

# get all laid cables
def get_all_cables(result):
    all_cables = []

    # loop over the batteries
    for battery in result:

        # loop over houses in the battery
        batterycables = []
        for house in battery['huizen']:

            # add cabels to the list
            batterycables += house['kabels']
        all_cables += set(batterycables)

    return all_cables

# get all houses not connected
def get_houses_left(houses):
    houses_left = []

    # loop over houses
    for house in houses:

        # check if it is connected and add to list if so
        if house.isconnected == False:
            houses_left.append(house)
    return houses_left

# find path from start to end
def findpath(start, end, first):
    path = []

    # if first == H, update horizontal (x values) first
    if first == 'H':

        # get start x values
        i = start[0]

        # if start x is bigger than end x, use -= 1
        if start[0] > end[0]:

            # while endpoint x is not yet reached, update current x
            while i != end[0]:
                path.append((i, start[1]))
                i -= 1
        
        # else use += 1
        else:
            while i != end[0]:
                path.append((i, start[1]))
                i += 1

        # set i to start y
        i = start[1]
        if start[1] > end[1]:
            while i != end[1]:
                path.append((end[0], i))
                i -= 1
        else:
            while i != end[1]:
                path.append((end[0], i))
                i += 1
    else:
        i = start[1]
        if start[1] > end[1]:
            while i != end[1]:
                path.append((start[0], i))
                i -= 1
        else:
            while i != end[1]:
                path.append((start[0], i))
                i += 1

        i = start[0]
        if start[0] > end[0]:
            while i != end[0]:
                path.append((i, end[1]))
                i -= 1
        else:
            while i != end[0]:
                path.append((i, end[1]))
                i += 1


    path.append(end)
    return path

# check if the algorithm needs to first do x values or y values
def averagex_andy(battery):
    x = 0
    y = 0
    coord = battery.coord

    # loop over houses connected to the battery
    for house in battery.connected_houses:

        # get distance to x,y coords from battery
        x += abs(house.coord[0] - coord[0])
        y += abs(house.coord[1] - coord[1])

    # calculate average x,y disatances
    avgx = x / len(battery.connected_houses)
    avgy = y / len(battery.connected_houses)

    # return bases on biggest averages
    if avgy > avgx:
        return 'V'
    else:
        return 'H'

# get closest cable to an endpoint
def get_closest_cable(cables, endpoint):
    closest = (110, 110)
    distance_to_closest = manhatten_distance(closest, endpoint)

    # loop over cables
    for cable in cables:

        # get manhatten distance to the endpoint
        distance = manhatten_distance(cable, endpoint)

        # if the distance is lower, update closest
        if distance < distance_to_closest:
            distance_to_closest = distance
            closest = cable
    
    # return closest
    return closest

def get_outliers(batteries):
    for index in batteries:
        battery = batteries[index]
        distances = []
        for house in battery.connected_houses:
            distances.append(house.distances[house.batteryconnected])
        average_distance = sum(distances) / len(distances)
        print(average_distance, max(distances))
    return 

def manhatten_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def connect_houses(batteries, houses):
        # let batteries choose its closest house in turn
    # i = 0
    skipcheck = 0
    while skipcheck != len(batteries):

        # set current to current batteries object
        current_battery = random.choice(list(batteries.keys()))
        current = batteries[current_battery]

        # get closest house to current
        house = current.get_closest_house()
        if house != None:
            if manhatten_distance(house.coord, current.coord) > 150:
                skipcheck += 1

            else: 
            # try to add it to the house
                try:
                    if current.capacity_check(house):
                        current.add_house(house)
                        skipcheck = 0
                    else:
                        skipcheck += 1
                except:
                    skipcheck = len(batteries)

        else:
            skipcheck = len(batteries)

    # get all houses not assigned
    houses_left = get_houses_left(houses)

    # loop for all houses in houses left
    for house in houses_left:

        # loop for batteries
        for battery in batteries:
            current = batteries[battery]

            # check if house can still be added to battery
            if current.capacity_check(house):
                house.isconnected = True
                current.add_house(house)

    # update houses left
    houses_left = get_houses_left(houses)

    # if houses left is not empty, check if some houses can be shuffled to add last house
    if len(houses_left) != 0:

        # loop over all batteries
        for battery in batteries:

            # calculate the capacity needed
            most_capacity = batteries[battery]
            cap_needed = houses_left[0].output - (most_capacity.capacity - most_capacity.currentload)

            # get house with lowest output that, if removed, will allow the house left to be added
            lowest = [100, 1]
            for house in most_capacity.connected_houses:
                if house.output > cap_needed and house.output < lowest[0]:
                    lowest = [house.output, house]

            # check if the house selected above can fit in an other battery
            try:
                for battery in batteries:
                    # if it fits, add it to the battery, remove it from the current battery
                    # and add the house left to the current battery
                    if batteries[battery].capacity_check(lowest[1]) and batteries[battery] != most_capacity:
                        batteries[battery].add_house(lowest[1])
                        most_capacity.remove_house(lowest[1])
                        most_capacity.add_house(houses_left[0])
                        break
            except:
                break

    # update houses left
    houses_left = get_houses_left(houses)
    return batteries, houses, houses_left

# Check if there is a house on the same X or Y that is closeby, if so change the direction to start the cable
# This elimantes snaking cables
def check_further(connected_cable, house, houses, default):
    for house in houses:
        if default == "V":
            if house.coord[1] == connected_cable[1] and abs(house.coord[0] - connected_cable[0]) <= 15:
                return "H"
            
        else:
            if house.coord[0] == connected_cable[0] and abs(house.coord[1] - connected_cable[1]) <= 15:
                return "V"
             
def update_battery_location(batteries):
    for i in batteries:
        avg_x = 0
        avg_y = 0
        battery = batteries[i]
        for house in battery.connected_houses:
            avg_x += house.coord[0]
            avg_y += house.coord[1]
        battery.coord = (round(avg_x / len(battery.connected_houses)), round(avg_y/ len(battery.connected_houses)))

    return batteries

def safe(batteries):
    temp = batteries
    return temp

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

        # place the batteries random
        if rand == True:
            battery_locations = []
            house_locations = [house.coord for house in houses]
            coord = (random.randint(0,50), random.randint(0,50))

            # try to get a battery placing where there is no house or other battery
            while coord in (house_locations + battery_locations):

                # make sure the battery is more than 15 places away form any ohter battery
                skip = -1
                while skip < len(battery_locations):
                    skip = 0
                    coord = (random.randint(0,50), random.randint(0,50))
                    for location in battery_locations:
                        if manhatten_distance(coord, location) < 10:
                            break
                        else:
                            skip += 1

            battery_locations.append(coord)

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

def save_highscore(path, result):
    try:
        with open(path) as json_file:
            data = json.load(json_file)

        if len(get_all_cables(data)) > len(get_all_cables(result)):
            with open(path, 'w') as outfile:
                json.dump(result, outfile)
    except:
        with open(path, 'w') as outfile:
            json.dump(result, outfile)


def connect_houses_from_houses(batteries, houses):
    skipcheck = 0
    while True:
        shortest = 100
        shortest_battery = None
        house = random.choice(houses)
        for i in batteries:
            if house.distances[i] < shortest and batteries[i].capacity_check(house) == True:
                shortest = house.distances[i]
                shortest_battery = i

        if shortest_battery != None:
            batteries[shortest_battery].add_house(house)
            houses.remove(house)
            skipcheck = 0
        else:
            skipcheck += 1

        if skipcheck == len(houses) or len(houses) == 0:
            break

    return batteries, houses

# Create a bargraph with all scores
def scores_plot(scores):
    amount_scores = []
    # Count how many times a score was found
    for score in set(sorted(scores)):
        amount_scores.append(scores.count(score))
    
    # Plot all scores with a colour gradient
    fig = go.Figure([go.Bar(x=list(set(sorted(scores))), y=amount_scores , marker_color=list(set(sorted(scores))))])
    fig.show()
    return 