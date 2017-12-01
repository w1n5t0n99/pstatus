import shlex

def LoadDB(file_name):
    printers = []
    with open(file_name, 'r') as f:
        for line in f:
            d = shlex.split(line)
            if len(d) == 3:
                printers.append((d[0], d[1], d[2]))

    return printers