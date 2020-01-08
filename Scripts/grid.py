import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from loadfiles import loadbattery, loadhouse

# Makes a grid for the different neighborhoods
def gridplotter(jsonpaths, batterypath, housespath):
    houses = loadhouse(housespath)
    batterijen = loadbattery(batterypath)

    # Stores the x and y coordinates of the Batteries
    batteryX = []
    batteryY = []
    for battery in batterijen:
        batteryX.append(int(battery[0]))
        batteryY.append(int(battery[1]))

    # Stores the x and y coordinates of the Houses
    housesX = []
    housesY = []
    for house in houses:
        temp = house.replace(' ', '').split(',')
        temp = [float(i) for i in temp]

        housesX.append(int(temp[0]))
        housesY.append(int(temp[1]))

    # Plot the grid
    plt.axis([-1, 51, -1, 51])
    plt.locator_params(nbins=10)

    # Show the major grid lines with dark grey lines
    plt.grid(b=True, which='major', color='#666666', linestyle='-')

    # Show the minor grid lines with very faint and almost transparent grey lines
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#666666', linestyle='-', alpha=0.1)

    # Plot the Houses and Batteries
    plt.plot(housesX, housesY, '^g', label="Houses")
    plt.plot(batteryX, batteryY, 'Hr', label="Batteries")

    colors = ['b', 'c', 'm', 'y', 'k']

    # Plot the paths from the houses to the batteries, each battery has its own color
    for j in range(len(jsonpaths)):
        for house in jsonpaths[j]['huizen']:
            plt.plot([i[0] for i in house['kabels']], [i[1] for i in house['kabels']], colors[j])

    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)

    plt.show()
