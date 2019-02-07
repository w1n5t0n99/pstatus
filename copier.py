from pysnmp.hlapi import *
from abc import ABCMeta, abstractmethod

class SnmpCore:
    def __init__(self):
        self.engine = SnmpEngine()
        self.com_data = CommunityData('public')
        self.context_data = ContextData()

class ICopier(metaclass=ABCMeta):
    '''base class for copiers'''

    _oid_info = '.1.3.6.1.2.1.1.1.0'
    _oid_black = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.1'
    _oid_cyan = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.2'
    _oid_magenta = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.3'
    _oid_yellow = '.1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.4'
    _oid_history_base = '.1.3.6.1.4.1.367.3.2.1.3.2.1.1.1.4.'

    def __init__(self, name, ip):
        self.core = SnmpCore()
        self.name = name
        self.ip = ip
        self.info = None
        self.black = None
        self.cyan = None
        self.magenta = None
        self.yellow = None
        self.history = [None] * 20

    def clear(self):
        self.info = None
        self.black = None
        self.cyan = None
        self.magenta = None
        self.yellow = None
        self.history = [None] * 20

    @abstractmethod
    def query(self):
        pass

class CopierBW(ICopier):
    '''black and white copier object'''

    def __init__(self, name, ip):
        super(CopierBW, self).__init__(name, ip)

    def query(self):
        error_indication, error_status, error_index, vals = next(
            getCmd(self.core.engine,
                   self.core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   self.core.context_data,
                   ObjectType(ObjectIdentity(self._oid_black)),
                   ObjectType(ObjectIdentity(self._oid_info)),
                   ObjectType(ObjectIdentity(self._oid_history_base + '1')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '2')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '3')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '4')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '5')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '6')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '7')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '8')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '9')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '10')),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        self.black = vals[0][1]
        self.info = vals[1][1]

        for x in range(0, 10):
            self.history[x] = (vals[x+2][1]).asOctets()

        error_indication, error_status, error_index, vals = next(
            getCmd(self.core.engine,
                   self.core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   self.core.context_data,
                   ObjectType(ObjectIdentity(self._oid_history_base + '11')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '12')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '13')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '14')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '15')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '16')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '17')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '18')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '19')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '20')),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        for x in range(0, 10):
            self.history[x+ 10] = (vals[x][1]).asOctets()


class CopierColor(ICopier):
    '''black and white copier object'''

    def __init__(self, name, ip):
        super(CopierColor, self).__init__(name, ip)

    def query(self):
        error_indication, error_status, error_index, vals = next(
            getCmd(self.core.engine,
                   self.core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   self.core.context_data,
                   ObjectType(ObjectIdentity(self._oid_black)),
                   ObjectType(ObjectIdentity(self._oid_cyan)),
                   ObjectType(ObjectIdentity(self._oid_magenta)),
                   ObjectType(ObjectIdentity(self._oid_yellow)),
                   ObjectType(ObjectIdentity(self._oid_info)),
                   ObjectType(ObjectIdentity(self._oid_history_base + '1')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '2')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '3')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '4')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '5')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '6')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '7')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '8')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '9')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '10')),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        self.black = vals[0][1]
        self.cyan = vals[1][1]
        self.magenta = vals[2][1]
        self.yellow = vals[3][1]
        self.info = vals[4][1]

        for x in range(0, 10):
            self.history[x] = (vals[x + 5][1]).asOctets()

        error_indication, error_status, error_index, vals = next(
            getCmd(self.core.engine,
                   self.core.com_data,
                   UdpTransportTarget((self.ip, 161)),
                   self.core.context_data,
                   ObjectType(ObjectIdentity(self._oid_history_base + '11')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '12')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '13')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '14')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '15')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '16')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '17')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '18')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '19')),
                   ObjectType(ObjectIdentity(self._oid_history_base + '20')),
                   )
        )

        if error_indication:
            raise Exception('printer snmp error - ip: {} error indication: {}'.format(self.ip, error_indication))
        elif error_status:
            raise Exception('printer snmp error - ip: {} error status: {}'.format(self.ip, error_status))

        for x in range(0, 10):
            self.history[x + 10] = (vals[x][1]).asOctets()