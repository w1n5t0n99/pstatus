from tkinter import *
import tkinter.messagebox

import printer as pr
import functools

def _generate_detail_str(printer):
    p = printer
    # all printers should have black toner
    if p.black is None:
        return "ERROR"


    if isinstance(printer, pr.PrinterBW):
        msg = "{}\nBlack: {}\nFuser: {}\nTray 1 Roller: {}\nTray 1 Torque Limiter: {}\nError State: {}".format(
            p.info,
            p.black,
            p.fuser,
            p.tr1_roller,
            p.tr1_torque_limiter,
            p.error_state)
    elif isinstance(printer, pr.PrinterColor):
        msg = "{}\nBlack: {} Cyan: {} Magenta: {} Yellow: {}\nFuser: {}\n" \
              "Tray 1 Roller: {}\nTransfer Belt: {}\nDust Cleaning Kit: {}\n" \
              "Error State: {}".format(
            p.info,
            p.black,
            p.cyan,
            p.magenta,
            p.yellow,
            p.fuser,
            p.tr1_roller,
            p.tr_belt,
            p.dust_ck,
            p.error_state)
    elif isinstance(printer, pr.PrinterHpColor):
        msg = "{}\nBlack: {} Cyan: {} Magenta: {} Yellow: {}\nFuser: {}".format(
            p.info,
            p.black,
            p.cyan,
            p.magenta,
            p.yellow,
            p.fuser)

    return msg

def _is_printer_warning(printer):
    p = printer
    # all printers should have black toner
    if p.black is None:
        return False

    if isinstance(printer, pr.PrinterColor):
        if (p.black == 0) or (p.cyan == 0) or (p.magenta == 0) or (p.yellow == 0):
            return True
        if p.error_state is not None:
            return True

    elif isinstance(printer, pr.PrinterBW):
        if p.black == 0:
            return True
        if p.error_state is not None:
            return True

    elif isinstance(printer, pr.PrinterHpColor):
        if (p.black == 0) or (p.cyan == 0) or (p.magenta == 0) or (p.yellow == 0):
            return True


class PrinterFrame:
    '''tkinter frame to display printer objects'''

    def __init__(self, parent, grid_row, grid_col):
        self._printer_frame = Frame(parent)
        self._printer_frame.grid(row=grid_row, column=grid_col, pady=(5, 0), sticky=E + N + W + S)
        self._printer_frame.grid_rowconfigure(0, weight=1)
        self._printer_frame.grid_columnconfigure(0, weight=1)

        self._printer_canvas = Canvas(self._printer_frame)
        self._printer_canvas.grid(row=0, column=0, sticky=E + N + W + S)
        self._printer_canvas.grid_rowconfigure(0, weight=1)
        self._printer_canvas.grid_columnconfigure(0, weight=1)

        self.vsb = Scrollbar(self._printer_frame, orient="vertical", command=self._printer_canvas.yview)
        self.vsb.grid(row=0, column=1, sticky=N + S)

    @staticmethod
    def _from_rgb(rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb

    def _set_scroll_region(self):
        scroll_height = 0
        for p in self._printer_rows:
            scroll_height += p[0].winfo_height()

        self._printer_canvas.config(scrollregion=(0, 0, 0, scroll_height))

    def _set_frame_width(self, event):
        canvas_width = event.width
        self._printer_canvas.itemconfigure(self._printer_canvas_window, width=canvas_width)

    def _create_printer_rows(self):
        f = self._printer_list_frame
        self._printer_rows = [(Button(f), Label(f)) for p in self._printers]

        i = 0
        for p in self._printers:

            if i % 2 == 0:
                bg_color = self._from_rgb((180, 180, 180))
            else:
                bg_color = self._from_rgb((200, 200, 200))

            self._printer_rows[i][0].config(text=("{}".format(p.name)),
                                            command=functools.partial(self._printer_detail_mb, i))

            self._printer_rows[i][0].grid(row=i, column=0, padx=(15, 0), sticky=N + S + E + W)
            f.grid_rowconfigure(i, weight=1)

            if p.black is None:
                self._printer_rows[i][1].config(text=" ", bg=bg_color)
            elif p.cyan is not None:
                self._printer_rows[i][1].config(text="B: {} C: {} M: {} Y: {}".format(p.black, p.cyan, p.magenta, p.yellow),  bg=bg_color,)
            else:
                self._printer_rows[i][1].config(text="B: {}".format(p.black),  bg=bg_color,)

            self._printer_rows[i][1].grid(row=i, column=1, padx=(0, 15), sticky=N + S + E + W)

            i += 1

    def _printer_detail_mb(self, row):
        p = self._printers[row]
        msg = _generate_detail_str(p)
        tkinter.messagebox.showinfo(title="{}".format(p.name), message=msg)

    def _resize_printer_frame(self, num_to_show):

        first_n_rows_height = 300
        first_n_columns_width = 400

        if not self._printer_rows:
            self._printer_canvas.config(width=first_n_columns_width + self.vsb.winfo_width(),
                                        height=first_n_rows_height)
            return

        if len(self._printer_rows) <= num_to_show:
            n = len(self._printer_rows)
        else:
            n = num_to_show

        first_n_rows_height = 0
        first_n_columns_width = 0
        first_n_columns_width = self._printer_rows[0][0].winfo_width() + self._printer_rows[0][1].winfo_width()

        for i in range(0, n):
            first_n_rows_height += self._printer_rows[i][0].winfo_height()

        self._printer_canvas.config(width=first_n_columns_width + self.vsb.winfo_width(), height=first_n_rows_height)

    def set_printers(self, printers):
        self._printers = printers
        self._printer_list_frame = Frame(self._printer_canvas)
        self._printer_list_frame.columnconfigure(0, weight=1)
        self._printer_list_frame.columnconfigure(1, weight=1)

        self._printer_canvas_window = self._printer_canvas.create_window((0, 0), window=self._printer_list_frame, anchor=N + W)
        self._printer_canvas.bind('<Configure>', self._set_frame_width)

        self._create_printer_rows()
        self._printer_frame.update()

        self._resize_printer_frame(14)
        self._printer_canvas.update_idletasks()
        self._set_scroll_region()
        self._printer_canvas.config(yscrollcommand=self.vsb.set)

    def clear_printers_info(self):
        for p in self._printers:
            p.clear()

        for p in self._printer_rows:
            p[1].config(text=" ")
            p[0].config(fg="black")


    def update_printers(self):
        for i in range(0, len(self._printer_rows)):
            self.update_row(i)

    def update_row(self, row):
        if row >= len(self._printer_rows):
            assert IndexError

        p = self._printers[row]

        if _is_printer_warning(p):
            self._printer_rows[row][0].config(fg="red")
        else:
            self._printer_rows[row][0].config(fg="black")

        if p.black is None:
            self._printer_rows[row][1].config(text="ERROR")
        elif p.cyan is not None:
            self._printer_rows[row][1].config(text="B: {} C: {} M: {} Y: {}".format(p.black, p.cyan, p.magenta,
                                                                                  p.yellow))
        else:
            self._printer_rows[row][1].config(text="B: {}".format(p.black))


