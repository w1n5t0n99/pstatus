import tkinter as tk
import threading

import printer_db as db
import printer as pr
import copier as cp

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
            print('{} b: {} err: {}'.format(printer.name, printer.black,
                                            printer.error_state if printer.error_state else "no error"))
        else:
            print('{} b: {} c: {} m: {} y : {} err: {}'.format(printer.name, printer.black, printer.cyan,
                                                       printer.magenta, printer.yellow,
                                                       printer.error_state if printer.error_state else "no error"))

    except:
        print('ERROR: {}'.format(printer.name))

def create_printer_rows(printers, rows_frame):
    prows = [tk.Button() for p in printers]

    i = 0
    for p in printers:
        prows[i] = tk.Button(rows_frame, text=("{}".format(p.name)))
        prows[i].grid(row=i, column=0, sticky='news')
        i+=1

    return prows


if __name__ == "__main__":

    pr_text = db.LoadDB('printers.txt')
    printers = create_printers(pr_text)
    printer_threads = []

    for p in printers:
        printer_threads.append(threading.Thread(target=query_printer, args=(p, )))

    for p in printer_threads:
        p.start()
        #p.join()

    c = cp.CopierColor('Office Copier', '172.19.3.16')
    c.query()

    print('name: {} b: {} c: {} m: {} y: {}\nhistory: {}'.format(c.name, c.black, c.cyan, c.magenta, c.yellow, c.history))

    '''
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frame_main = tk.Frame(root, bg="gray")
    frame_main.grid(sticky='news')

    label1 = tk.Label(frame_main, text="Label 1", fg="green")
    label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')

    label2 = tk.Label(frame_main, text="Label 2", fg="blue")
    label2.grid(row=1, column=0, pady=(5, 0), sticky='nw')

    label3 = tk.Label(frame_main, text="Label 3", fg="red")
    label3.grid(row=3, column=0, pady=5, sticky='nw')

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(frame_main)
    frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
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

    # Add 9-by-5 buttons to the frame
    rows = 9
    columns = 5
    buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
    for i in range(0, rows):
        for j in range(0, columns):
            buttons[i][j] = tk.Button(frame_buttons, text=("%d,%d" % (i + 1, j + 1)))
            buttons[i][j].grid(row=i, column=j, sticky='news')

    # Update buttons frames idle tasks to let tkinter calculate buttons sizes
    frame_buttons.update_idletasks()

    # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
    first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
    first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
    frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                        height=first5rows_height)

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))

    # Launch the GUI
    root.mainloop()

    '''

    printer_grid_rows = []

    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frame_main = tk.Frame(root, bg="gray")
    frame_main.grid(sticky='news')

    label1 = tk.Label(frame_main, text="Printers", fg="green")
    label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(frame_main)
    frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
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

    printer_grid_rows = create_printer_rows(printers, frame_buttons)

    # Update buttons frames idle tasks to let tkinter calculate buttons sizes
    frame_buttons.update_idletasks()

    # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
    first5columns_width = sum([printer_grid_rows[j].winfo_width() for j in range(0, 5)])
    first5rows_height = sum([printer_grid_rows[i].winfo_height() for i in range(0, 5)])
    frame_canvas.config(width=first5columns_width + vsb.winfo_width(), height=first5rows_height)

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))

    # Launch the GUI
    root.mainloop()

    '''
    1.3.6.1.2.1.43.9.2.1.1 (prtOutputIndex): output capacity (0 or more; 0 means out of paper)
    1.3.6.1.2.1.25.3.5.1.2 (hrPrinterDetectedErrorState): octet string of
    length 2 (2 bytes); if bits below are set, corresponding error condition is in effect:
     lowPaper              0
     noPaper               1
     lowToner              2
     noToner               3
     doorOpen              4
     jammed                5
     offline               6
     serviceRequested      7
     inputTrayMissing      8
     outputTrayMissing     9
     markerSupplyMissing  10
     outputNearFull       11
     outputFull           12
     inputTrayEmpty       13
     overduePreventMaint  14
     
    If both bytes are zero, no error condition detected
    
    Bits are numbered starting with the most significant
      bit of the first byte being bit 0, the least
      significant bit of the first byte being bit 7, the
      most significant bit of the second byte being bit 8,
      and so on.  A one bit encodes that the condition was
      detected, while a zero bit encodes that the condition
      was not detected.
    '''