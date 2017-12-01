import tkinter as tk

import printer_query
import printer_db

root = tk.Tk()

printers = printer_db.LoadDB('printers.txt')

for p in printers:
    pres = printer_query.QueryPrinter(p)
    if '_color' in pres.type:
        s = tk.StringVar()
        s.set('{0} model: {5} black: {1} cyan: {2} magenta: {3} yellow: {4}'.format(pres.name, pres.black, pres.cyan,
                                                                                    pres.magenta,
                                                                                    pres.yellow,
                                                                                    pres.model))
        w = tk.Label(root, textvariable=s)
        w.pack()
    else:
        s = tk.StringVar()
        s.set('{0} model: {2} black: {1}'.format(pres.name, pres.black, pres.model))
        w = tk.Label(root, textvariable=s)
        w.pack()

root.mainloop()