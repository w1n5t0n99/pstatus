import shlex
import os

def LoadDB(file_name):
    printers = []

    index = 0
    with open(file_name, 'r') as f:
        for line in f:
            d = shlex.split(line)
            if len(d) == 3:
                printers.append((d[0], d[1], d[2], index))
                index+=1

    return printers
