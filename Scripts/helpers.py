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

            # while endpoitn x is not yet reached, update current x
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
    distance_to_closest = abs(closest[0] - endpoint[0]) +abs(closest[1] - endpoint[1])

    # loop over cables
    for cable in cables:

        # get manhatten distance to the endpoint
        distance = abs(cable[0] - endpoint[0]) +abs(cable[1] - endpoint[1])

        # if the distance is lower, update closest
        if distance < distance_to_closest:
            distance_to_closest = distance
            closest = cable
    
    # return closest
    return closest

def get_outliers(batteries):
    outliers = []
    for index in batteries:
        battery = batteries[index]
        for house in battery.connected_houses:
            if house.distances[index] > 50:
                outliers.append(house)
    return outliers

def switchoutliers(outliers, houses, batteries):
    outliers_distance = []
    for outlier in outliers:
        outliers_distance.append([outlier.distances[outlier.batteryconnected], outlier])

    outliers_distance.sort(key=lambda tup: tup[0], reverse=True)
    
    for item in outliers_distance:
        print(outlier)
        tried_switches = []
        while True:
            closest_house = [100, 1]
            outlier = item[1]
            # get house closest to outier
            for house in houses:
                distance = abs(outlier.coord[0] - house.coord[0]) +abs(outlier.coord[1] - house.coord[1])
                if distance < closest_house[0] and outlier.batteryconnected != house.batteryconnected:
                    closest_house[0] = distance
                    closest_house[1] = house

            # get house to switch with
            switch_house = [100, 1, 2]
            for old in batteries[outlier.batteryconnected].connected_houses:
                if old in outliers:
                    continue
                for new in batteries[closest_house[1].batteryconnected].connected_houses:
                    distance = abs(new.coord[0] - old.coord[0]) +abs(new.coord[1] - old.coord[1])
                    if distance < switch_house[0]:
                        switch_house[0] = distance
                        switch_house[1] = old
                        switch_house[2] = new

            # try the switch
            outlier_battery = batteries[outlier.batteryconnected]
            switch_battery = batteries[closest_house[1].batteryconnected]
            if switch_battery.currentload + (outlier.output - switch_house[2].output) < switch_battery.capacity and \
                outlier_battery.currentload + (switch_house[2].output - outlier.output) < outlier_battery.capacity:
                outlier_battery.remove_house(outlier)
                switch_battery.add_house(outlier)
                outlier_battery.add_house(switch_house[2])
                switch_battery.remove_house(switch_house[2])
                print("CURRENT OUTLIER", outlier)
                print('CLOSEST TO OUTLIER',closest_house[0], closest_house[1])
                print('SWITCH', switch_house[0], '\nOLD',switch_house[1],'\nNEW' ,switch_house[2])
                print('Dit zou moeten werken')
                break

            else:
                tried_switches.append([closest_house[1], switch_house[1], switch_house[2]])
                break

            print('__________________________________________________')



    return