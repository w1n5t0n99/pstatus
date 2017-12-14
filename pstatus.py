import tkinter as tk
import threading

import printer_query
import printer_db
import printer_async_query

_NAME_WIDTH = 25
_LEVEL_WIDTH = 6

_TOTAL_COLUMNS = 5
_NAME_COLUMN = 0
_BLACK_COLUMN = 1
_CYAN_COLUMN = 2
_MAGENTA_COLUMN = 3
_YELLOW_COLUMN = 4

_update_lock = threading.Lock()

_ui_status_rows = []
_ui_refresh_button =  None

def SetAsHeaderRow():
    if len(_ui_status_rows) > 0:
        ui_row = _ui_status_rows[0]
        for r in ui_row:
            r.grid_forget()

        ui_row[0].config(text='Name', width=_NAME_WIDTH, bg='gray')
        ui_row[0].grid(row=0, column=0)
        ui_row[1].config(text='Black', width=_LEVEL_WIDTH, bg='gray')
        ui_row[1].grid(row=0, column=1)
        ui_row[2].config(text='Cyan', width=_LEVEL_WIDTH, bg='#00ffff')
        ui_row[2].grid(row=0, column=2)
        ui_row[3].config(text='Magenta', width=_LEVEL_WIDTH, bg='#ff00ff')
        ui_row[3].grid(row=0, column=3)
        ui_row[4].config(text='Yellow', width=_LEVEL_WIDTH, bg='#ffff00')
        ui_row[4].grid(row=0, column=4)

def SetAsStatusRow(row, name, black, cyan, magenta, yellow):
    if len(_ui_status_rows) > row:
        ui_row = _ui_status_rows[row]
        for r in ui_row[:-1]:
            r.grid_forget()

        n = tk.StringVar()
        n.set('{0}'.format(name))
        ui_row[0].config(textvariable=n, width=_NAME_WIDTH, bg=ui_row[5])
        ui_row[0].grid(row=row, column=0)

        b = tk.StringVar()
        b.set('{0}'.format(black))
        ui_row[1].config(textvariable=b, width=_LEVEL_WIDTH, bg=ui_row[5])
        ui_row[1].grid(row=row, column=1)

        c = tk.StringVar()
        c.set('{0}'.format(cyan))
        ui_row[2].config(textvariable=c, width=_LEVEL_WIDTH, bg=ui_row[5])
        ui_row[2].grid(row=row, column=2)

        m = tk.StringVar()
        m.set('{0}'.format(magenta))
        ui_row[3].config(textvariable=m, width=_LEVEL_WIDTH, bg=ui_row[5])
        ui_row[3].grid(row=row, column=3)

        y = tk.StringVar()
        y.set('{0}'.format(yellow))
        ui_row[4].config(textvariable=y, width=_LEVEL_WIDTH, bg=ui_row[5])
        ui_row[4].grid(row=row, column=4)

def SetAsErrorRow(row, msg):
    if len(_ui_status_rows) > row:
        ui_row = _ui_status_rows[row]
        for r in ui_row[:-1]:
            r.grid_forget()

        m = tk.StringVar()
        m.set('{0}'.format(msg))
        ui_row[0].config(textvariable=m, width=_NAME_WIDTH, bg='green')
        ui_row[0].grid(row=row, column=0, columnspan=5, rowspan=2, sticky='we')


def InitLabels(printers):
    r = 0
    l0 = tk.Label(root, text='Name', width=_NAME_WIDTH, bg='gray')
    l0.grid(row=0, column=0)
    l1 = tk.Label(root, text='Black', width=_LEVEL_WIDTH, bg='gray')
    l1.grid(row=0, column=1)
    l2 = tk.Label(root, text='Cyan', width=_LEVEL_WIDTH, bg='#00ffff')
    l2.grid(row=0, column=2)
    l3 = tk.Label(root, text='Magenta', width=_LEVEL_WIDTH, bg='#ff00ff')
    l3.grid(row=0, column=3)
    l4 = tk.Label(root, text='Yellow', width=_LEVEL_WIDTH, bg='#ffff00')
    l4.grid(row=0, column=4)

    printer_rows.append(l0)
    printer_rows.append(l1)
    printer_rows.append(l2)
    printer_rows.append(l3)
    printer_rows.append(l4)

    if printers.empty():
        l4 = tk.Label(root, text='Printers not found, make sure file named printers.txt\nin same directory as .exe', width=_NAME_WIDTH + (_LEVEL_WIDTH * 4), bg='green')
        l4.grid(row=1, column=0, columnspan=5, rowspan=2, sticky='we')
        return

    r = 1
    for p in list(printers.queue):
        m = tk.StringVar()
        m.set('{0}'.format(p[1]))

        l0 = tk.Label(root, textvariable=m, width=_NAME_WIDTH)
        l0.grid(row=r, column=0)
        l1 = tk.Label(root, text=' ', width=_LEVEL_WIDTH)
        l1.grid(row=r, column=1)
        l2 = tk.Label(root, text=' ', width=_LEVEL_WIDTH)
        l2.grid(row=r, column=2)
        l3 = tk.Label(root, text=' ', width=_LEVEL_WIDTH)
        l3.grid(row=r, column=3)
        l4 = tk.Label(root, text=' ', width=_LEVEL_WIDTH)
        l4.grid(row=r, column=4)

        orig_color = '#C0C0C0'
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

    button = tk.Button(root, text='Refresh', width=_LEVEL_WIDTH, command=AsyncUpdateLabels)
    button.grid(row=r, column=4)


def UpdateLabel(text, row, column, cell_width=_LEVEL_WIDTH):
    pl = printer_rows[(row * _TOTAL_COLUMNS) + column]
    b = tk.StringVar()
    if isinstance(text, int):
        b.set('{0}'.format(text))
        pl.config(textvariable=b, width=cell_width,
                  fg='black' if abs(text) >= 10 else '#ff3232')
    else:
        b.set(text)
        if text == 'Error':
            pl.config(textvariable=b, width=cell_width, fg='#ff3232')
        else:
            pl.config(textvariable=b, width=cell_width)

def AsyncUpdateLabels(printers):
    ps_thread = printer_async_query.PStatusThread('status-thread', printers)
    ps_thread.start()
    ps_thread.join()

    r = 1
    for p in list(printer_async_query.query_results.queue):
        if '_color' in p.type:
            UpdateLabel(text=p.name, row=r, column=0, cell_width=_NAME_WIDTH)
            UpdateLabel(text=p.black, row=r, column=1)
            UpdateLabel(text=p.cyan, row=r, column=2)
            UpdateLabel(text=p.magenta, row=r, column=3)
            UpdateLabel(text=p.yellow, row=r, column=4)
        else:
            if p.black != -3:
                UpdateLabel(text=p.black, row=r, column=1)
            else:
                UpdateLabel(text='OK', row=r, column=1)

        if p.status == 'error':
            UpdateLabel(text='Error', row=r, column=1)

        r += 1

def ClearLabels():
    r = 1
    for p in list(printers.queue):
        UpdateLabel(text=' ', row=r, column=1)
        UpdateLabel(text=' ', row=r, column=2)
        UpdateLabel(text=' ', row=r, column=3)
        UpdateLabel(text=' ', row=r, column=4)
        r += 1

root = tk.Tk()
root.title('Printer Status')
root.minsize(width=375, height= 500)
root.resizable(width=False, height=False)

printers = printer_db.LoadDBQueue('printers.txt')
printer_rows = []

'''
InitLabels(printers)
if printers != None:
    threading.Thread(name='update_thread', target=AsyncUpdateLabels, args=(printers,), daemon=True).start()
'''

for i in range(0,2):
    l0 = tk.Label(root, text='Name', width=_NAME_WIDTH, bg='gray')
    l0.grid(row=i, column=0)
    l1 = tk.Label(root, text='Black', width=_LEVEL_WIDTH, bg='gray')
    l1.grid(row=i, column=1)
    l2 = tk.Label(root, text='Cyan', width=_LEVEL_WIDTH, bg='#00ffff')
    l2.grid(row=i, column=2)
    l3 = tk.Label(root, text='Magenta', width=_LEVEL_WIDTH, bg='#ff00ff')
    l3.grid(row=i, column=3)
    l4 = tk.Label(root, text='Yellow', width=_LEVEL_WIDTH, bg='#ffff00')
    l4.grid(row=i, column=4)

    r = []
    r.append(l0)
    r.append(l1)
    r.append(l2)
    r.append(l3)
    r.append(l4)
    r.append('gray')
    _ui_status_rows.append(r)

SetAsStatusRow(0, 'test name', 55, 44, 33, 22)
SetAsErrorRow(0, 'test error row')

root.mainloop()

'''
oid = '1.3.6.1.2.1.25.3.5.1.2'
printer_query.DebugQueryWalk('172.19.3.11')
'''