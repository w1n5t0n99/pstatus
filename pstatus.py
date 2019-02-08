from tkinter import *
import tkinter.messagebox
import threading
import functools

import printer_db as db
import printer as pr
import copier as cp

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


def create_printer_name_column(printers, frame):
    prows = [Button() for p in printers]

    i = 0
    for p in printers:
        prows[i] = Button(frame, text=("{}".format(p.name)), command= functools.partial(printer_detail_mb, i))
        prows[i].grid(row=i, column=0, sticky=N + S + E + W)
        frame.grid_rowconfigure(i, weight=1)
        i+=1

    return prows


def create_printer_info_column(printers, frame):
    prows = [Label() for p in printers]

    i = 0
    for p in printers:
        if p.black is None:
            prows[i] = Label(frame, text="ERROR")
        elif p.cyan is not None:
            prows[i] = Label(frame, text="b: {} c: {} m: {} y : {}".format(p.black, p.cyan, p.magenta, p.yellow))
        else:
            prows[i] = Label(frame, text="b: {}".format(p.black))

        prows[i].grid(row=i, column=1, sticky=N + S + E + W)
        i += 1

    return prows



def resize_printer_frame(frame, name_column, info_column, num_to_show):

    if len(name_column) != len(info_column):
        raise ValueError

    if len(name_column) <= num_to_show:
        n = len(name_column)
    else:
        n = num_to_show

    first_n_columns_width = name_column[0].winfo_width() + info_column[0].winfo_width()
    first_n_rows_height = 0

    for i in range(0, n):
        first_n_rows_height += name_column[i].winfo_height()

    frame.config(width=first_n_columns_width + vsb.winfo_width(), height=first_n_rows_height)


def refresh_printer_row(row):
    p = printers[row]
    if p.cyan is not None:
        printer_label_col[row].config( text="b: {} c: {} m: {} y : {}".format(p.black, p.cyan, p.magenta, p.yellow))
    else:
        printer_label_col[row].config(text="b: {}".format(p.black))


def printer_detail_mb(row):
    p = printers[row]

    if p.black is None:
        msg = "ERROR"
    elif p.cyan is None:
        msg = "black: {}\nfuser: {}\ntray 1 roller: {}\ntray 1 torque limiter: {}\nerror state: {}".format(p.black,
                                                                                                           p.fuser,
                                                                                                           p.tr1_roller,
                                                                                                           p.tr1_torque_limiter,
                                                                                                           p.error_state)
    else:
        msg = "black: {} cyan: {} magenta: {} yellow: {}\nfuser: {}\ntray 1 roller: {}\ntransfer belt: {}\nerror state: {}".format(p.black,
                                                                                                                                   p.cyan,
                                                                                                                                   p.magenta,
                                                                                                                                   p.yellow,
                                                                                                                                   p.fuser,
                                                                                                                                   p.tr1_roller,
                                                                                                                                   p.tr_belt,
                                                                                                                                   p.error_state)

    tkinter.messagebox.showinfo(title="{}".format(p.name), message=msg)

def set_scroll_region(printer_col, canvas):
    scroll_height = 0
    for p in printer_col:
        scroll_height += p.winfo_height()

    canvas.config(scrollregion=(0, 0, 0, scroll_height))


def frame_width(event):
    canvas_width = event.width
    canvas.itemconfigure(canvas_window, width=canvas_width)


def on_frame_configure(event):
    #canvas.config(scrollregion=canvas.bbox("all"))
    set_scroll_region(printer_button_col, canvas)


if __name__ == "__main__":

    pr_text = db.LoadDB('printers.txt')
    printers = create_printers(pr_text)
    printer_threads = []

    for p in printers:
        printer_threads.append(threading.Thread(target=query_printer, args=(p,)))

    for p in printer_threads:
        p.start()
    for p in printer_threads:
        p.join()

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

    ref_button = Button(main_frame, text="Refresh", bg='light gray')
    ref_button.grid(row=2, column=0, pady=(5, 0), padx=(5, 0), sticky=W)

    frame_canvas = Frame(main_frame, bg="green")
    frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky=E + N + W + S)
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)

    # frame canvas children =====================================
    canvas = Canvas(frame_canvas)
    canvas.grid(row=0, column=0, sticky=E + N + W + S)
    canvas.grid_rowconfigure(0, weight=1)
    canvas.grid_columnconfigure(0, weight=1)

    vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky=N + S)

    # canvas children ==============================================

    printers_frame = Frame(canvas, bg="blue")
    printers_frame.columnconfigure(0, weight=1)
    printers_frame.columnconfigure(1, weight=1)

    canvas_window = canvas.create_window((0, 0), window=printers_frame, anchor=N + W)

    canvas.bind('<Configure>', frame_width)
    #printers_frame.bind('<Configure>', on_frame_configure)

    printer_button_col = create_printer_name_column(printers, printers_frame)
    printer_label_col = create_printer_info_column(printers, printers_frame)

    resize_printer_frame(printers_frame, printer_label_col, printer_button_col, 12)
    printers_frame.update_idletasks()

    set_scroll_region(printer_button_col, canvas)
    canvas.config(yscrollcommand=vsb.set)

    root.mainloop()