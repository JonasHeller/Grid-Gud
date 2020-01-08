import re

# load houses file from path
def loadhouse(path):

    # open file
    with open(path, 'r') as f:

        # read lines, split on newline and remove first (header) and last (empty) lines
        lines = f.read()
        houses = lines.split('\n')
        del houses[0]
        del houses[-1]
        return houses

# load battery file from path
def loadbattery(path):

    # open file
    with open(path, 'r') as f:

        # read lines, split on newline and remove first (header) and last (empty) lines
        lines = f.read()
        batterijen = lines.split('\n')
        del batterijen[0]
        del batterijen[-1]
        batterijennew = []

        # loop over all batteries
        for batterij in batterijen:

            # get all numbers from the string
            batterij = re.findall(r'\d+', batterij)

            # add numbers to list
            batterijennew.append([int(batterij[0]), int(batterij[1]), float(batterij[2] + '.' + batterij[3])])
        return batterijennew