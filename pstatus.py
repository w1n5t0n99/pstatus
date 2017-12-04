import tkinter as tk
import threading

import printer_query
import printer_db

root = tk.Tk()
root.title('Printer Status')
root.minsize(width=300, height= 500)

printers = printer_db.LoadDB('printers.txt')

def AddTonerLabel(level, row, column):
    level_width = 5
    b = tk.StringVar()
    if isinstance(level, int):
        b.set('{0}'.format(level))
        tk.Label(root, textvariable=b, width=level_width,
                 fg='black' if abs(level) >= 10 else '#ff3232').grid(row=row, column=column)
    else:
        b.set(level)
        tk.Label(root, textvariable=b, width=level_width).grid(row=row, column=column)

def AddLabels(printers):
    r = 0
    level_width = 6

    tk.Label(root, text='Name', bg='gray').grid(row=0, column=0)
    tk.Label(root, text='Black', width=level_width, bg='gray').grid(row=0, column=1)
    tk.Label(root, text='Cyan', width=level_width, bg='#00ffff').grid(row=0, column=2)
    tk.Label(root, text='Magenta', width=level_width, bg='#ff00ff').grid(row=0, column=3)
    tk.Label(root, text='Yellow', width=level_width, bg='#ffff00').grid(row=0, column=4)
    r+=1

    for p in printers:
        pres = printer_query.QueryPrinter(p)
        if '_color' in pres.type:
            m = tk.StringVar()
            m.set('{0}'.format(pres.name))
            tk.Label(root, textvariable=m).grid(row=r, column=0)

            AddTonerLabel(pres.black, row=r, column=1)
            AddTonerLabel(pres.cyan, row=r, column=2)
            AddTonerLabel(pres.magenta, row=r, column=3)
            AddTonerLabel(pres.yellow, row=r, column=4)
            r+=1
        else:
            m = tk.StringVar()
            m.set('{0}'.format(pres.name))
            tk.Label(root, textvariable=m).grid(row=r, column=0)

            if pres.black != -3:
                AddTonerLabel(pres.black, row=r, column=1)
            else:
                AddTonerLabel('OK', row=r, column=1)
            r += 1

threading.Thread(target=AddLabels, args=(printers,)).start()
root.mainloop()