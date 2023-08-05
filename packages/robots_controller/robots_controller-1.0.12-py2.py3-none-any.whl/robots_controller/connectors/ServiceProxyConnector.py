# генерация тестового VB.NET конфига на основе excel Config.xlsx
import pyodbc
import json
import requests
#import logging

#import sys
# sys.path.append('../')

from robots_controller.common.error import error_handler


class ServiceProxyConnector:
    URL = "http://0001ofsbill01.msk.mts.ru:8001/"

    def __init__(self):
        driver = 'DRIVER={SQL SERVER}'
        server = 'SERVER=0000uipathdb01.msk.mts.ru'
        port = 'PORT=1433'
        database = 'DATABASE=UiPath'
        user = 'Trusted_Connection=yes'
        connStr = ';'.join([driver, server, port, database, user])

        self.conn = pyodbc.connect(connStr)
        self.cursor = self.conn.cursor()

        self.__token = None

    def __del__(self):
        self.conn.close()

    @property
    def token(self):
        if self.__token:
            return self.__token
        else:
            self.__login(self)
            return self.__token

    @error_handler
    def __login(self):
        token = None
        method = "api/users/login"
        head = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla'}
        params = {"user": {"username": "sgsafono", "password": "Q3/eaifc"}}

        reply = requests.post("{0}{1}".format(
            self.__class__.URL, method), json=params, headers=head)
        if reply.status_code == 200:
            _json = reply.json()
            # print(reply.text)
            #_json_ = json.dumps(reply.text)
            token = _json['token']

        self.__token = token

    # @error_handler
    def getInqueryByNumber(self, srid):
        data = None
        method = "api/incoming/siebel"
        head = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla',
                'authorization': 'Token {}'.format(self.token)}
        params = {
            "jsonrpc": "2.0",
            "method": "getInquiryByNumber",
            "params":
            {
                "sender": "test",
                "inquiryNumber": srid,
                "data": "Full"
            },
            "id": 1
        }
        reply = requests.post("{0}{1}".format(
            self.__class__.URL, method), json=params, headers=head)
        if reply.status_code == 200:
            _json = reply.json()
            #_json_ = json.dumps(reply.text)
            data = _json["result"]["data"]

        return data

    @error_handler
    def getInquiryList(self, _dateFrom, _dateTo, _theme, _type, _subTheme, _offlineQueue):
        data = None
        method = "api/incoming/siebel"

        head = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla',
                'authorization': 'Token {}'.format(self.token)}

        params = {
            "jsonrpc": "2.0", "method": "getInquiryList", "params":
                {
                    "sender": "Robot",
                    "dateFrom": _dateFrom,
                    "dateTo": _dateTo,
                    "query": {
                        "FullSR": "Y",
                        "Theme": _theme,
                        "Type": _type,
                        "SubTheme": _subTheme,
                        "OfflineQueue": _offlineQueue,
                        "interactionStatus": "Open"
                    }
                },
            "id": 1
        }

        reply = requests.post("{0}{1}".format(
            self.__class__.URL, method), json=params, headers=head)
        if reply.status_code == 200:
            __json = reply.json()
            data = __json["result"]["data"]

        return data
