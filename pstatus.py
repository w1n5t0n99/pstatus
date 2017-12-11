import tkinter as tk
import threading

import printer_query
import printer_db

name_width = 25
level_width = 6
total_column = 5

def InitLabels(printers):
    r = 0
    l0 = tk.Label(root, text='Name', width=name_width, bg='gray')
    l0.grid(row=0, column=0)
    l1 = tk.Label(root, text='Black', width=level_width, bg='gray')
    l1.grid(row=0, column=1)
    l2 = tk.Label(root, text='Cyan', width=level_width, bg='#00ffff')
    l2.grid(row=0, column=2)
    l3 = tk.Label(root, text='Magenta', width=level_width, bg='#ff00ff')
    l3.grid(row=0, column=3)
    l4 = tk.Label(root, text='Yellow', width=level_width, bg='#ffff00')
    l4.grid(row=0, column=4)

    printer_rows.append(l0)
    printer_rows.append(l1)
    printer_rows.append(l2)
    printer_rows.append(l3)
    printer_rows.append(l4)

    if printers == None:
        l4 = tk.Label(root, text='Printers not found, make sure file named printers.txt\nin same directory as .exe', width=name_width + (level_width*4), bg='green')
        l4.grid(row=1, column=0, columnspan=5, rowspan=2, sticky='we')
        return

    r = 1
    for p in printers:
        m = tk.StringVar()
        m.set('{0}'.format(p[1]))

        l0 = tk.Label(root, textvariable=m, width=name_width)
        l0.grid(row=r, column=0)
        l1 = tk.Label(root, text=' ', width=level_width)
        l1.grid(row=r, column=1)
        l2 = tk.Label(root, text=' ', width=level_width)
        l2.grid(row=r, column=2)
        l3 = tk.Label(root, text=' ', width=level_width)
        l3.grid(row=r, column=3)
        l4 = tk.Label(root, text=' ', width=level_width)
        l4.grid(row=r, column=4)

        orig_color = l0.cget('background')
        alt_color = 'white'

        if r%2 == 0:
            bg_color = alt_color
        else:
            bg_color = orig_color

        l0.config(bg=bg_color)
        l1.config(bg=bg_color)
        l2.config(bg=bg_color)
        l3.config(bg=bg_color)
        l4.config(bg=bg_color)

        printer_rows.append(l0)
        printer_rows.append(l1)
        printer_rows.append(l2)
        printer_rows.append(l3)
        printer_rows.append(l4)
        r +=1

    button = tk.Button(root, text='Refresh', width=level_width, command=AsyncUpdateLablels)
    button.grid(row=r, column=4)


def UpdateLabel(level, row, column):
    pl = printer_rows[(row*total_column)+column]
    b = tk.StringVar()
    if isinstance(level, int):
        b.set('{0}'.format(level))
        pl.config(textvariable=b, width=level_width,
                 fg='black' if abs(level) >= 10 else '#ff3232')
    else:
        b.set(level)
        if level == 'Error':
            pl.config(textvariable=b, width=level_width, fg='#ff3232')
        else:
            pl.config(textvariable=b, width=level_width)



def UpdateLabels(printers):
    r=1

    for p in printers:
        pres = printer_query.QueryPrinter(p)
        if '_color' in pres.type:

            UpdateLabel(level=pres.black, row=r, column=1)
            UpdateLabel(level=pres.cyan, row=r, column=2)
            UpdateLabel(level=pres.magenta, row=r, column=3)
            UpdateLabel(level=pres.yellow, row=r, column=4)
        else:
            if pres.black != -3:
                UpdateLabel(level=pres.black, row=r, column=1)
            else:
                UpdateLabel(level='OK', row=r, column=1)

        if pres.status == 'error':
            UpdateLabel(level='Error', row=r, column=1)

        r += 1

def ClearLabels():
    r = 1
    for p in printers:
        UpdateLabel(level=' ', row=r, column=1)
        UpdateLabel(level=' ', row=r, column=2)
        UpdateLabel(level=' ', row=r, column=3)
        UpdateLabel(level=' ', row=r, column=4)
        r += 1

def AsyncUpdateLablels():
    for thread in threading.enumerate():
        if thread.name == 'update_thread':
            return
        else:
            ClearLabels()
            threading.Thread(name='update_thread', target=UpdateLabels, args=(printers,), daemon=True).start()


root = tk.Tk()
root.title('Printer Status')
root.minsize(width=375, height= 500)
root.resizable(width=False, height=False)

printers = printer_db.LoadDB('printers.txt')
printer_rows = []

'''
InitLabels(printers)
if printers != None:
    threading.Thread(name='update_thread', target=UpdateLabels, args=(printers,), daemon=True).start()
root.mainloop()
'''

printer_query.AsyncQueryPrinters(printers, 2)
for p in printer_query.query_results:
    print(p[3][0][1])