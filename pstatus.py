from pysnmp.hlapi import *

oid_ss_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_ss_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

oid_ss_cyan = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_ss_magenta = '1.3.6.1.2.1.43.11.1.1.9.1.2'
oid_ss_yellow = '1.3.6.1.2.1.43.11.1.1.9.1.3'
oid_ss_black = '1.3.6.1.2.1.43.11.1.1.9.1.4'

# 0 - 100 (to the nearest 10%)
oid_ricoh_black = '1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.1'
oid_ricoh_cyan = '1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.2'
oid_ricoh_magenta = '1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.3'
oid_ricoh_yellow = '1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.4'

# 0 = ok 9 = empty
oid_ricoh_tray1 = '1.3.6.1.4.1.367.3.2.1.2.20.2.2.1.11.2.1'
oid_ricoh_tray2 = '1.3.6.1.4.1.367.3.2.1.2.20.2.2.1.11.2.2'
oid_ricoh_tray3 = '1.3.6.1.4.1.367.3.2.1.2.20.2.2.1.11.2.3'
oid_ricoh_tray4 = '1.3.6.1.4.1.367.3.2.1.2.20.2.2.1.11.2.4'

oid_ricoh_total_pcount = '1.3.6.1.4.1.367.3.2.1.2.19.1.0'

printer_description = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)

def SamsungTonerPercantage(val):
    return val * 0.01

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('172.19.3.16', 161)),
           ContextData(),
           ObjectType(ObjectIdentity(oid_ricoh_black)),
           ObjectType(ObjectIdentity(oid_ricoh_cyan)),
           ObjectType(ObjectIdentity(oid_ricoh_magenta)),
           ObjectType(ObjectIdentity(oid_ricoh_yellow)),
           ObjectType(ObjectIdentity(oid_ricoh_total_pcount)))
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
