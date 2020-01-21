from helpers import findpath, averagex_andy, get_closest_cable, check_further

# output the results in json format
def makejson(batteries):
    jsonlist = []

    # loop over batteries
    for item in batteries:
        battery = batteries[item]

        # create a dict for the battery
        batterydict = {
            'locatie' : battery.coord,
            'capaciteit' : battery.capacity,
            'huizen' : []
            }

        # check if horizontal or vertical needs to be done first
        first = averagex_andy(battery)
        # loop over connected houses
        for house in battery.connected_houses:

            get all aready laid cables
            all_cables = []
            for houses in batterydict['huizen']:
                all_cables += houses['kabels']

            check which cable is closest to the house
            start = get_closest_cable(all_cables, house.coord)
            if start == (110, 110):
                start = battery.coord
            other = check_further(start, house.coord, battery.connected_houses, first)
            if other != first:
                path = findpath(start, house.coord, other)
            else:
                path = findpath(start, house.coord, first)
            house.path = path

            # make dict for the house
            batterydict['huizen'].append({
                'locatie' : house.coord,
                'output' : house.output,
                # create the path to the house from the battery
                'kabels' : path
            })
        jsonlist.append(batterydict)

    return jsonlist
