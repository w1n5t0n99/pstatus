import tkinter as tk
import threading

import printer_query
import printer_db

root = tk.Tk()
root.title('Printer Status')

printers = printer_db.LoadDB('printers.txt')

def AddLabels(printers):
    r = 0
    for p in printers:
        pres = printer_query.QueryPrinter(p)
        if '_color' in pres.type:
            m = tk.StringVar()
            m.set('{0}'.format(pres.name))
            tk.Label(root, textvariable=m).grid(row=r, column=0)
            b=tk.StringVar()
            b.set('{0}'.format(pres.black))
            tk.Label(root, textvariable=b).grid(row=r, column=1)
            c = tk.StringVar()
            c.set('{0}'.format(pres.cyan))
            tk.Label(root, textvariable=c, bg ="#00ffff").grid(row=r, column=2)
            m = tk.StringVar()
            m.set('{0}'.format(pres.magenta))
            tk.Label(root, textvariable=m, bg="#ff00ff").grid(row=r, column=3)
            y = tk.StringVar()
            y.set('{0}'.format(pres.yellow))
            tk.Label(root, textvariable=y, bg="#ffff00").grid(row=r, column=4)
            r+=1
        else:
            m = tk.StringVar()
            m.set('{0}'.format(pres.name))
            tk.Label(root, textvariable=m).grid(row=r, column=0)
            b = tk.StringVar()
            if pres.black != -3:
                b.set('{0}'.format(pres.black))
            else:
                b.set('OK')
            tk.Label(root, textvariable=b).grid(row=r, column=1)
            r += 1

threading.Thread(target=AddLabels, args=(printers,)).start()
root.mainloop()