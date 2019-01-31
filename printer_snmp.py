from pysnmp.hlapi import *
from collections import namedtuple

class Printer:
    def __init__(self, name, model, ip):
        self.name = name
        self.model = model
        self.ip = ip

class Clp775Info:
    oid_yellow = '.1.3.6.1.2.1.43.11.1.1.9.1.1'
    oid_magenta = '.1.3.6.1.2.1.43.11.1.1.9.1.2'
    oid_cyan = '.1.3.6.1.2.1.43.11.1.1.9.1.3'
    oid_black = '.1.3.6.1.2.1.43.11.1.1.9.1.4'
    oid_tr_belt = '.1.3.6.1.2.1.43.11.1.1.9.1.5'
    oid_fuser = '.1.3.6.1.2.1.43.11.1.1.9.1.6'
    oid_mp_roller = '.1.3.6.1.2.1.43.11.1.1.9.1.7'
    oid_tr1_roller = '.1.3.6.1.2.1.43.11.1.1.9.1.8'
    oid_tr1_rroller = '.1.3.6.1.2.1.43.11.1.1.9.1.9'
    oid_dust_cleaning_kit = '.1.3.6.1.2.1.43.11.1.1.9.1.10'

    oid_yellow_str = '.1.3.6.1.2.1.43.11.1.1.6.1.1'
    oid_magenta_str = '.1.3.6.1.2.1.43.11.1.1.6.1.2'
    oid_cyan_str = '.1.3.6.1.2.1.43.11.1.1.6.1.3'
    oid_black_str = '.1.3.6.1.2.1.43.11.1.1.6.1.4'
    oid_tr_belt_str = '.1.3.6.1.2.1.43.11.1.1.6.1.5'
    oid_fuser_str = '.1.3.6.1.2.1.43.11.1.1.6.1.6'
    oid_mp_roller_str = '.1.3.6.1.2.1.43.11.1.1.6.1.7'
    oid_tr1_roller_str = '.1.3.6.1.2.1.43.11.1.1.6.1.8'
    oid_tr1_rroller_str = '.1.3.6.1.2.1.43.11.1.1.6.1.9'
    oid_dust_cleaning_kit_str = '.1.3.6.1.2.1.43.11.1.1.6.1.10'

    oid_yellow_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.1 '
    oid_magenta_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.2'
    oid_cyan_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.3'
    oid_black_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.4'
    oid_tr_belt_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.5'
    oid_fuser_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.6'
    oid_mp_roller_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.7'
    oid_tr1_roller_capcity = '.1.3.6.1.2.1.43.11.1.1.8.1.8'
    oid_tr1_rroller_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.9'
    oid_dust_cleaning_kit_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.10'

    def __init__(self, yellow, magenta, cyan, black, tr_belt, fuser, mp_roller, tr1_roller, tr1_rroller, dust_clean_kit):
        self.yellow = yellow
        self.magenta = magenta
        self.cyan = cyan
        self.black = black
        self.tr_belt = tr_belt
        self.fuser = fuser
        self.mp_roller = mp_roller
        self.tr1_roller = tr1_roller
        self.tr1_rroller = tr1_rroller
        self.dust_clean_kit = dust_clean_kit


class PrinterSnmp:
    def __init__(self):
        self._engine = SnmpEngine()
        self._com_data = CommunityData('public')
        self._context_data = ContextData()

