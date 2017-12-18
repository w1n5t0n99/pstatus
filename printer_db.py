import shlex
import os
import queue

def LoadDB(file_name):
    printers = queue.Queue()

    index = 0
    with open(file_name, 'r') as f:
        for line in f:
            d = shlex.split(line)
            if len(d) == 3:
                printers.put((d[0], d[1], d[2], index))
                index+=1

    return printers
