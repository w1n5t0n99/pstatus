import tkinter as tk
import threading
import queue
import struct

import printer_db
import grid
import scroll_frame
import printer_snmp as ps
import printer_group as pg
import printer as pr
from pysnmp.hlapi import *


_update_lock = threading.Lock()

_header = None
_rows = []
_row_offset = 1
_root = None
_ref_button = None
_pthread = threading.Thread(name='placeholder-thread')
_printers = []

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
    _update_lock.acquire()
    if isinstance(_rows[row], grid.GridRow):
        _rows[row].update(name, black, cyan, magenta, yellow)
    else:
        _rows[row].grid_forget()
        _rows[row] = grid.GridRow(scroll_win.scrollwindow, row, name, black, cyan, magenta, yellow)
    _update_lock.release()

def UpdatePrinterGuiMsg(row, msg):
    _update_lock.acquire()
    _rows[row].grid_forget()
    #header is grid row 0
    _rows[row] = grid.GridMsgRow(scroll_win.scrollwindow, row+1, msg)
    _update_lock.release()

def ClearLabels():
    for row, i in enumerate(_rows[1:]):
        _update_lock.acquire()
        if isinstance(_rows[i], grid.GridRow):
            _rows[row].clear()
        else:
            _rows[row].grid_forget()
        _update_lock.release()

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
    '''
    printer_group = pg.PrinterGroup()

    lib_color_printer = ps.PrinterSamsungColor('Library Color', '172.19.3.4')
    lib_bw_printer = ps.PrinterSamsungBW('Library B&W', '172.19.3.1')
    vva_printer = ps.PrinterSamsungBW('VVA', '172.19.3.14')
    lib_copier = ps.PrinterRicohBW('Library Copier', '172.16.3.8')
    office_copier = ps.PrinterRicohColor('Office Copier', '172.25.10.5')

    printer_group.append(lib_color_printer)
    printer_group.append(lib_bw_printer)
    printer_group.append(vva_printer)
    printer_group.append(lib_copier)
    printer_group.append(office_copier)

    printer_group.query()

    for p in printer_group:
        print(p)

    '''
    core = ps.SnmpCore()

    p0 = pr.PrinterBW('RHS VVA BW', '172.19.3.14')
    p0.query(core)

    print("name: {} error: {}".format(p0.name, p0.error_state))
    if p0.cyan:
        print("cyan: {}".format(p0.cyan))

    root.mainloop()


