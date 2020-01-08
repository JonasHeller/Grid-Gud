def get_all_cables(result):
    all_cables = []
    for battery in result:
        for house in battery['huizen']:
            all_cables += house['kabels']
    return all_cables

def get_houses_left(houses):
    houses_left = []
    for house in houses:
        if house.isconnected == False:
            houses_left.append(house)
    return houses_left

def findpath(start, end, first):
    path = []
    if first == 'H':
        i = start[0]
        if start[0] > end[0]:
            while i != end[0]:
                path.append((i, start[1]))
                i -= 1
        else:
            while i != end[0]:
                path.append((i, start[1]))
                i += 1

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

def averagex_andy(battery):
    x = 0
    y = 0
    coord = battery.coord
    for house in battery.connected_houses:
        x += abs(house.coord[0] - coord[0])
        y += abs(house.coord[1] - coord[1])
    avgx = x / len(battery.connected_houses)
    avgy = y / len(battery.connected_houses)
    if avgy < avgx:
        return 'V'
    else:
        return 'H'