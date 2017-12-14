import tkinter as tk

name_width = 20
val_width = 5

def ToStringVar(data):
    sv = tk.StringVar()
    sv.set('{}'.format(data))
    return sv

class GridRow:
    def __init__(self, row, name, val0, val1, val2, val3):
        self._row = row
        self._name = name
        self._vals = []
        self._vals.append(val0)
        self._vals.append(val1)
        self._vals.append(val2)
        self._vals.append(val3)

        self.grid_set()

    def grid_forget(self):
        self._nw.grid_forget()
        for w in self._vws:
            w.grid_forget()

    def grid_set(self):
        self._nw = tk.Label(root, textvariable=ToStringVar(self._name), bg='gray', width=name_width)
        self._nw.grid(row=self._row, column=0, sticky='nsew')

        self._vws = []
        for i in range(4):
            l = tk.Label(root, textvariable=ToStringVar(self._vals[i]), bg='gray', width=val_width)
            l.grid(row=self._row, column=i + 1, sticky='nsew')
            self._vws.append(l)

class GridMsgRow:
    def __init__(self, row, msg):
        self._row = row
        self._msg = msg

        self.grid_set()

    def grid_set(self):
        self._mw = tk.Label(root, textvariable=ToStringVar(self._msg), bg='green')
        self._mw.grid(row=self._row, column=0, columnspan=5, sticky='nsew')

    def grid_forget(self):
        self._mw.grid_forget()

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Test Grid')
    root.minsize(width=375, height=500)
    root.resizable(width=False, height=False)

    # add header
    for i in range(5):
        if i == 0:
            tk.Label(root, text='text {}'.format(i), bg='gray', width=name_width).grid(row=0, column=i, sticky='nsew')
        else:
            tk.Label(root, text='text {}'.format(i), bg='gray', width=val_width).grid(row=0, column=i, sticky='nsew')

    for i in range(1, 5):
        root.grid_columnconfigure(i, weight=1)

    g0 = GridRow(1, 'row 1', '44', 55, 66, 77)
    g1 = GridRow(3, 'row 2', '44', 55, 66, 77)
    g2 = GridMsgRow(2, 'this is a message\nmessgae\nmessage')

    #g0.grid_forget()
    #g1.grid_forget()
    root.mainloop()

