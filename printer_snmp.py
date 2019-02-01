from pysnmp.hlapi import *
from abc import ABCMeta, abstractmethod

class SnmpCore:
    def __init__(self):
        self.engine = SnmpEngine()
        self.com_data = CommunityData('public')
        self.context_data = ContextData()

class IPrinter(metaclass=ABCMeta):
    @abstractmethod
    def query(self, snmp_core):
        pass

class PrinterClp775(IPrinter):
    oid_name = '.1.3.6.1.2.1.1.5.0'
    oid_info = '.1.3.6.1.2.1.1.1.0'

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

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def _clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def _percentage(self, toner_level, max_capacity):
        level = int(toner_level / max_capacity * 100)
        return self._clamp(level, 0, 100)

    def query(self, snmp_core):
        error_indication, error_status, error_index, vals = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self.oid_yellow)),
                   ObjectType(ObjectIdentity(self.oid_magenta)),
                   ObjectType(ObjectIdentity(self.oid_cyan)),
                   ObjectType(ObjectIdentity(self.oid_black)),
                   ObjectType(ObjectIdentity(self.oid_tr_belt)),
                   ObjectType(ObjectIdentity(self.oid_fuser)),
                   ObjectType(ObjectIdentity(self.oid_mp_roller)),
                   ObjectType(ObjectIdentity(self.oid_tr1_roller)),
                   ObjectType(ObjectIdentity(self.oid_tr1_rroller)),
                   ObjectType(ObjectIdentity(self.oid_dust_cleaning_kit)),
                   )
        )

        error_indication, error_status, error_index, vals_max = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self.oid_yellow_capacity)),
                   ObjectType(ObjectIdentity(self.oid_magenta_capacity)),
                   ObjectType(ObjectIdentity(self.oid_cyan_capacity)),
                   ObjectType(ObjectIdentity(self.oid_black_capacity)),
                   ObjectType(ObjectIdentity(self.oid_tr_belt_capacity)),
                   ObjectType(ObjectIdentity(self.oid_fuser_capacity)),
                   ObjectType(ObjectIdentity(self.oid_mp_roller_capacity)),
                   ObjectType(ObjectIdentity(self.oid_tr1_roller_capcity)),
                   ObjectType(ObjectIdentity(self.oid_tr1_rroller_capacity)),
                   ObjectType(ObjectIdentity(self.oid_dust_cleaning_kit_capacity)),
                   ObjectType(ObjectIdentity(self.oid_name)),
                   ObjectType(ObjectIdentity(self.oid_info)),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        self.yellow_level = self._percentage(vals[0][1], vals_max[0][1])
        self.magenta_level = self._percentage(vals[1][1], vals_max[1][1])
        self.cyan_level = self._percentage(vals[2][1], vals_max[2][1])
        self.black_level = self._percentage(vals[3][1], vals_max[3][1])
        self.tr_belt_level = self._percentage(vals[4][1], vals_max[4][1])
        self.fuser_level = self._percentage(vals[5][1], vals_max[5][1])
        self.mp_roller_level = self._percentage(vals[6][1], vals_max[6][1])
        self.tr1_roller_level = self._percentage(vals[7][1], vals_max[7][1])
        self.tr1_rroller_level = self._percentage(vals[8][1], vals_max[8][1])
        self.dust_ck_level = self._percentage(vals[9][1], vals_max[9][1])
        self.internal_name = vals_max[10][1]
        self.info = vals_max[11][1]


    def __str__(self):
        return 'name: {} internal name: {} black: {} yellow: {} magenta: {} cyan: {}\n    transfer belt: {}' \
               ' fuser: {} mp roller: {} tray1_roller: {} tray1 rroller: {} dust cleaning kit: {}\n' \
               '    info: {}'.format(self.name,
                                  self.internal_name,
                                  self.black_level,
                                  self.yellow_level,
                                  self.magenta_level,
                                  self.cyan_level,
                                  self.tr_belt_level,
                                  self.fuser_level,
                                  self.mp_roller_level,
                                  self.tr1_roller_level,
                                  self.tr1_rroller_level,
                                  self.dust_ck_level,
                                  self.info)



class PrinterMl371(IPrinter):
    oid_name = '.1.3.6.1.2.1.1.5.0'
    oid_info = '.1.3.6.1.2.1.1.1.0'

    oid_black = '.1.3.6.1.2.1.43.11.1.1.9.1.1'
    oid_fuser = '.1.3.6.1.2.1.43.11.1.1.9.1.2'
    oid_tr1_roller = '.1.3.6.1.2.1.43.11.1.1.9.1.3'
    oid_tr1_torque_limiter = '.1.3.6.1.2.1.43.11.1.1.9.1.4'

    oid_black_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.1'
    oid_fuser_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.2'
    oid_tr1_roller_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.3'
    oid_tr1_torque_limiter_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.4'

    oid_black_str = '.1.3.6.1.2.1.43.11.1.1.6.1.1'
    oid_fuser_str = '.1.3.6.1.2.1.43.11.1.1.6.1.2'
    oid_tr1_roller_str = '.1.3.6.1.2.1.43.11.1.1.6.1.3'
    oid_tr1_torque_limiter_Str = '.1.3.6.1.2.1.43.11.1.1.6.1.4'

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def _clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def _percentage(self, toner_level, max_capacity):
        level = int(toner_level / max_capacity * 100)
        return self._clamp(level, 0, 100)

    def query(self, snmp_core):
        error_indication, error_status, error_index, vals = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self.oid_black)),
                   ObjectType(ObjectIdentity(self.oid_fuser)),
                   ObjectType(ObjectIdentity(self.oid_tr1_roller)),
                   ObjectType(ObjectIdentity(self.oid_tr1_torque_limiter)),
                   )
        )

        error_indication, error_status, error_index, vals_max = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self.oid_black_capacity)),
                   ObjectType(ObjectIdentity(self.oid_fuser_capacity)),
                   ObjectType(ObjectIdentity(self.oid_tr1_roller_capacity)),
                   ObjectType(ObjectIdentity(self.oid_tr1_torque_limiter_capacity)),
                   ObjectType(ObjectIdentity(self.oid_name)),
                   ObjectType(ObjectIdentity(self.oid_info)),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        self.black_level = self._percentage(vals[0][1], vals_max[0][1])
        self.fuser_level = self._percentage(vals[1][1], vals_max[1][1])
        self.tr1_roller_level = self._percentage(vals[2][1], vals_max[2][1])
        self.tr1_torque_limiter_level = self._percentage(vals[3][1], vals_max[3][1])
        self.internal_name = vals_max[4][1]
        self.info = vals_max[5][1]

    def __str__(self):
        return 'name: {} internal name: {} black: {} fuser: {} tray1 roller: {}' \
               ' tray 1 torque limiter: {}\n    info: {}'.format(self.name,
                                                              self.internal_name,
                                                              self.black_level,
                                                              self.fuser_level,
                                                              self.tr1_roller_level,
                                                              self.tr1_torque_limiter_level,
                                                              self.info)

class PrinterM3820dw(IPrinter):
    oid_name = '.1.3.6.1.2.1.1.5.0'
    oid_info = '.1.3.6.1.2.1.1.1.0'

    oid_black = '.1.3.6.1.2.1.43.11.1.1.9.1.1'
    oid_fuser = '.1.3.6.1.2.1.43.11.1.1.9.1.2'
    oid_tr1_roller = '.1.3.6.1.2.1.43.11.1.1.9.1.3'
    oid_tr1_torque_limiter = '.1.3.6.1.2.1.43.11.1.1.9.1.4'

    oid_black_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.1'
    oid_fuser_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.2'
    oid_tr1_roller_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.3'
    oid_tr1_torque_limiter_capacity = '.1.3.6.1.2.1.43.11.1.1.8.1.4'

    oid_black_str = '.1.3.6.1.2.1.43.11.1.1.6.1.1'
    oid_fuser_str = '.1.3.6.1.2.1.43.11.1.1.6.1.2'
    oid_tr1_roller_str = '.1.3.6.1.2.1.43.11.1.1.6.1.3'
    oid_tr1_torque_limiter_Str = '.1.3.6.1.2.1.43.11.1.1.6.1.4'

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def _clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def _percentage(self, toner_level, max_capacity):
        level = int(toner_level / max_capacity * 100)
        return self._clamp(level, 0, 100)

    def query(self, snmp_core):
        error_indication, error_status, error_index, vals = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self.oid_black)),
                   ObjectType(ObjectIdentity(self.oid_fuser)),
                   ObjectType(ObjectIdentity(self.oid_tr1_roller)),
                   ObjectType(ObjectIdentity(self.oid_tr1_torque_limiter)),
                   )
        )

        error_indication, error_status, error_index, vals_max = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self.oid_black_capacity)),
                   ObjectType(ObjectIdentity(self.oid_fuser_capacity)),
                   ObjectType(ObjectIdentity(self.oid_tr1_roller_capacity)),
                   ObjectType(ObjectIdentity(self.oid_tr1_torque_limiter_capacity)),
                   ObjectType(ObjectIdentity(self.oid_name)),
                   ObjectType(ObjectIdentity(self.oid_info)),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        self.black_level = self._percentage(vals[0][1], vals_max[0][1])
        self.fuser_level = self._percentage(vals[1][1], vals_max[1][1])
        self.tr1_roller_level = self._percentage(vals[2][1], vals_max[2][1])
        self.tr1_torque_limiter_level = self._percentage(vals[3][1], vals_max[3][1])
        self.internal_name = vals_max[4][1]
        self.info = vals_max[5][1]

    def __str__(self):
        return 'name: {} internal name: {} black: {} fuser: {} tray1 roller: {}' \
               ' tray 1 torque limiter: {}\n    info: {}'.format(self.name,
                                                              self.internal_name,
                                                              self.black_level,
                                                              self.fuser_level,
                                                              self.tr1_roller_level,
                                                              self.tr1_torque_limiter_level,
                                                              self.info)

