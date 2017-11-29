from pysnmp.hlapi import *
from collections import namedtuple
import tkinter as tk
import pdata

PrinterData = namedtuple('printerdata', ['name', 'type', 'black', 'cyan', 'magenta', 'yellow'])

oid_ss_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_ss_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

oid_ss_c_yellow = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_ss_c_magenta = '1.3.6.1.2.1.43.11.1.1.9.1.2'
oid_ss_c_cyan = '1.3.6.1.2.1.43.11.1.1.9.1.3'
oid_ss_c_black = '1.3.6.1.2.1.43.11.1.1.9.1.4'

oid_ss_y_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_ss_m_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.2'
oid_ss_c_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.3'
oid_ss_b_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.4'

oid_hp_c_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_hp_c_cyan = '1.3.6.1.2.1.43.11.1.1.9.1.2'
oid_hp_c_magenta = '1.3.6.1.2.1.43.11.1.1.9.1.3'
oid_hp_c_yellow = '1.3.6.1.2.1.43.11.1.1.9.1.4'

oid_hp_b_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_hp_c_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.2'
oid_hp_m_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.3'
oid_hp_y_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.4'

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

oid_hp_bw_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'

oid_hp_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

oid_bw_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

printer_description = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)

def TonerPercantage(toner_level, max_capacity):
    return int((toner_level / max_capacity) * 100)

def QueryPrinter(printer):
    if printer[2] == 'hp_bw' or printer[2] == 'ss_bw':
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('public'),
                   UdpTransportTarget((printer[0], 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid_max_capacity)),
                   ObjectType(ObjectIdentity(oid_bw_black)))
        )

        if errorIndication or errorStatus:
            return'error', []
        else:
            return '', [varBinds[0][1], varBinds[1][1]]
    elif printer[2] == 'ss_c':
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('public'),
                   UdpTransportTarget((printer[0], 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid_ss_b_max_capacity)),
                   ObjectType(ObjectIdentity(oid_ss_c_black)),
                   ObjectType(ObjectIdentity(oid_ss_c_max_capacity)),
                   ObjectType(ObjectIdentity(oid_ss_c_cyan)),
                   ObjectType(ObjectIdentity(oid_ss_m_max_capacity)),
                   ObjectType(ObjectIdentity(oid_ss_c_magenta)),
                   ObjectType(ObjectIdentity(oid_ss_y_max_capacity)),
                   ObjectType(ObjectIdentity(oid_ss_c_yellow)))
        )

        if errorIndication or errorStatus:
            return 'error', []
        else:
            return '', [varBinds[0][1], varBinds[1][1], varBinds[2][1], varBinds[3][1], varBinds[4][1], varBinds[5][1],
                        varBinds[6][1], varBinds[7][1]]
    elif printer[2] == 'hp_c':
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('public'),
                   UdpTransportTarget((printer[0], 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid_hp_b_max_capacity)),
                   ObjectType(ObjectIdentity(oid_hp_c_black)),
                   ObjectType(ObjectIdentity(oid_hp_c_max_capacity)),
                   ObjectType(ObjectIdentity(oid_hp_c_cyan)),
                   ObjectType(ObjectIdentity(oid_hp_m_max_capacity)),
                   ObjectType(ObjectIdentity(oid_hp_c_magenta)),
                   ObjectType(ObjectIdentity(oid_hp_y_max_capacity)),
                   ObjectType(ObjectIdentity(oid_hp_c_yellow)))
        )

        if errorIndication or errorStatus:
            return 'error', []
        else:
            return '', [varBinds[0][1], varBinds[1][1], varBinds[2][1], varBinds[3][1], varBinds[4][1], varBinds[5][1],
                        varBinds[6][1], varBinds[7][1]]
    elif printer[2] == 'rc_cpr':
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('public'),
                   UdpTransportTarget((printer[0], 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid_max_capacity)),
                   ObjectType(ObjectIdentity(oid_ricoh_black)))
        )

        if errorIndication or errorStatus:
            return 'error', []
        else:
            return '', [varBinds[1][1]]
    elif printer[2] == 'rc_cpr_c':
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('public'),
                   UdpTransportTarget((printer[0], 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid_max_capacity)),
                   ObjectType(ObjectIdentity(oid_ricoh_black)),
                   ObjectType(ObjectIdentity(oid_ricoh_cyan)),
                   ObjectType(ObjectIdentity(oid_ricoh_magenta)),
                   ObjectType(ObjectIdentity(oid_ricoh_yellow)))
        )

        if errorIndication or errorStatus:
            return 'error', []
        else:
            return '', [varBinds[0][1], varBinds[1][1], varBinds[2][1], varBinds[3][1], varBinds[4][1]]
    else:
        return 'error', []

def ProcessPrinters(printers):
    process_printers = []
    for printer in printers:
        error_status, pvals = QueryPrinter(printer)
        if error_status:
            process_printers.append(PrinterData(printer[1],'printer unreachable', 0, 0, 0, 0))
        elif printer[2] == 'ss_bw' or printer[2] == 'hp_bw':
            process_printers.append(PrinterData(printer[1], printer[2], TonerPercantage(pvals[1], pvals[0]), 0, 0, 0))
        elif printer[2] == 'rc_cpr':
            process_printers.append(PrinterData(printer[1], printer[2], pvals[0], 0, 0, 0))
        elif printer[2] == 'rc_cpr_c':
            process_printers.append(PrinterData(printer[1], printer[2],
                                                TonerPercantage(pvals[1], pvals[0]),
                                                TonerPercantage(pvals[3], pvals[2]),
                                                TonerPercantage(pvals[5], pvals[4]),
                                                TonerPercantage(pvals[7], pvals[6])))
        elif printer[2] == 'ss_c':
            process_printers.append(PrinterData(printer[1], printer[2],
                                                TonerPercantage(pvals[1], pvals[0]),
                                                TonerPercantage(pvals[3], pvals[2]),
                                                TonerPercantage(pvals[5], pvals[4]),
                                                TonerPercantage(pvals[7], pvals[6])))
    return None, process_printers
'''

for printer in pdata.rce_printers:
    error_status, pvals = QueryPrinter(printer)
    if error_status:
        print('error - could not query printer data')
    elif printer[2] == 'ss_bw' or printer[2] == 'hp_bw':
        print('%s - Black: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0]))))
    elif printer[2] == 'rc_cpr':
        print('%s - Black: %s' % (printer[1], pvals[0]))
    elif printer[2] == 'rc_cpr_c':
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0])),
                                                                  int(TonerPercantage(pvals[2], pvals[0])),
                                                                  int(TonerPercantage(pvals[3], pvals[0])),
                                                                  int(TonerPercantage(pvals[4], pvals[0]))))
    else:
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0])),
                                                                  int(TonerPercantage(pvals[3], pvals[2])),
                                                                  int(TonerPercantage(pvals[5], pvals[4])),
                                                                  int(TonerPercantage(pvals[7], pvals[6]))))


for printer in pdata.rhs_printers:
    error_status, pvals = QueryPrinter(printer)
    if error_status:
        print('error - could not query printer data')
    elif printer[2] == 'ss_bw' or printer[2] == 'hp_bw':
        print('%s - Black: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0]))))
    elif printer[2] == 'rc_cpr':
        print('%s - Black: %s' % (printer[1], pvals[0]))
    elif printer[2] == 'rc_cpr_c':
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0])),
                                                                  int(TonerPercantage(pvals[2], pvals[0])),
                                                                  int(TonerPercantage(pvals[3], pvals[0])),
                                                                  int(TonerPercantage(pvals[4], pvals[0]))))
    else:
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0])),
                                                                  int(TonerPercantage(pvals[3], pvals[2])),
                                                                  int(TonerPercantage(pvals[5], pvals[4])),
                                                                  int(TonerPercantage(pvals[7], pvals[6]))))

for printer in pdata.sbo_printers:
    error_status, pvals = QueryPrinter(printer)
    if error_status:
        print('error - could not query printer data')
    elif printer[2] == 'ss_bw' or printer[2] == 'hp_bw':
        print('%s - Black: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0]))))
    elif printer[2] == 'rc_cpr':
        print('%s - Black: %s' % (printer[1], pvals[0]))
    elif printer[2] == 'rc_cpr_c':
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0])),
                                                                  int(TonerPercantage(pvals[2], pvals[0])),
                                                                  int(TonerPercantage(pvals[3], pvals[0])),
                                                                  int(TonerPercantage(pvals[4], pvals[0]))))
    else:
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], int(TonerPercantage(pvals[1], pvals[0])),
                                                                  int(TonerPercantage(pvals[3], pvals[2])),
                                                                  int(TonerPercantage(pvals[5], pvals[4])),
                                                                  int(TonerPercantage(pvals[7], pvals[6]))))

'''
'''
errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('172.25.10.7', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.2')),
           ObjectType(ObjectIdentity(oid_hp_supply_unit)),
           ObjectType(ObjectIdentity(oid_ss_c_black)),
           ObjectType(ObjectIdentity(oid_ss_c_cyan)),
           ObjectType(ObjectIdentity(oid_ss_c_magenta)))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
'''


error, proc_printers = ProcessPrinters(pdata.rce_printers)
print(error)
if error is None:
    for p in proc_printers:
        if p.type == 'hp_bw' or p.type == 'ss_bw':
            print('%s - Black: %s' % (p.name, p.black))
        elif p.type == 'ss_c':
            print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (p.name, p.black, p.cyan, p.magenta, p.yellow))

