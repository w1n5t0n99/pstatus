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

class PrinterAficioMp4001(IPrinter):
    oid_info = '.1.3.6.1.2.1.1.1.0'
    oid_black = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.1'

    oid_history = ['.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.1',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.2',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.3',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.4',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.5',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.6',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.7',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.8',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.9',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.10',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.11',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.12',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.13',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.14',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.15',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.16',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.17',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.18',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.19',
                   '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.20',
                   ]

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.history = []

    def query(self, snmp_core):
        error_indication, error_status, error_index, vals = next(
            getCmd(snmp_core.engine,
                   snmp_core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   snmp_core.context_data,
                   ObjectType(ObjectIdentity(self.oid_black)),
                   ObjectType(ObjectIdentity(self.oid_info)),
                   ObjectType(ObjectIdentity(self.oid_history[0])),
                   ObjectType(ObjectIdentity(self.oid_history[1])),
                   ObjectType(ObjectIdentity(self.oid_history[2])),
                   ObjectType(ObjectIdentity(self.oid_history[3])),
                   ObjectType(ObjectIdentity(self.oid_history[4])),
                   ObjectType(ObjectIdentity(self.oid_history[5])),
                   ObjectType(ObjectIdentity(self.oid_history[6])),
                   ObjectType(ObjectIdentity(self.oid_history[7])),
                   ObjectType(ObjectIdentity(self.oid_history[8])),
                   ObjectType(ObjectIdentity(self.oid_history[9])),
                   ObjectType(ObjectIdentity(self.oid_history[10])),
                   ObjectType(ObjectIdentity(self.oid_history[11])),
                   ObjectType(ObjectIdentity(self.oid_history[12])),
                   ObjectType(ObjectIdentity(self.oid_history[13])),
                   ObjectType(ObjectIdentity(self.oid_history[14])),
                   ObjectType(ObjectIdentity(self.oid_history[15])),
                   ObjectType(ObjectIdentity(self.oid_history[16])),
                   ObjectType(ObjectIdentity(self.oid_history[17])),
                   ObjectType(ObjectIdentity(self.oid_history[18])),
                   ObjectType(ObjectIdentity(self.oid_history[19])),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        self.black_level = vals[0][1]
        self.info = vals[1][1]

        for x in range(0, 20):
            self.history.append(vals[x+2][1])

    def __str__(self):
        return 'name: {} black: {}\n    history 1: {}\n    history 2: {}\n    history 3: {}\n    history 4: {}\n' \
               '    history 5: {}\n    history 6: {}\n    history 7: {}\n    history 8: {}\n    history 9: {}\n' \
               '    history 10: {}\n    history 11: {}\n    history 12: {}\n    history 13: {}\n    history 14: {}\n' \
               '    history 15: {}\n    history 16: {}\n    history 17: {}\n    history 18: {}\n    history 19: {}\n' \
               '    history 20: {}\n    info: {}'.format(self.name,
                                                         self.black_level,
                                                         self.history[0],
                                                         self.history[1],
                                                         self.history[2],
                                                         self.history[3],
                                                         self.history[4],
                                                         self.history[5],
                                                         self.history[6],
                                                         self.history[7],
                                                         self.history[8],
                                                         self.history[9],
                                                         self.history[10],
                                                         self.history[11],
                                                         self.history[12],
                                                         self.history[13],
                                                         self.history[14],
                                                         self.history[15],
                                                         self.history[16],
                                                         self.history[17],
                                                         self.history[18],
                                                         self.history[19],
                                                         self.info,
                                                         )

class PrinterAficioMpC4501(IPrinter):
        oid_info = '.1.3.6.1.2.1.1.1.0'
        oid_black = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.1'
        oid_cyan = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.2'
        oid_magenta = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.3'
        oid_yellow = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.4'

        oid_history = ['.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.1',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.2',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.3',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.4',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.5',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.6',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.7',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.8',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.9',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.10',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.11',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.12',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.13',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.14',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.15',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.16',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.17',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.18',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.19',
                       '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.20',
                       ]

        def __init__(self, name, ip):
            self.name = name
            self.ip = ip
            self.history = []

        def query(self, snmp_core):
            error_indication, error_status, error_index, vals = next(
                getCmd(snmp_core.engine,
                       snmp_core.com_data,
                       UdpTransportTarget((self.ip, 161)),
                       snmp_core.context_data,
                       ObjectType(ObjectIdentity(self.oid_black)),
                       ObjectType(ObjectIdentity(self.oid_cyan)),
                       ObjectType(ObjectIdentity(self.oid_magenta)),
                       ObjectType(ObjectIdentity(self.oid_yellow)),
                       ObjectType(ObjectIdentity(self.oid_info)),
                       ObjectType(ObjectIdentity(self.oid_history[0])),
                       ObjectType(ObjectIdentity(self.oid_history[1])),
                       ObjectType(ObjectIdentity(self.oid_history[2])),
                       ObjectType(ObjectIdentity(self.oid_history[3])),
                       ObjectType(ObjectIdentity(self.oid_history[4])),
                       ObjectType(ObjectIdentity(self.oid_history[5])),
                       ObjectType(ObjectIdentity(self.oid_history[6])),
                       ObjectType(ObjectIdentity(self.oid_history[7])),
                       ObjectType(ObjectIdentity(self.oid_history[8])),
                       ObjectType(ObjectIdentity(self.oid_history[9])),
                       ObjectType(ObjectIdentity(self.oid_history[10])),
                       ObjectType(ObjectIdentity(self.oid_history[11])),
                       ObjectType(ObjectIdentity(self.oid_history[12])),
                       ObjectType(ObjectIdentity(self.oid_history[13])),
                       ObjectType(ObjectIdentity(self.oid_history[14])),
                       ObjectType(ObjectIdentity(self.oid_history[15])),
                       ObjectType(ObjectIdentity(self.oid_history[16])),
                       ObjectType(ObjectIdentity(self.oid_history[17])),
                       ObjectType(ObjectIdentity(self.oid_history[18])),
                       ObjectType(ObjectIdentity(self.oid_history[19])),
                       )
            )

            if error_indication:
                raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
            elif error_status:
                raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

            self.black_level = vals[0][1]
            self.cyan_level = vals[1][1]
            self.magenta_level = vals[2][1]
            self.yellow_level = vals[3][1]
            self.info = vals[4][1]

            for x in range(0, 20):
                self.history.append(vals[x + 5][1])

        def __str__(self):
            return 'name: {} black: {} cyan: {} magenta: {} yellow: {}\n' \
                   '    history 1: {}\n    history 2: {}\n    history 3: {}\n    history 4: {}\n' \
                   '    history 5: {}\n    history 6: {}\n    history 7: {}\n    history 8: {}\n    history 9: {}\n' \
                   '    history 10: {}\n    history 11: {}\n    history 12: {}\n    history 13: {}\n    history 14: {}\n' \
                   '    history 15: {}\n    history 16: {}\n    history 17: {}\n    history 18: {}\n    history 19: {}\n' \
                   '    history 20: {}\n    info: {}'.format(self.name,
                                                             self.black_level,
                                                             self.cyan_level,
                                                             self.magenta_level,
                                                             self.yellow_level,
                                                             self.history[0],
                                                             self.history[1],
                                                             self.history[2],
                                                             self.history[3],
                                                             self.history[4],
                                                             self.history[5],
                                                             self.history[6],
                                                             self.history[7],
                                                             self.history[8],
                                                             self.history[9],
                                                             self.history[10],
                                                             self.history[11],
                                                             self.history[12],
                                                             self.history[13],
                                                             self.history[14],
                                                             self.history[15],
                                                             self.history[16],
                                                             self.history[17],
                                                             self.history[18],
                                                             self.history[19],
                                                             self.info,
                                                             )