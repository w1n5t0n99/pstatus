import printer_snmp as ps
from collections import namedtuple

printer_tuple = namedtuple('printers', ['model', 'printer'])

class PrintersWatcher:
    def __init__(self):
        self.snmp_core = ps.SnmpCore()
        self.printers = []

    def add_printer(self, name, model, ip):
        self.printers.append(printer_tuple(model=model, printer=))

