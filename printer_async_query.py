from pysnmp.hlapi import *
from collections import namedtuple
import threading
import queue

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

QueryResult = namedtuple('queryresult', ['name', 'type', 'status', 'black', 'cyan', 'magenta', 'yellow', 'model', 'type'])

query_results = []
query_results_lock = threading.Lock()
max_query_threads = 10
max_total_threads = max_query_threads + 2

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
               ObjectType(ObjectIdentity(oid_hp_model)),
               ObjectType(ObjectIdentity(oid_hp_name)))
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
               ObjectType(ObjectIdentity(oid_ss_model)),
               ObjectType(ObjectIdentity(oid_ss_name)))
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
               ObjectType(ObjectIdentity(oid_ss_c_yellow)),
               ObjectType(ObjectIdentity(oid_ss_model)),
               ObjectType(ObjectIdentity(oid_ss_name)),
               ObjectType(ObjectIdentity(oid_ss_name)))
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
               ObjectType(ObjectIdentity(oid_hp_c_yellow)),
               ObjectType(ObjectIdentity(oid_hp_model)),
               ObjectType(ObjectIdentity(oid_hp_name)))
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

class QueryThread (threading.Thread):
    ''' query a single printer '''
    def __init__(self, id, printer_data):
        self.id = id
        self.printer_data = printer_data
        self.threadID = 'thread {}'.format(id)

    def run(self):
        qr = QueryResult()
        if self.printer_data[2] == 'hp_bw' or self.printer_data[2] == 'ss_bw':
            if self.printer_data[2] == 'hp_bw':
                error_indication, error_status, error_index, var_binds = _QueryHpBw(self.printer_data)
            elif self.printer_data[2] == 'ss_bw':
                error_indication, error_status, error_index, var_binds = _QuerySsBw(self.printer_data)

            if error_indication or error_status:
                qr = QueryResult(name=error_indication, type=error_status, status='error', black=0, cyan=0, magenta=0,
                                   yellow=0,
                                   model='error')
            else:
                qr = QueryResult(name=var_binds[3][1], type=self.printer_data[2], status='ok',
                                   black=TonerPercentage(var_binds[1][1], var_binds[0][1]),
                                   cyan=0, magenta=0, yellow=0, model=var_binds[2][1])

        elif self.printer_data[2] == 'ss_color' or self.printer_data[2] == 'hp_color':
            if self.printer_data[2] == 'ss_color':
                error_indication, error_status, error_index, var_binds = _QuerySsColor(self.printer_data)
            elif self.printer_data[2] == 'hp_color':
                error_indication, error_status, error_index, var_binds = _QueryHpColor(self.printer_data)

            if error_indication or error_status:
                qr = QueryResult(name=error_indication, type=error_status, status='error', black=0, cyan=0, magenta=0,
                                   yellow=0,
                                   model='error')
            else:
                qr = QueryResult(name=self.printer_data[1], type=self.printer_data[2], status='ok',
                                   black=TonerPercentage(var_binds[1][1], var_binds[0][1]),
                                   cyan=TonerPercentage(var_binds[3][1], var_binds[2][1]),
                                   magenta=TonerPercentage(var_binds[5][1], var_binds[4][1]),
                                   yellow=TonerPercentage(var_binds[7][1], var_binds[6][1]),
                                   model=var_binds[8][1])
        elif self.printer_data[2] == 'rc_cpr':
            error_indication, error_status, error_index, var_binds = _QueryRicohBw(self.printer_data)
            if error_indication or error_status:
                qr =  QueryResult(name=error_indication, type=error_status, status='error', black=0, cyan=0, magenta=0,
                                   yellow=0,
                                   model='error')
            else:
                qr =  QueryResult(name=self.printer_data[1], type=self.printer_data[2], status='ok', black=var_binds[1][1],
                                   cyan=0, magenta=0, yellow=0, model=var_binds[2][1])
        elif self.printer_data[2] == 'rc_cpr_color':
            error_indication, error_status, error_index, var_binds = _QueryRicohColor(self.printer_data)
            if error_indication or error_status:
                qr = QueryResult(name=error_indication, type=error_status, status='error', black=0, cyan=0, magenta=0,
                                   yellow=0,
                                   model='error')
            else:
                qr =  QueryResult(name=self.printer_data[1], type=self.printer_data[2], status='ok',
                                   black=TonerPercentage(var_binds[1][1], var_binds[0][1]),
                                   cyan=TonerPercentage(var_binds[2][1], var_binds[0][1]),
                                   magenta=TonerPercentage(var_binds[3][1], var_binds[0][1]),
                                   yellow=TonerPercentage(var_binds[4][1], var_binds[0][1]),
                                   model=var_binds[5][1])
        else:
            qr =  QueryResult(name='printer type not recognized', type=self.printer_data[2], status='error', black=0, cyan=0, magenta=0, yellow=0,
                               model='error')

        query_results_lock.acquire()
        query_results.append(qr)
        query_results_lock.release()
