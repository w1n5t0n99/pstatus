from pysnmp.hlapi import *
import pdata

oid_ss_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_ss_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

oid_ss_c_yellow = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_ss_c_magenta = '1.3.6.1.2.1.43.11.1.1.9.1.2'
oid_ss_c_cyan = '1.3.6.1.2.1.43.11.1.1.9.1.3'
oid_ss_c_black = '1.3.6.1.2.1.43.11.1.1.9.1.4'

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
oid_hp_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_hp_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

oid_bw_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_max_capacity = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

printer_description = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)

def TonerPercantage(toner_level, max_capacity):
    return (toner_level / max_capacity) * 100

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
                   ObjectType(ObjectIdentity(oid_ss_max_capacity)),
                   ObjectType(ObjectIdentity(oid_ss_c_black)),
                   ObjectType(ObjectIdentity(oid_ss_c_cyan)),
                   ObjectType(ObjectIdentity(oid_ss_c_magenta)),
                   ObjectType(ObjectIdentity(oid_ss_c_yellow)))
        )

        if errorIndication or errorStatus:
            return 'error', []
        else:
            return '', [varBinds[0][1], varBinds[1][1], varBinds[2][1], varBinds[3][1], varBinds[4][1]]
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


for printer in pdata.rce_printers:
    error_status, pvals = QueryPrinter(printer)
    if error_status:
        print('error - could not query printer data')
    elif printer[2] == 'ss_bw' or printer[2] == 'hp_bw':
        print('%s - Black: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0])))
    elif printer[2] == 'rc_cpr':
        print('%s - Black: %s' % (printer[1], pvals[0]))
    elif printer[2] == 'rc_cpr_c':
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0]),
                                                                  TonerPercantage(pvals[2], pvals[0]),
                                                                  TonerPercantage(pvals[3], pvals[0]),
                                                                  TonerPercantage(pvals[4], pvals[0])))
    else:
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0]),
                                                                  TonerPercantage(pvals[2], pvals[0]),
                                                                  TonerPercantage(pvals[3], pvals[0]),
                                                                  TonerPercantage(pvals[4], pvals[0])))


for printer in pdata.rhs_printers:
    error_status, pvals = QueryPrinter(printer)
    if error_status:
        print('error - could not query printer data')
    elif printer[2] == 'ss_bw' or printer[2] == 'hp_bw':
        print('%s - Black: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0])))
    elif printer[2] == 'rc_cpr':
        print('%s - Black: %s' % (printer[1], pvals[0]))
    elif printer[2] == 'rc_cpr_c':
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0]),
                                                                  TonerPercantage(pvals[2], pvals[0]),
                                                                  TonerPercantage(pvals[3], pvals[0]),
                                                                  TonerPercantage(pvals[4], pvals[0])))
    else:
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0]),
                                                                  TonerPercantage(pvals[2], pvals[0]),
                                                                  TonerPercantage(pvals[3], pvals[0]),
                                                                  TonerPercantage(pvals[4], pvals[0])))

for printer in pdata.sbo_printers:
    error_status, pvals = QueryPrinter(printer)
    if error_status:
        print('error - could not query printer data')
    elif printer[2] == 'ss_bw' or printer[2] == 'hp_bw':
        print('%s - Black: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0])))
    elif printer[2] == 'rc_cpr':
        print('%s - Black: %s' % (printer[1], pvals[0]))
    elif printer[2] == 'rc_cpr_c':
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0]),
                                                                  TonerPercantage(pvals[2], pvals[0]),
                                                                  TonerPercantage(pvals[3], pvals[0]),
                                                                  TonerPercantage(pvals[4], pvals[0])))
    else:
        print('%s - Black: %s Cyan: %s Magenta: %s Yellow: %s' % (printer[1], TonerPercantage(pvals[1], pvals[0]),
                                                                  TonerPercantage(pvals[2], pvals[0]),
                                                                  TonerPercantage(pvals[3], pvals[0]),
                                                                  TonerPercantage(pvals[4], pvals[0])))