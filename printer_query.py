from pysnmp.hlapi import *
from collections import namedtuple
import threading
import queue

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
oid_ricoh_model = '1.3.6.1.2.1.25.3.2.1.3.1'
oid_ricoh_name = '1.3.6.1.2.1.43.5.1.1.16.1'

oid_hp_bw_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'
oid_ss_bw_black = '1.3.6.1.2.1.43.11.1.1.9.1.1'

oid_hp_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'
oid_hp_model = '1.3.6.1.2.1.25.3.2.1.3.1'
oid_hp_name = '1.3.6.1.2.1.43.5.1.1.16.1'

oid_ss_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'
oid_ss_model = '1.3.6.1.2.1.25.3.2.1.3.1'
oid_ss_name = '1.3.6.1.2.1.43.5.1.1.16.1'

oid_ss_bw_mc = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_hp_bw_mc = '1.3.6.1.2.1.43.11.1.1.8.1.1'

QueryResult = namedtuple('queryresult', ['name', 'type', 'status', 'black', 'cyan', 'magenta', 'yellow', 'model'])

query_results = []
thread_lock = threading.Lock()

def Clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def TonerPercentage(toner_level, max_capacity):
    level = int(toner_level / max_capacity * 100)
    return Clamp(level, 0, 100)

def _QueryHpBw(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_hp_bw_mc)),
               ObjectType(ObjectIdentity(oid_hp_bw_black)),
               ObjectType(ObjectIdentity(oid_hp_model)))
    )

    return error_indication, error_status, error_index, var_binds

def _QuerySsBw(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ss_bw_mc)),
               ObjectType(ObjectIdentity(oid_ss_bw_black)),
               ObjectType(ObjectIdentity(oid_ss_model)))
    )

    return error_indication, error_status, error_index, var_binds

def _AsyncQuerySsBw(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ss_bw_mc)),
               ObjectType(ObjectIdentity(oid_ss_bw_black)),
               ObjectType(ObjectIdentity(oid_ss_model)))
    )

    thread_lock.acquire()
    query_results.append((error_indication, error_status, error_index, var_binds))
    thread_lock.release()

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
               ObjectType(ObjectIdentity(oid_ss_c_yellow)),
               ObjectType(ObjectIdentity(oid_ss_model)))
    )

    return error_indication, error_status, error_index, var_binds

def _AsyncQuerySsColor(printer):
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
               ObjectType(ObjectIdentity(oid_ss_c_yellow)),
               ObjectType(ObjectIdentity(oid_ss_model)))
    )
    thread_lock.acquire()
    query_results.append((error_indication, error_status, error_index, var_binds))
    thread_lock.release()

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
               ObjectType(ObjectIdentity(oid_hp_c_yellow)),
               ObjectType(ObjectIdentity(oid_hp_model)))
    )

    return error_indication, error_status, error_index, var_binds

def _QueryRicohBw(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ricoh_mc)),
               ObjectType(ObjectIdentity(oid_ricoh_black)),
               ObjectType(ObjectIdentity(oid_ricoh_model)))
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
               ObjectType(ObjectIdentity(oid_ricoh_yellow)),
               ObjectType(ObjectIdentity(oid_ricoh_model))               )
    )

    return error_indication, error_status, error_index, var_binds

def QueryPrinter(printer):
    if printer[2] == 'hp_bw' or printer[2] == 'ss_bw':
        if printer[2] == 'hp_bw':
            error_indication, error_status, error_index, var_binds = _QueryHpBw(printer)
        elif printer[2] == 'ss_bw':
            error_indication, error_status, error_index, var_binds = _QuerySsBw(printer)

        if error_indication or error_status:
            return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0,
                               model='error')
        else:
            return QueryResult(name=printer[1], type=printer[2], status='ok',
                               black=TonerPercentage(var_binds[1][1], var_binds[0][1]),
                               cyan=0, magenta=0, yellow=0, model=var_binds[2][1])

    elif printer[2] == 'ss_color' or printer[2] == 'hp_color':
        if printer[2] == 'ss_color':
            error_indication, error_status, error_index, var_binds = _QuerySsColor(printer)
        elif  printer[2] == 'hp_color':
            error_indication, error_status, error_index, var_binds = _QueryHpColor(printer)

        if error_indication or error_status:
            return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0,
                               model='error')
        else:
            return QueryResult(name=printer[1], type=printer[2], status='ok',
                               black=TonerPercentage(var_binds[1][1], var_binds[0][1]),
                               cyan=TonerPercentage(var_binds[3][1], var_binds[2][1]),
                               magenta=TonerPercentage(var_binds[5][1], var_binds[4][1]),
                               yellow=TonerPercentage(var_binds[7][1], var_binds[6][1]),
                               model=var_binds[8][1])
    elif printer[2] == 'rc_cpr':
        error_indication, error_status, error_index, var_binds = _QueryRicohBw(printer)
        if error_indication or error_status:
            return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0,
                               model='error')
        else:
            return QueryResult(name=printer[1], type=printer[2], status='ok', black=var_binds[1][1],
                               cyan=0, magenta=0, yellow=0, model=var_binds[2][1])
    elif printer[2] == 'rc_cpr_color':
        error_indication, error_status, error_index, var_binds = _QueryRicohColor(printer)
        if error_indication or error_status:
            return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0,
                               model='error')
        else:
            return QueryResult(name=printer[1], type=printer[2], status='ok',
                               black=TonerPercentage(var_binds[1][1], var_binds[0][1]),
                               cyan=TonerPercentage(var_binds[2][1], var_binds[0][1]),
                               magenta=TonerPercentage(var_binds[3][1], var_binds[0][1]),
                               yellow=TonerPercentage(var_binds[4][1], var_binds[0][1]),
                               model=var_binds[5][1])
    else:
        return QueryResult(name=printer[1], type=printer[2], status='error', black=0, cyan=0, magenta=0, yellow=0,
                           model='error')


def AsyncQueryPrinters(printers, num_threads):
    t0 = threading.Thread(name='q0', target=_AsyncQuerySsBw, args=(printers[0],))
    t1 = threading.Thread(name='q1', target=_AsyncQuerySsColor, args=(printers[1],))

    t0.start()
    t1.start()
    t0.join()
    t1.join()