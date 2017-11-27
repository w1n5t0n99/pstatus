from pysnmp.hlapi import *

oid_ss_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_ss_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

oid_ss_cyan = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_ss_magenta = '1.3.6.1.2.1.43.11.1.1.9.1.2'
oid_ss_yellow = '1.3.6.1.2.1.43.11.1.1.9.1.3'
oid_ss_black = '1.3.6.1.2.1.43.11.1.1.9.1.4'

printer_description = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)

def SamsungTonerPercantage(val):
    return val * 0.01

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('172.16.3.5', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.4')), #black
           ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.1')), #cyan
           ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.2')), #magenta
           ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.3')), #yellow
           ObjectType(ObjectIdentity(oid_ss_max_capacity)))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
       # print(SamsungTonerPercantage(varBind[1]))
