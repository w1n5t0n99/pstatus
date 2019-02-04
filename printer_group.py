import printer_snmp as pr

class PrinterGroup:
    ''' collection of printers sharing a snmp core'''

    def __init__(self):
        self.snmp_core = pr.SnmpCore()
        self.printers = []

    def append(self, printer):
        self.printers.append(printer)

    def remove(self, printer):
        self.printers.remove(printer)

    def query(self):
        for p in self.printers:
            p.query(self.snmp_core)

    def __iter__(self):
        return iter(self.printers)

    def __next__(self):
        return next(self.printers)


