import tkinter as tk
import threading

import printer_db
import printer_async_query
import printer_query
import grid


_update_lock = threading.Lock()

_header = None
_rows = []
_root = None
_ref_button = None
_pthread = threading.Thread(name='placeholder-thread')

def InitPrinterGui(printers):
    _header = grid.GridHeaderRow(root)

    if printers.empty():
        _rows.append(grid.GridMsgRow(root, 1, 'Printers not found, make sure file named printers.txt\nin same directory as .exe'))
        return

    r = 1
    for p in list(printers.queue):

        _rows.append(grid.GridRow(root, r, p[1], ' ', ' ', ' ', ' '))
        r +=1

    _ref_button = tk.Button(root, text='Refresh', width=6, command=RunUpdateThread)
    _ref_button.grid(row=r, column=4)

def UpdatePrinterGui(row, name, black, cyan, magenta, yellow):
    _update_lock.acquire()
    _rows[row].grid_forget()
    #header is grid row 0
    _rows[row] = grid.GridRow(root, row+1, name, black, cyan, magenta, yellow)
    _update_lock.release()

def UpdatePrinterGuiMsg(row, msg):
    _update_lock.acquire()
    _rows[row].grid_forget()
    #header is grid row 0
    _rows[row] = grid.GridMsgRow(root, row+1, msg)
    _update_lock.release()


def AsyncUpdateLabels(printers):
    ps_thread = printer_async_query.PStatusThread('status-thread', printers, UpdatePrinterGui)
    ps_thread.start()
    ps_thread.join()
    '''    
    while ps_thread.is_alive():
        p = printer_async_query.query_results.get()
        if p is not None:
            if p.status is not 'ok':
                _rows[p.row].grid_forget()
                _rows[p.row] = grid.GridMsgRow(root, p.row + 1, p.status)
            else:
                _rows[p.row].grid_forget()
                _rows[p.row] = grid.GridRow(root, p.row + 1, p.name, p.black, p.cyan, p.magenta, p.yellow)   
    '''

def UpdateLabels(printers):
    for p in list(printers.queue):
        qr = printer_query.QueryPrinter(p)
        if qr.status == 'ok':
            UpdatePrinterGui(qr.row, qr.name, qr.black, qr.cyan, qr.magenta, qr.yellow)
        else:
            UpdatePrinterGuiMsg(qr.row, qr.status)

def RunUpdateThread():
    global _pthread
    if _pthread.is_alive() is not True:
        _pthread = threading.Thread(name='update_thread', target=UpdateLabels, args=(printers,), daemon=True)
        _pthread.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Printer Status')
    root.minsize(width=375, height=500)
    root.resizable(width=False, height=False)

    printers = printer_db.LoadDBQueue('printers.txt')
    printer_rows = []

    InitPrinterGui(printers)

    '''
    if printers != None:
        threading.Thread(name='update_thread', target=AsyncUpdateLabels, args=(printers,), daemon=True).start()
    '''
    if _pthread.is_alive() is not True:
        print('got here')
        _pthread = threading.Thread(name='update_thread', target=UpdateLabels, args=(printers,), daemon=True)
        _pthread.start()

    root.mainloop()


