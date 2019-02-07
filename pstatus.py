import tkinter as tk
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
    prows = [tk.Button() for p in printers]

    i = 0
    for p in printers:
        prows[i] = tk.Button(frame, text=("{}".format(p.name)), command= functools.partial(printer_detail_mb, i))
        prows[i].grid(row=i, column=0, sticky='news')
        i+=1

    return prows


def create_printer_info_column(printers, frame):
    prows = [tk.Label() for p in printers]

    i = 0
    for p in printers:
        if p.black is None:
            prows[i] = tk.Label(frame, text="ERROR")
        elif p.cyan is not None:
            prows[i] = tk.Label(frame, text="b: {} c: {} m: {} y : {}".format(p.black, p.cyan, p.magenta, p.yellow))
        else:
            prows[i] = tk.Label(frame, text="b: {}".format(p.black))

        prows[i].grid(row=i, column=1, sticky='news')
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
        #first_n_columns_width += name_column[i].winfo_width()
        first_n_rows_height += name_column[i].winfo_height()

    frame.config(width=first_n_columns_width + vsb.winfo_width(), height=first_n_rows_height)


def refresh_printer_row(row):
    p = printers[row]
    if p.cyan is not None:
        printer_label_col[row].config( text="b: {} c: {} m: {} y : {}".format(p.black, p.cyan, p.magenta, p.yellow))
    else:
        printer_label_col[row].config(text="b: {}".format(p.black))


def printer_detail_mb(row):
    print(row)
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

    tk.messagebox.showinfo(title="{}".format(p.name), message=msg)



if __name__ == "__main__":

    pr_text = db.LoadDB('printers.txt')
    printers = create_printers(pr_text)
    printer_threads = []

    for p in printers:
        printer_threads.append(threading.Thread(target=query_printer, args=(p,)))

    for p in printer_threads:
        p.start()
        p.join()

    root = tk.Tk()
    root.title = 'printer status'
    root.grid_rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frame_main = tk.Frame(root, bg="gray")
    frame_main.grid(sticky='news')

    label1 = tk.Label(frame_main, text="Printers", bg="gray")
    label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')

    ref_button = tk.Button(frame_main, text="Refresh")
    ref_button.grid(row=2, column=0, pady=(5, 0), sticky='nw')

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(frame_main)
    frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)

    # Add a canvas in that frame
    canvas = tk.Canvas(frame_canvas, bg="yellow")
    canvas.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to the canvas
    vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)

    # Create a frame to contain the buttons
    frame_buttons = tk.Frame(canvas, bg="blue")
    canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

    printer_button_col = create_printer_name_column(printers, frame_buttons)
    printer_label_col = create_printer_info_column(printers, frame_buttons)

    # Update buttons frames idle tasks to let tkinter calculate buttons sizes
    frame_buttons.update_idletasks()

    # Resize the canvas frame to show exactly 5 buttons and the scrollbar
    resize_printer_frame(frame_canvas, printer_button_col, printer_label_col, 8)
    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))

    # Launch the GUI
    root.mainloop()

