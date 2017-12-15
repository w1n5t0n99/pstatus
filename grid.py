import tkinter as tk

_NAME_WIDTH = 20
_VAL_WIDTH = 5

def ToStringVar(data):
    sv = tk.StringVar()
    sv.set('{}'.format(data))
    return sv

class GridHeaderRow:
    def __init__(self, root):
        self._root = root
        self._row = 0
        self._ws = []
        # add header
        self.grid_set()

    def grid_forget(self):
        for w in self._ws:
            w.grid_forget()

    def grid_set(self):
        ids = ['Name', 'Black', 'Cyan', 'Magenta', 'Yellow']
        widths = [_NAME_WIDTH, _VAL_WIDTH, _VAL_WIDTH, _VAL_WIDTH, _VAL_WIDTH]
        bgs = ['gray', 'gray', '#00ffff', '#ff00ff', '#ffff00']
        for i in range(5):
            l = tk.Label(self._root, textvariable=ToStringVar(ids[i]), bg=bgs[i], width=widths[i])
            l.grid(row=self._row, column=i, sticky='nsew')
            self._ws.append(l)

        for i in range(1, 5):
            self._root.grid_columnconfigure(i, weight=1)

class GridRow:
    def __init__(self, root, row, name, black, cyan, magenta, yellow):
        self._root = root
        self._row = row
        self._name = name
        self._vals = []
        self._vals.append(black)
        self._vals.append(cyan)
        self._vals.append(magenta)
        self._vals.append(yellow)

        self.grid_set()

    def grid_forget(self):
        self._nw.grid_forget()
        for w in self._vws:
            w.grid_forget()

    def grid_set(self):
        bg_color = '#B0B0B0' if (self._row % 2) == 0 else 'white'

        self._nw = tk.Label(self._root, textvariable=ToStringVar(self._name), bg=bg_color, width=_NAME_WIDTH)
        self._nw.grid(row=self._row, column=0, sticky='nsew')

        self._vws = []
        for i, val in enumerate(self._vals):
            if isinstance(val, int):
                fg_color='black' if abs(val) >= 10 else '#ff3232'
            else:
                fg_color = 'black'

            if val == -3:
                val = 'OK'

            l = tk.Label(self._root, textvariable=ToStringVar(val), bg=bg_color, width=_VAL_WIDTH, fg=fg_color)
            l.grid(row=self._row, column=i + 1, sticky='nsew')
            self._vws.append(l)

class GridMsgRow:
    def __init__(self, root, row, msg):
        self._root = root
        self._row = row
        self._msg = msg

        self.grid_set()

    def grid_set(self):
        self._mw = tk.Label(self._root, textvariable=ToStringVar(self._msg), bg='green')
        self._mw.grid(row=self._row, column=0, columnspan=5, sticky='nsew')

    def grid_forget(self):
        self._mw.grid_forget()

