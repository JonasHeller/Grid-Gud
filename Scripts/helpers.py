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