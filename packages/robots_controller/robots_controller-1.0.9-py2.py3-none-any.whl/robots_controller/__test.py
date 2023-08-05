from sys import path
#path.append("c:\\python36\\lib\\site-packages")


print(path)

import json

from connectors.ServiceProxyConnector import ServiceProxyConnector


#_json = json.loads('{"id":6,"name":"sgsafono","email":"sgsafono@mts.ru","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NiwibmFtZSI6InNnc2Fmb25vIiwiZW1haWwiOiJzZ3NhZm9ub0BtdHMucnUiLCJleHAiOjE2MDQ4MjY5MjAsImlhdCI6MTU5OTY0MjkyMH0.mPPWNTYxDDXfx9lQrWQ6x2eeGyT_RYgsFwdtUeaiaB8"}')
#print(_json)
#tok = _json["token"]




spc1 = ServiceProxyConnector()
res = spc1.getInqueryByNumber("1-688357270685")

print(res)