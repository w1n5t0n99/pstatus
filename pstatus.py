from tkinter import *
import tkinter.messagebox
import threading
import functools

import printer_db as db
import printer as pr
import copier as cp
import printer_frame as pf

printers = []
printer_button_col = []
printer_label_col = []

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
    except:
        printer.clear()


def update_if_thread_finished(printer_threads, printer_frame):
    alive = True
    while alive == True:
        i = 0
        for p in printer_threads:
            cur_alive = False
            if p.is_alive():
                cur_alive = True
            else:
                printer_frame.update_row(i)

            i+=1
        alive = cur_alive



if __name__ == "__main__":

    pr_text = db.LoadDB('printers.txt')
    printers = create_printers(pr_text)
    printer_threads = []

    for p in printers:
        printer_threads.append(threading.Thread(target=query_printer, args=(p,)))

    root = Tk()
    root.title("printer status")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    # Create & Configure frame
    main_frame = Frame(root)
    main_frame.grid(row=0, column=0, sticky=N + S + E + W)
    main_frame.grid_rowconfigure(0, weight=0)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight = 1)
    main_frame.grid_rowconfigure(2, weight=0)


    # main frame children ===============================================
    label = Label(main_frame, text="Printers", bg='gray')
    label.grid(row=0, column=0, pady=(5, 0), padx=(5,5), sticky=E + N + W + S)

    printer_frame = pf.PrinterFrame(main_frame, 1, 0)
    printer_frame.set_printers(printers)

    ref_button = Button(main_frame, text="Refresh", bg='light gray', command=printer_frame.update_printers)
    ref_button.grid(row=2, column=0, pady=(5, 0), padx=(5, 0), sticky=W)

    for p in printer_threads:
        p.start()
  #  for p in printer_threads:
  #     p.join()

    printer_frame.update_printers()

    root.after(8000, printer_frame.update_printers)
    root.mainloop()