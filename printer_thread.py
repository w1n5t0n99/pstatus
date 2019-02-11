import threading
import printer as pr
import printer_frame as pf


class PrinterThread(threading.Thread):
    '''threading class for printer objects'''

    def __init__(self, printer, row, printer_frame, group=None, target=None, name=None):
        super(PrinterThread, self).__init__(group=group, target=target, name=name)
        self._printer = printer
        self._row = row
        self._printer_frame = printer_frame


    def run(self):
        try:
            self._printer.query()
        except:
            self._printer.clear()

        self._printer_frame.update_row(self._row)



