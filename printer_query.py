from pysnmp.hlapi import *
from collections import namedtuple

oid_ss_c_yellow = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_ss_c_magenta = '1.3.6.1.2.1.43.11.1.1.9.1.2'
oid_ss_c_cyan = '1.3.6.1.2.1.43.11.1.1.9.1.3'
oid_ss_c_black = '1.3.6.1.2.1.43.11.1.1.9.1.4'

oid_ss_c_yellow_mc= '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_ss_c_magenta_mc = '1.3.6.1.2.1.43.11.1.1.8.1.2'
oid_ss_c_cyan_mc = '1.3.6.1.2.1.43.11.1.1.8.1.3'
oid_ss_c_black_mc = '1.3.6.1.2.1.43.11.1.1.8.1.4'

oid_hp_c_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_hp_c_cyan = '1.3.6.1.2.1.43.11.1.1.9.1.2'
oid_hp_c_magenta = '1.3.6.1.2.1.43.11.1.1.9.1.3'
oid_hp_c_yellow = '1.3.6.1.2.1.43.11.1.1.9.1.4'

oid_hp_c_black_mc = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_hp_c_cyan_mc = '1.3.6.1.2.1.43.11.1.1.8.1.2'
oid_hp_c_magenta_mc = '1.3.6.1.2.1.43.11.1.1.8.1.3'
oid_hp_c_yellow_mc = '1.3.6.1.2.1.43.11.1.1.8.1.4'

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
oid_ricoh_mc = '1.3.6.1.2.1.43.11.1.1.8.1.1'

oid_hp_bw_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_ss_bw_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'

oid_hp_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'
oid_ss_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'

oid_ss_bw_mc = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_hp_bw_mc = '1.3.6.1.2.1.43.11.1.1.8.1.1'

QueryResult = namedtuple('queryresult', ['name', 'type', 'status', 'black', 'cyan', 'magenta', 'yellow'])

def TonerPercentage(toner_level, max_capacity):
    return int((toner_level / max_capacity) * 100)

def _QueryHpBw(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_hp_bw_mc)),
               ObjectType(ObjectIdentity(oid_hp_bw_black)))
    )

    return error_indication, error_status, error_index, var_binds

def _QuerySsBw(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ss_bw_mc)),
               ObjectType(ObjectIdentity(oid_ss_bw_black)))
    )

    return error_indication, error_status, error_index, var_binds

def _QuerySsColor(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ss_c_black_mc)),
               ObjectType(ObjectIdentity(oid_ss_c_black)),
               ObjectType(ObjectIdentity(oid_ss_c_cyan_mc)),
               ObjectType(ObjectIdentity(oid_ss_c_cyan)),
               ObjectType(ObjectIdentity(oid_ss_c_magenta_mc)),
               ObjectType(ObjectIdentity(oid_ss_c_magenta)),
               ObjectType(ObjectIdentity(oid_ss_c_yellow_mc)),
               ObjectType(ObjectIdentity(oid_ss_c_yellow)))
    )

    return error_indication, error_status, error_index, var_binds

def _QueryHpColor(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_hp_c_black_mc)),
               ObjectType(ObjectIdentity(oid_hp_c_black)),
               ObjectType(ObjectIdentity(oid_hp_c_cyan_mc)),
               ObjectType(ObjectIdentity(oid_hp_c_cyan)),
               ObjectType(ObjectIdentity(oid_hp_c_magenta_mc)),
               ObjectType(ObjectIdentity(oid_hp_c_magenta)),
               ObjectType(ObjectIdentity(oid_hp_c_yellow_mc)),
               ObjectType(ObjectIdentity(oid_hp_c_yellow)))
    )

    return error_indication, error_status, error_index, var_binds

def _QueryRicohBw(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ricoh_mc)),
               ObjectType(ObjectIdentity(oid_ricoh_black)))
    )

    return error_indication, error_status, error_index, var_binds

def _QueryRicohColor(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ricoh_mc)),
               ObjectType(ObjectIdentity(oid_ricoh_black)),
               ObjectType(ObjectIdentity(oid_ricoh_cyan)),
               ObjectType(ObjectIdentity(oid_ricoh_magenta)),
               ObjectType(ObjectIdentity(oid_ricoh_yellow)))
    )

    return error_indication, error_status, error_index, var_binds

def QueryPrinter(printer):
    if printer[2] == 'hp_bw' or printer[2] == 'ss_bw':
        if printer[2] == 'hp_bw':
            errorIndication, errorStatus, errorIndex, varBinds = _QueryHpBw(printer)
        elif printer[2] == 'ss_bw':
            errorIndication, errorStatus, errorIndex, varBinds = _QuerySsBw(printer)

        if errorIndication or errorStatus:
            return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0)
        else:
            return QueryResult(name=printer[1], type=printer[2], status='ok',
                               black=TonerPercentage(varBinds[1][1], varBinds[0][1]),
                               cyan=0, magenta=0, yellow=0)

    elif printer[2] == 'ss_c' or printer[2] == 'hp_c':
        if printer[2] == 'ss_c':
            errorIndication, errorStatus, errorIndex, varBinds = _QuerySsColor(printer)
        elif  printer[2] == 'hp_c':
            errorIndication, errorStatus, errorIndex, varBinds = _QueryHpColor(printer)

        if errorIndication or errorStatus:
            return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0)
        else:
            return QueryResult(name=printer[1], type=printer[2], status='ok',
                               black=TonerPercentage(varBinds[1][1], varBinds[0][1]),
                               cyan=TonerPercentage(varBinds[2][1], varBinds[3][1]),
                               magenta=TonerPercentage(varBinds[4][1], varBinds[5][1]),
                               yellow=TonerPercentage(varBinds[6][1], varBinds[7][1]))
    elif printer[2] == 'rc_cpr':
        errorIndication, errorStatus, errorIndex, varBinds = _QueryRicohBw(printer)
        if errorIndication or errorStatus:
            return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0)
        else:
            return QueryResult(name=printer[1], type=printer[2], status='ok', black=varBinds[1][1],
                               cyan=0, magenta=0, yellow=0)
    elif printer[2] == 'rc_cpr_c':
        errorIndication, errorStatus, errorIndex, varBinds = _QueryRicohColor(printer)
        if errorIndication or errorStatus:
            return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0)
        else:
            return QueryResult(name=printer[1], type=printer[2], status='ok',
                               black=TonerPercentage(varBinds[1][1], varBinds[0][1]),
                               cyan=TonerPercentage(varBinds[2][1], varBinds[0][1]),
                               magenta=TonerPercentage(varBinds[3][1], varBinds[0][1]),
                               yellow=TonerPercentage(varBinds[4][1], varBinds[0][1]))
    else:
        return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0)


