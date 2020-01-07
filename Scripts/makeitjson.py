def makejson(batteries):
    jsonlist = []
    for item in batteries:
        battery = batteries[item]
        batterydict = {
            'locatie' : battery.coord,
            'capaciteit' : battery.capacity,
            'huizen' : []
            }
        
        for house in battery.connected_houses:
            batterydict['huizen'].append({
                'locatie' : house.coord,
                'output' : house.output,
                'kabels' : findpath(battery.coord, house.coord)
            })
        jsonlist.append(batterydict)

    return jsonlist

def findpath(start, end):
    path = []
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
    path.append(end)
    return path