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
    _oid_tr1_torque_limiter = '.1.3.6.1.2.1.43.11.1.1.9.1.4'

    _oid_yellow_str = '.1.3.6.1.2.1.43.11.1.1.6.1.1'
    _oid_magenta_str = '.1.3.6.1.2.1.43.11.1.1.6.1.2'
    _oid_cyan_str = '.1.3.6.1.2.1.43.11.1.1.6.1.3'
    _oid_black_str = '.1.3.6.1.2.1.43.11.1.1.6.1.4'
    _oid_tr_belt_str = '.1.3.6.1.2.1.43.11.1.1.6.1.5'
    _oid_fuser_str = '.1.3.6.1.2.1.43.11.1.1.6.1.6'
    _oid_mp_roller_str = '.1.3.6.1.2.1.43.11.1.1.6.1.7'
    _oid_tr1_roller_str = '.1.3.6.1.2.1.43.11.1.1.6.1.8'
    _oid_tr1_rroller_str = '.1.3.6.1.2.1.43.11.1.1.6.1.9'
    _oid_dust_cleaning_kit_str = '.1.3.6.1.2.1.43.11.1.1.6.1.10'

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
    _oid_tr1_torque_limiter_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.4'

    def __init__(self, name, ip):
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

    @abstractmethod
    def query(self, snmp_core):
        pass

    def _clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def _percentage(self, toner_level, max_capacity):
        level = int(toner_level / max_capacity * 100)
        return self._clamp(level, 0, 100)


class PrinterBW(IPrinter):
    '''black and white printer object'''

    def __init__(self, name, ip):
        super(PrinterBW, self).__init__(name, ip)

    def query(self, snmp_core):
        error_indication, error_status, error_index, vals = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self._oid_black)),
                   ObjectType(ObjectIdentity(self._oid_fuser)),
                   ObjectType(ObjectIdentity(self._oid_tr1_roller)),
                   ObjectType(ObjectIdentity(self._oid_tr1_torque_limiter)),
                   )
        )

        error_indication, error_status, error_index, vals_max = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self._oid_black_capacity)),
                   ObjectType(ObjectIdentity(self._oid_fuser_capacity)),
                   ObjectType(ObjectIdentity(self._oid_tr1_roller_capcity)),
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
       # self.tr1_roller = super(PrinterBW, self)._percentage(vals[2][1], vals_max[2][1])
       # self.tr1_torque_limiter = super(PrinterBW, self)._percentage(vals[3][1], vals_max[3][1])
        self.tr1_roller = vals[2][1]
        self.tr1_torque_limiter = vals[3][1]
        self.error_state = (vals_max[4][1]).asNumbers()
        self.info = vals_max[5][1]
