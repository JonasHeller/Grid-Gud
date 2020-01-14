import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Makes a grid for the different neighborhoods
def gridplotter(jsonpaths):

    # Plot the grid
    plt.axis([-1, 51, -1, 51])
    plt.locator_params(nbins=10)

    # Show the major grid lines with dark grey lines
    plt.grid(b=True, which='major', color='#666666', linestyle='-')

    # Show the minor grid lines with very faint and almost transparent grey lines
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#666666', linestyle='-', alpha=0.1)

    # Plots the Batteries in the grid
    for battery in jsonpaths:
        plt.plot(battery['locatie'][0], battery['locatie'][1], 'Hr', label='Batteries')

    # Plots the Houses in the grid
    for battery in jsonpaths:
        for house in battery['huizen']:
            plt.plot(house['locatie'][0], house['locatie'][1], '^g', label='Houses')

    colors = ['b', 'c', 'm', 'y', 'k']

    # Plot the paths from the houses to the batteries, each battery has its own color
    for j in range(len(jsonpaths)):
        for house in jsonpaths[j]['huizen']:
            plt.plot([i[0] for i in house['kabels']], [i[1] for i in house['kabels']], colors[j])

    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)

    plt.show()
