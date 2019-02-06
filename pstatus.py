import tkinter as tk
import grid
import scroll_frame

import threading

import printer_db as db
import printer as pr

_header = None
_rows = []
_row_offset = 1
_root = None
_ref_button = None

_printers = []

def create_printers(printers_text):
    printers = []
    for p in printers_text:
        if p[2] == 'bw':
            printers.append(pr.PrinterBW(p[1], p[0]))
        elif p[2] == 'color':
            printers.append(pr.PrinterColor(p[1], p[0]))

    return printers

def query_printer(printer):
    try:
        printer.query()

        if printer.cyan is None:
            print('{} b: {}'.format(printer.name, printer.black))
        else:
            print('{} b: {} c: {} m: {} y : {}'.format(printer.name, printer.black, printer.cyan,
                                                       printer.magenta, printer.yellow))

    except:
        print('ERROR: {}'.format(printer.name))


def InitPrinterGui(printers):
    _header = grid.GridHeaderRow(scroll_win.scrollwindow)
    _rows.append(_header)
    r = len(_rows)
    global _row_offset
    _row_offset = r

    for p in list(printers.queue):

        _rows.append(grid.GridRow(scroll_win.scrollwindow, r, p[1], ' ', ' ', ' ', ' '))
        r +=1

   # _ref_button = tk.Button(root, text='Refresh', width=6, command=RunUpdateThread)
    _ref_button.grid()


def UpdatePrinterGui(row, name, black, cyan, magenta, yellow):
    if isinstance(_rows[row], grid.GridRow):
        _rows[row].update(name, black, cyan, magenta, yellow)
    else:
        _rows[row].grid_forget()
        _rows[row] = grid.GridRow(scroll_win.scrollwindow, row, name, black, cyan, magenta, yellow)

def UpdatePrinterGuiMsg(row, msg):
    _rows[row].grid_forget()
    #header is grid row 0
    _rows[row] = grid.GridMsgRow(scroll_win.scrollwindow, row+1, msg)

def ClearLabels():
    for row, i in enumerate(_rows[1:]):
        if isinstance(_rows[i], grid.GridRow):
            _rows[row].clear()
        else:
            _rows[row].grid_forget()

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Printer Status')
  #  root.minsize(width=375, height=500)
   # root.resizable(width=False, height=False)

    scroll_win = scroll_frame.ScrolledWindow(root, canv_h=500, canv_w=375)
    scroll_win.grid()

    '''


    try:
        _printers = printer_db.LoadDB('printers.txt')
    except EnvironmentError:
        _printers = queue.Queue()
        if _printers.empty():
            _rows.append(grid.GridMsgRow(scroll_win.scrollwindow,
                                         1, 'Printers not found, make sure file named printers.txt\nin same directory as .exe'))
    finally:
        InitPrinterGui(_printers)

    '''

    pr_text = db.LoadDB('printers.txt')
    printers = create_printers(pr_text)
    printer_threads = []

    for p in printers:
        printer_threads.append(threading.Thread(target=query_printer, args=(p, )))

    for p in printer_threads:
        p.start()
        #p.join()


    root.mainloop()


