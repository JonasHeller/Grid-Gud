## Read me

Smart grid project part of the minor programming at the Universety of Amsterdam

made by: Jonas Heller, Krolos Abdou, Justin Bon


### Goal

In this project the goal was to write and optimize an algorithm that connects all the houses in a grid to a battery using the least amount of cable possible. Minding the different output of each house and the maximum cappacity of each battery.  

We were given three different datasets to test our algorithm. Each has a different placement of the batteries and houses in addition to some minor capacaty differences.  


### process

Starting with the project the first goal was to succesfully connect all the houses to a battery without going over the maximum capacaty.  

After this we started with optimizing the algorithm and added more heuristics.  

At first each house was connected with a individual cable that was not to be shared by houses. Later the houses were allowed to share cables, this improved our algorithm by a lot. 


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


### Copyright

© 2020 All rights reserved 





