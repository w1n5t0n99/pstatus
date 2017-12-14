import tkinter as tk
import threading

import printer_db
import printer_async_query
import grid


_NAME_WIDTH = 25
_LEVEL_WIDTH = 6

_TOTAL_COLUMNS = 5
_NAME_COLUMN = 0
_BLACK_COLUMN = 1
_CYAN_COLUMN = 2
_MAGENTA_COLUMN = 3
_YELLOW_COLUMN = 4
_update_lock = threading.Lock()

_rows = []
_root = None
_ref_button = None

def InitLabels(printers):
    grid.GridHeaderRow(root)

    if printers.empty():
        _rows.append(grid.GridMsgRow(root, 1, 'Printers not found, make sure file named printers.txt\nin same directory as .exe'))
        return

    r = 1
    for p in list(printers.queue):

        _rows.append(grid.GridRow(root, r, p[1], ' ', ' ', ' ', ' '))
        r +=1

        _ref_button = tk.Button(root, text='Refresh', width=_LEVEL_WIDTH, command=AsyncUpdateLabels)
        _ref_button.grid(row=r, column=4)


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

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Printer Status')
    root.minsize(width=375, height=500)
    root.resizable(width=False, height=False)

    printers = printer_db.LoadDBQueue('printers.txt')
    printer_rows = []

    InitLabels(printers)
    '''
    if printers != None:
        threading.Thread(name='update_thread', target=AsyncUpdateLabels, args=(printers,), daemon=True).start()
    '''

    root.mainloop()

    '''
    oid = '1.3.6.1.2.1.25.3.5.1.2'
    printer_query.DebugQueryWalk('172.19.3.11')
    '''


