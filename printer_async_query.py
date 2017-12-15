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
oid_hp_name = '1.3.6.1.4.1.11.2.3.9.4.2.1.1.3.10'

oid_ss_supply_unit = '1.3.6.1.2.1.43.11.1.1.7.1.1'
oid_ss_model = '1.3.6.1.2.1.25.3.2.1.3.1'
oid_ss_name = '1.3.6.1.2.1.43.5.1.1.16.1'

oid_ss_bw_mc = '1.3.6.1.2.1.43.11.1.1.8.1.1'
oid_hp_bw_mc = '1.3.6.1.2.1.43.11.1.1.8.1.1'

QueryResult = namedtuple('queryresult', ['name', 'type', 'status', 'black', 'cyan', 'magenta', 'yellow', 'model', 'row'])

query_results = queue.Queue()

_query_results_lock = threading.Lock()
_MAX_QUERY_THREADS = 40

def _ErrorQueryResult(error):
    return QueryResult(name='', type='', status=error, black=0, cyan=0, yellow=0, magenta=0, model=0, row=0)

def _Clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def _TonerPercentage(toner_level, max_capacity):
    level = int(toner_level / max_capacity * 100)
    return _Clamp(level, 0, 100)

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

    if error_indication:
        qr = _ErrorQueryResult(error_indication)
    elif error_status:
        qr = _ErrorQueryResult('{} at {}'.format(error_status.prettyPrint(),
                                                 error_index and var_binds[-1][int(error_index) - 1] or '?'))
    else:
        qr = QueryResult(name=printer[1], type=printer[2], status='ok',
                         black=_TonerPercentage(var_binds[1][1], var_binds[0][1]),
                         cyan=' ', magenta= ' ', yellow= ' ', model=var_binds[2][1], row=printer[3])

    return qr

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

    if error_indication:
        qr = _ErrorQueryResult(error_indication)
    elif error_status:
        qr = _ErrorQueryResult('{} at {}'.format(error_status.prettyPrint(),
                                                 error_index and var_binds[-1][int(error_index) - 1] or '?'))
    else:
        qr = QueryResult(name=printer[1], type=printer[2], status='ok',
                         black=_TonerPercentage(var_binds[1][1], var_binds[0][1]),
                         cyan= ' ', magenta= ' ', yellow=' ', model=var_binds[2][1], row=printer[3])

    return qr

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
               ObjectType(ObjectIdentity(oid_ss_name)))
    )

    if error_indication:
        qr = _ErrorQueryResult(error_indication)
    elif error_status:
        qr = _ErrorQueryResult('{} at {}'.format(error_status.prettyPrint(),
                                                 error_index and var_binds[-1][int(error_index) - 1] or '?'))
    else:
        qr = QueryResult(printer[1], type=printer[2], status='ok',
                         black=_TonerPercentage(var_binds[1][1], var_binds[0][1]),
                         cyan=_TonerPercentage(var_binds[3][1], var_binds[2][1]),
                         magenta=_TonerPercentage(var_binds[5][1], var_binds[4][1]),
                         yellow=_TonerPercentage(var_binds[7][1], var_binds[6][1]),
                         model=var_binds[8][1], row=printer[3])


    return qr

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

    if error_indication:
        qr = _ErrorQueryResult(error_indication)
    elif error_status:
        qr = _ErrorQueryResult('{} at {}'.format(error_status.prettyPrint(),
                                                 error_index and var_binds[-1][int(error_index) - 1] or '?'))
    else:
        qr = QueryResult(printer[1], type=printer[2], status='ok',
                         black=_TonerPercentage(var_binds[1][1], var_binds[0][1]),
                         cyan=_TonerPercentage(var_binds[3][1], var_binds[2][1]),
                         magenta=_TonerPercentage(var_binds[5][1], var_binds[4][1]),
                         yellow=_TonerPercentage(var_binds[7][1], var_binds[6][1]),
                         model=var_binds[8][1], row=printer[3])

    return qr

def _QueryRicohBw(printer):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((printer[0], 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ricoh_mc)),
               ObjectType(ObjectIdentity(oid_ricoh_black)),
               ObjectType(ObjectIdentity(oid_ricoh_model)),
               ObjectType(ObjectIdentity(oid_ricoh_name)))
    )

    if error_indication:
        qr = _ErrorQueryResult(error_indication)
    elif error_status:
        qr = _ErrorQueryResult('{} at {}'.format(error_status.prettyPrint(),
                                                 error_index and var_binds[-1][int(error_index) - 1] or '?'))
    else:
        qr = QueryResult(name=printer[1], type=printer[2], status='ok', black=var_binds[1][1],
                         cyan=' ', magenta=' ', yellow=' ', model=var_binds[2][1], row=printer[3])

    return qr

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
               ObjectType(ObjectIdentity(oid_ricoh_model)),
               ObjectType(ObjectIdentity(oid_ricoh_name)))
    )

    if error_indication:
        qr = _ErrorQueryResult(error_indication)
    elif error_status:
        qr = _ErrorQueryResult('{} at {}'.format(error_status.prettyPrint(),
                                                 error_index and var_binds[-1][int(error_index) - 1] or '?'))
    else:
        qr = QueryResult(name=printer[1], type=printer[2], status='ok',
                         black=_TonerPercentage(var_binds[1][1], var_binds[0][1]),
                         cyan=_TonerPercentage(var_binds[2][1], var_binds[0][1]),
                         magenta=_TonerPercentage(var_binds[3][1], var_binds[0][1]),
                         yellow=_TonerPercentage(var_binds[4][1], var_binds[0][1]),
                         model=var_binds[5][1], row=printer[3])

    return qr

class QueryThread (threading.Thread):
    ''' query a single printer '''
    def __init__(self, id, printer_data, query_callback_func):
        threading.Thread.__init__(self)
        self.id = id
        self.printer_data = printer_data
        self.threadID = 'thread {}'.format(id)
        self._query_callback_func = query_callback_func

    def run(self):
        if self.printer_data[2] == 'hp_bw':
            qr = _QueryHpBw(self.printer_data)
        elif self.printer_data[2] == 'ss_bw':
            qr = _QuerySsBw(self.printer_data)
        elif self.printer_data[2] == 'ss_color':
            qr = _QuerySsColor(self.printer_data)
        elif self.printer_data[2] == 'hp_color':
            qr = _QueryHpColor(self.printer_data)
        elif self.printer_data[2] == 'rc_cpr':
            qr = _QueryRicohBw(self.printer_data)
        elif self.printer_data[2] == 'rc_cpr_color':
            qr = _QueryRicohColor(self.printer_data)
        else:
            qr = _ErrorQueryResult('error - {} - not recognized type'.format(self.printer_data[2]))

        query_results.put(qr)
        if self._query_callback_func is not None:
            self._query_callback_func(self.printer_data[3], qr.name, qr.black, qr.cyan, qr.magenta, qr.yellow)

class PStatusThread (threading.Thread):
    def __init__(self, id, printers, query_callback_func = None):
        threading.Thread.__init__(self)
        self.id = id
        self.printers = printers
        self.threadID = id
        self._query_callback_func = query_callback_func

    def run(self):
        q_thread_id = 0
        num_query_threads = _MAX_QUERY_THREADS if _MAX_QUERY_THREADS < self.printers.qsize() else self.printers.qsize()
        thread_list = []

        for x in range(0, num_query_threads-1):
            qt = QueryThread(q_thread_id, self.printers.get(), self._query_callback_func)
            qt.start()
            thread_list.append(qt)

            q_thread_id+=1
            self.printers.task_done()

        while not self.printers.empty():
            if threading.active_count() < (num_query_threads + 3):
                qt = QueryThread(q_thread_id, self.printers.get(), self._query_callback_func)
                qt.start()
                thread_list.append(qt)

                q_thread_id += 1
                self.printers.task_done()

        for qt in thread_list:
            qt.join()