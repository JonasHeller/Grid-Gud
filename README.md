## Read me

Smart grid project part of the minor programming at the Universety of Amsterdam

made by: Jonas Heller, Krolos Abdou, Justin Bon


### Goal

In this project the goal was to write and optimize an algorithm that connects all the houses in a grid to a battery using the least amount of cables possible, minding the different output of each house and the maximum cappacity of each battery.  

We were given three different datasets to test our algorithms. Each has a different placement of the batteries and houses in addition to some minor capacaty differences.  

The project consist of four problems:
- Random: Find a random solution
- Optimize the made algorithm
- Change the places of the batteries
- Buy different batteries


### Algorithms

#### Random
This algorithm is fairly simple: Connect all houses at random with a battery without exceeding the capacaty. After allocating all the houses connect them using the following algorithm: Check the average X and Y distance from the battery to its connected houses. Based on the result, make the horizontal or vertical path first (This does not matter if cables cannot be shared between houses).

#### Withclustering
For this algorithm we use a moddified version of the prim algorithm. First, the algorithm chooses a random battery and allocates the closest house to it. If the battery already has houses allocated to it, choose a house that is closest to the battery or a already connected house (Closest to the cluster as a whole). When all houses are allocated, make the paths to connect them to their battery. The algorithm always tries to connect a house to the closest already laid cable in its network. It also checks if there are houses farther away from it that are on the same X or Y coordinate as to eliminate snaking cables. 

#### Midpointclustering
This algorithm places all the batteries on random locations but no closer than 15 spaces from another battery. It then allocates all the houses 1000 times and then takes the best result. Then it moves the batteries to the middel of this result. This all is done 10 times to get an optimal result. The pathmaking is the same as in "Withclustering"

#### Buybatteries
For this task we were allowed to purchase our own desired batteries with different capacaty to cost ratio's. The algorithm makes a random selection of batteries that satisfies the total output of all the houses. It then places them the same way as "Midpointclustering" but does not move them once placed. It then connects the houses the same way as in "Withclustering". This is done 1000 times and the best score is saved. It then makes a new selection of batteries and repeats this process ten times. 


### Repository 

This respository consists of some documentation, a data folder, a scripts folder and a scores folder. 

In the data folder you will find all the neccesary datafiles to run the project. This includes the posistion of the houses and batteries. 

The scripts folder includes all the different scripts we wrote. 

These files do the following:

Battery and house include the needed classes 

Loadfiles load the desired files into the script

Makeitjson takes the result of a solution and formats it to Json

Grid takes the Json and makes a visualisation

Random is an script that finds a random correct solution.

Withclustering uses different heuristics to improve the algorithm to find a lowest possible score. 

Midpointclustering uses different heuristics to find a solution. This includes changing the position of the batteries. (v2, v3, v4 are variations that are not used for our top scores.)

buybatteries uses batteries of different costs and capacaties to find a solution 

Bestscores load the best scores for each datasets and makes a visualisation 

Test is just a generic file for testing some functionality

The scores folder includes all our top scores in Json format. 

### Running it yourself

To run the project yourself just download the repository and navigate to the folder in a terminal/cmd.

Check the requirements.txt for all the packages you will need or run "pip install -r requirements.txt"

Choose which dataset you want to try by changing the path at the top of the file you want to run. 

For random see the docstring comment in makeitjson.py  

Just run the file using "python3 {filename.py}"

The files containing the algorithms are:
- Random.py
- withclustering.py
- midpointclustering.py
- buybatteries.py

### Copyright

© 2020 All rights reserved 





