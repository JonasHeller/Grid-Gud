import re

def loadhouse(path):
    with open(path, 'r') as f:
        lines = f.read()
        houses = lines.split('\n')
        del houses[0]
        del houses[-1]
        return houses

def loadbattery(path):
    with open(path, 'r') as f:
        lines = f.read()
        batterijen = lines.split('\n')
        del batterijen[0]
        del batterijen[-1]
        batterijennew = []
        for batterij in batterijen:
            batterij = re.findall(r'\d+', batterij)
            batterijennew.append([int(batterij[0]), int(batterij[1]), float(batterij[2] + '.' + batterij[3])])
        return batterijennew