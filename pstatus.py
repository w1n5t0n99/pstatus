import tkinter as tk
import threading
import queue

import printer_db
import printer_async_query
import printer_query
import grid
import scroll_frame

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

    _ref_button = tk.Button(root, text='Refresh', width=6, command=RunUpdateThread)
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


def AsyncUpdateLabels(printers):
    ps_thread = printer_async_query.PStatusThread('status-thread', printers, UpdatePrinterGui)
    ps_thread.start()
    ps_thread.join()


def UpdateLabels(printers):
    for p in list(printers.queue):
        qr = printer_query.QueryPrinter(p)
        if qr.status == 'ok':
            UpdatePrinterGui(qr.row + _row_offset, qr.name, qr.black, qr.cyan, qr.magenta, qr.yellow)
        else:
            UpdatePrinterGuiMsg(qr.row + _row_offset, qr.status)

def ClearLabels():
    for row, i in enumerate(_rows[1:]):
        _update_lock.acquire()
        if isinstance(_rows[i], grid.GridRow):
            _rows[row].clear()
        else:
            _rows[row].grid_forget()
        _update_lock.release()

def RunUpdateThread():
    global _pthread
    if _pthread.is_alive() is not True:
        ClearLabels()
        _pthread = threading.Thread(name='update_thread', target=UpdateLabels, args=(_printers,), daemon=True)
        _pthread.start()


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
    if printers != None:
        threading.Thread(name='update_thread', target=AsyncUpdateLabels, args=(printers,), daemon=True).start()
    '''

    '''
    if _pthread.is_alive() is not True:
        _pthread = threading.Thread(name='update_thread', target=UpdateLabels, args=(_printers,), daemon=True)
        _pthread.start()

    '''

    _engine = SnmpEngine()
    _com_data = CommunityData('public')
    _context_data = ContextData()

    error_indication, error_status, error_index, var_binds = next(
        getCmd(_engine,
               _com_data,
               UdpTransportTarget(('172.16.3.12', 161)),
               _context_data,
               ObjectType(ObjectIdentity('1.3.6.1.2.1.43.8.2.1.9.1.1')),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.43.8.2.1.10.1.1'))
               ))

    if error_indication:
        print(error_indication)
    elif error_status:
        print('{} at {}'.format(error_status.prettyPrint(), error_index and var_binds[-1][int(error_index) - 1] or '?'))
    else:
        print('max: {} level: {}'.format(var_binds[0][1], var_binds[1][1]))

    root.mainloop()


#  1.3.6.1.2.1.43.6.1.1.3.1.1 = printer cover status
#  1.3.6.1.2.1.43.16.5.1.2.1.1 = text currently shown on printers console display
#  1.3.6.1.2.1.43.8.2.1.18.1.1 = description of tray e.g. tray 1
#  1.3.6.1.2.1.43.8.2.1.18.1.2 = description of tray e.g. tray 2
#  1.3.6.1.2.1.43.8.2.1.9.1.1 = max capacity of paper tray
#  1.3.6.1.2.1.43.8.2.1.10.1.1 = current capacity of paper tray