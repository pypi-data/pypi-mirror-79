import json

from robots_controller.connectors.ServiceProxyConnector import ServiceProxyConnector


#_json = json.loads('{"id":6,"name":"sgsafono","email":"sgsafono@mts.ru","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NiwibmFtZSI6InNnc2Fmb25vIiwiZW1haWwiOiJzZ3NhZm9ub0BtdHMucnUiLCJleHAiOjE2MDQ4MjY5MjAsImlhdCI6MTU5OTY0MjkyMH0.mPPWNTYxDDXfx9lQrWQ6x2eeGyT_RYgsFwdtUeaiaB8"}')
#print(_json)
#tok = _json["token"]




obj = ServiceProxyConnector()
res = obj.getInqueryByNumber("1-688357270685")

print(res)