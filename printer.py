from pysnmp.hlapi import *
from abc import ABCMeta, abstractmethod

class SnmpCore:
    def __init__(self):
        self.engine = SnmpEngine()
        self.com_data = CommunityData('public')
        self.context_data = ContextData()

class IPrinter(metaclass=ABCMeta):
    '''base class for printers'''

    _oid_info = '.1.3.6.1.2.1.1.1.0'
    _oid_error = '.1.3.6.1.2.1.25.3.5.1.2.1'

    def __init__(self, name, ip):
        self.core = SnmpCore()
        self.name = name
        self.ip = ip
        self.error_state = None
        self.info = None
        self.black = None
        self.cyan = None
        self.magenta = None
        self.yellow = None
        self.fuser = None
        self.tr_belt = None
        self.mp_roller = None
        self.tr1_roller = None
        self.tr1_rroller = None
        self.dust_ck = None
        self.tr1_torque_limiter = None

    def clear(self):
        self.error_state = None
        self.info = None
        self.black = None
        self.cyan = None
        self.magenta = None
        self.yellow = None
        self.fuser = None
        self.tr_belt = None
        self.mp_roller = None
        self.tr1_roller = None
        self.tr1_rroller = None
        self.dust_ck = None
        self.tr1_torque_limiter = None

    @abstractmethod
    def query(self):
        pass

    def _clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def _percentage(self, toner_level, max_capacity):
        level = int(toner_level / max_capacity * 100)
        return self._clamp(level, 0, 100)

    def _get_error_str(self, err):
        err_str = ''
        if err[1] & 0b00000001:
            err_str += ', service requested'
        if err[1] & 0b00000010:
            err_str += ', offline'
        if err[1] & 0b00000100:
            err_str += ', jammed'
        if err[1] & 0b00001000:
            err_str += ', door open'
        if err[1] & 0b00010000:
            err_str += ', no toner'
        if err[1] & 0b00100000:
            err_str += ', low toner'
        if err[1] & 0b01000000:
            err_str += ', no paper'
        if err[1] & 0b10000000:
            err_str += ', low paper'

        if err[0] & 0b00000001:
            err_str += ', unused bit'
        if err[0] & 0b00000010:
            err_str += ', overdue prevent maintenance'
        if err[0] & 0b00000100:
            err_str += ', input tray empty'
        if err[0] & 0b00001000:
            err_str += ', output full'
        if err[0] & 0b00010000:
            err_str += ', output near full'
        if err[0] & 0b00100000:
            err_str += ', marker supply missing'
        if err[0] & 0b01000000:
            err_str += ', output tray missing'
        if err[0] & 0b10000000:
            err_str += ', input tray missing'

        if err[0] == 0 and err[1] == 0:
            err_str = None

        return err_str


class PrinterBW(IPrinter):
    '''black and white printer object'''

    _oid_black = '.1.3.6.1.2.1.43.11.1.1.9.1.1'
    _oid_fuser = '.1.3.6.1.2.1.43.11.1.1.9.1.2'
    _oid_tr1_roller = '.1.3.6.1.2.1.43.11.1.1.9.1.3'
    _oid_tr1_torque_limiter = '.1.3.6.1.2.1.43.11.1.1.9.1.4'
    _oid_black_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.1'
    _oid_fuser_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.2'
    _oid_tr1_roller_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.3'
    _oid_tr1_torque_limiter_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.4'

    def __init__(self, name, ip):
        super(PrinterBW, self).__init__(name, ip)

    def query(self):
        error_indication, error_status, error_index, vals = next(
            getCmd(self.core.engine,
                   self.core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   self.core.context_data,
                   ObjectType(ObjectIdentity(self._oid_black)),
                   ObjectType(ObjectIdentity(self._oid_fuser)),
                   ObjectType(ObjectIdentity(self._oid_tr1_roller)),
                   ObjectType(ObjectIdentity(self._oid_tr1_torque_limiter)),
                   )
        )

        error_indication, error_status, error_index, vals_max = next(
            getCmd(self.core.engine,
                   self.core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   self.core.context_data,
                   ObjectType(ObjectIdentity(self._oid_black_capacity)),
                   ObjectType(ObjectIdentity(self._oid_fuser_capacity)),
                   ObjectType(ObjectIdentity(self._oid_tr1_roller_capacity)),
                   ObjectType(ObjectIdentity(self._oid_tr1_torque_limiter_capacity)),
                   ObjectType(ObjectIdentity(self._oid_error)),
                   ObjectType(ObjectIdentity(self._oid_info)),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        self.black = self._percentage(vals[0][1], vals_max[0][1])
        self.fuser = self._percentage(vals[1][1], vals_max[1][1])
        self.tr1_roller = self._percentage(vals[2][1], vals_max[2][1])
        self.tr1_torque_limiter = self._percentage(vals[3][1], vals_max[3][1])
        self.error_state = self._get_error_str((vals_max[4][1]).asNumbers())
        self.info = vals_max[5][1]

class PrinterColor(IPrinter):
    '''color printer object'''

    _oid_yellow = '.1.3.6.1.2.1.43.11.1.1.9.1.1'
    _oid_magenta = '.1.3.6.1.2.1.43.11.1.1.9.1.2'
    _oid_cyan = '.1.3.6.1.2.1.43.11.1.1.9.1.3'
    _oid_black = '.1.3.6.1.2.1.43.11.1.1.9.1.4'
    _oid_tr_belt = '.1.3.6.1.2.1.43.11.1.1.9.1.5'
    _oid_fuser = '.1.3.6.1.2.1.43.11.1.1.9.1.6'
    _oid_mp_roller = '.1.3.6.1.2.1.43.11.1.1.9.1.7'
    _oid_tr1_roller = '.1.3.6.1.2.1.43.11.1.1.9.1.8'
    _oid_tr1_rroller = '.1.3.6.1.2.1.43.11.1.1.9.1.9'
    _oid_dust_cleaning_kit = '.1.3.6.1.2.1.43.11.1.1.9.1.10'

    _oid_yellow_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.1 '
    _oid_magenta_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.2'
    _oid_cyan_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.3'
    _oid_black_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.4'
    _oid_tr_belt_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.5'
    _oid_fuser_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.6'
    _oid_mp_roller_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.7'
    _oid_tr1_roller_capcity = '.1.3.6.1.2.1.43.11.1.1.8.1.8'
    _oid_tr1_rroller_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.9'
    _oid_dust_cleaning_kit_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.10'

    def __init__(self, name, ip):
        super(PrinterColor, self).__init__(name, ip)

    def query(self):
        error_indication, error_status, error_index, vals = next(
            getCmd(self.core.engine,
                   self.core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   self.core.context_data,
                   ObjectType(ObjectIdentity(self._oid_yellow)),
                   ObjectType(ObjectIdentity(self._oid_magenta)),
                   ObjectType(ObjectIdentity(self._oid_cyan)),
                   ObjectType(ObjectIdentity(self._oid_black)),
                   ObjectType(ObjectIdentity(self._oid_tr_belt)),
                   ObjectType(ObjectIdentity(self._oid_fuser)),
                   ObjectType(ObjectIdentity(self._oid_mp_roller)),
                   ObjectType(ObjectIdentity(self._oid_tr1_roller)),
                   ObjectType(ObjectIdentity(self._oid_tr1_rroller)),
                   ObjectType(ObjectIdentity(self._oid_dust_cleaning_kit)),
                   )
        )

        error_indication, error_status, error_index, vals_max = next(
            getCmd(self.core.engine,
                   self.core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   self.core.context_data,
                   ObjectType(ObjectIdentity(self._oid_yellow_capacity)),
                   ObjectType(ObjectIdentity(self._oid_magenta_capacity)),
                   ObjectType(ObjectIdentity(self._oid_cyan_capacity)),
                   ObjectType(ObjectIdentity(self._oid_black_capacity)),
                   ObjectType(ObjectIdentity(self._oid_tr_belt_capacity)),
                   ObjectType(ObjectIdentity(self._oid_fuser_capacity)),
                   ObjectType(ObjectIdentity(self._oid_mp_roller_capacity)),
                   ObjectType(ObjectIdentity(self._oid_tr1_roller_capcity)),
                   ObjectType(ObjectIdentity(self._oid_tr1_rroller_capacity)),
                   ObjectType(ObjectIdentity(self._oid_dust_cleaning_kit_capacity)),
                   ObjectType(ObjectIdentity(self._oid_error)),
                   ObjectType(ObjectIdentity(self._oid_info)),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        self.yellow = self._percentage(vals[0][1], vals_max[0][1])
        self.magenta = self._percentage(vals[1][1], vals_max[1][1])
        self.cyan = self._percentage(vals[2][1], vals_max[2][1])
        self.black = self._percentage(vals[3][1], vals_max[3][1])
        self.tr_belt = self._percentage(vals[4][1], vals_max[4][1])
        self.fuser = self._percentage(vals[5][1], vals_max[5][1])
        self.mp_roller = self._percentage(vals[6][1], vals_max[6][1])
        self.tr1_roller = self._percentage(vals[7][1], vals_max[7][1])
        self.tr1_rroller = self._percentage(vals[8][1], vals_max[8][1])
        self.dust_ck = self._percentage(vals[9][1], vals_max[9][1])
        self.error_state = self._get_error_str((vals_max[10][1]).asNumbers())
        self.info = vals_max[11][1]





