from tkinter import *
import os
import sys

import printer_thread
import printer_db as db
import printer as pr
import copier as cp
import printer_frame as pf
import printer_icon
#need to fix pyinstaller race condition
import encodings.idna

_db_file = "printers.txt"
_printers = []
_printer_threads = []
_printer_frame = None
_status_label = None
_ref_button = None


def _create_printers(printers_text):
    printers = []
    for p in printers_text:
        if p[2] == 'bw':
            printers.append(pr.PrinterBW(p[1], p[0]))
        elif p[2] == 'color':
            printers.append(pr.PrinterColor(p[1], p[0]))
        elif p[2] == 'hp_color':
            printers.append(pr.PrinterHpColor(p[1], p[0]))

    return printers

def _load_and_create_printers():
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    _db_path = os.path.join(application_path, _db_file)

    global _printers
    try:
        pr_text = db.LoadDB(_db_path)
        _printers = _create_printers(pr_text)
    except Exception:
        _status_label.config(text="Unable to Load Printers")
        _printers = []


def _printer_threads_active():
    active = False
    for p in _printer_threads:
        if p.is_alive():
            active = True

    return active


def _refresh_printers():
    if _printer_threads_active():
        return

    _printer_threads.clear()
    _printer_frame.clear_printers_info()
    i = 0
    for p in _printers:
        _printer_threads.append(printer_thread.PrinterThread(p, i, _printer_frame))
        i += 1

    for p in _printer_threads:
        p.start()


if __name__ == "__main__":

    root = Tk()
    root.title("RCPS Printers")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.iconbitmap(default=printer_icon.get_icon_file())
    # Create & Configure frame
    main_frame = Frame(root)
    main_frame.grid(row=0, column=0, sticky=N + S + E + W)
    main_frame.grid_rowconfigure(0, weight=0)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight = 1)
    main_frame.grid_rowconfigure(2, weight=0)


    # main frame children ===============================================
    _status_label = Label(main_frame, text="Printers", bg='gray')
    _status_label.grid(row=0, column=0, pady=(5, 0), padx=(5, 5), sticky=E + N + W + S)

    _load_and_create_printers()

    _printer_frame = pf.PrinterFrame(main_frame, 1, 0)
    _printer_frame.set_printers(_printers)

    _ref_button = Button(main_frame, text="Refresh", bg='light gray', command=_refresh_printers)
    _ref_button.grid(row=2, column=0, pady=(5, 0), padx=(5, 0), sticky=W)

    i = 0
    for p in _printers:
        _printer_threads.append(printer_thread.PrinterThread(p, i, _printer_frame))
        i+=1

    for p in _printer_threads:
        p.start()

    #root.after(8000, printer_frame.update_printers)
    root.mainloop()