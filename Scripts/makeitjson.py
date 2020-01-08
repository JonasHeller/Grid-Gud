from helpers import findpath, averagex_andy

def makejson(batteries):
    jsonlist = []
    for item in batteries:
        battery = batteries[item]
        batterydict = {
            'locatie' : battery.coord,
            'capaciteit' : battery.capacity,
            'huizen' : []
            }

        first = averagex_andy(battery)

        for house in battery.connected_houses:
            batterydict['huizen'].append({
                'locatie' : house.coord,
                'output' : house.output,
                'kabels' : findpath(battery.coord, house.coord, first)
            })
        jsonlist.append(batterydict)

    return jsonlist

