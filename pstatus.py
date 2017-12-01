import tkinter as tk
import pdata
import printer_query
from pysnmp.hlapi import *

'''
for p in pdata.rce_printers:
    pres = printer_query.QueryPrinter(p)
    if '_color' in pres.type:
        print('{0} model: {5} black: {1} cyan: {2} magenta: {3} yellow: {4}'.format(pres.name, pres.black, pres.cyan, pres.magenta, pres.yellow, pres.model) )
    else:
        print('{0} model: {2} black: {1}'.format(pres.name, pres.black, pres.model))

for p in pdata.rhs_printers:
    pres = printer_query.QueryPrinter(p)
    if '_color' in pres.type:
        print('{0} model: {5} black: {1} cyan: {2} magenta: {3} yellow: {4}'.format(pres.name, pres.black, pres.cyan, pres.magenta, pres.yellow, pres.model) )
    else:
        print('{0} model: {2} black: {1}'.format(pres.name, pres.black, pres.model))
'''

#'1.3.6.1.2.1.43.11.1.1.8.1.1'
errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public', mpModel=0),
           UdpTransportTarget(('172.16.3.16', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.43.5.1.1.16.1')))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
