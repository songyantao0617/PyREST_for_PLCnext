import logging.config
import sys

from com.Phoenixcontact.REST.Authentication import Authentication
from com.Phoenixcontact.REST.BasicRead import BasicRead
from com.Phoenixcontact.REST.ClientInfo import ClientInfo
from com.Phoenixcontact.REST.Constant import RestConstant
from com.Phoenixcontact.REST.DataGroup import DataGroup, ReadGroup
from com.Phoenixcontact.REST.RESTException import RESTException
from com.Phoenixcontact.REST.RESTHttpClient import RESTHttpclient
from com.Phoenixcontact.REST.SendData import SendData
from com.Phoenixcontact.REST.Session import Session


class NewClient(ClientInfo):

    def __init__(self, IPaddress):
        super().__init__()
        self.PLCnIp = IPaddress
        self.__reConnectCount = 0
        self.sessionMode = False
        self._Http = RESTHttpclient(self)
        self._DataGroup = DataGroup(self)
        self._Authentication = Authentication(self)
        self._BasicRead = BasicRead(self)
        self._SendData = SendData(self)
        self._Session = Session(self, 1, 'SessionThead')

    def reportGroups(self):
        while True:
            if self.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.connect()
            try:
                self._DataGroup._ReportGroups()
                self.__reConnectCount = 0
                return self.groupReportResult
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self._reConnect()
                elif 'invalidSessionID' in E.message and self.__reConnectCount < 2:
                    self._Session._createSessionID()
                else:
                    raise E

    def registerReadGroups(self, variableNames, pathPrefix=RestConstant.PATHPREFIX, _object=True):
        while True:
            if self.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.connect()
            try:

                __id, __variables = self._DataGroup._RegisterGroup(variableNames, pathPrefix)
                self.__reConnectCount = 0
                if _object:
                    return ReadGroup(groupID=__id, Client=self, vars=__variables, varName=variableNames,
                                     prefix=pathPrefix)
                else:
                    return __id, __variables
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self._reConnect()
                elif 'invalidSessionID' in E.message and self.__reConnectCount < 2:
                    self._Session._createSessionID()
                else:
                    raise E

    def connect(self):

        if self.sessionMode and self._Session.sessionID == None:
            # self._Session.setDaemon(True)
            self._Session.start()
            while self._Session.sessionID == None:
                pass

        logging.info('Connecting...')
        self._Authentication._Login()
        logging.info('Connect success')
        return

    def readDatas_dict(self, variableNames, pathPrefix=RestConstant.PATHPREFIX):
        while True:
            if self.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.connect()
            try:
                __result = self._BasicRead._ReadVariables(variableNames, pathPrefix)
                self.__reConnectCount = 0
                return __result
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self._reConnect()
                elif 'invalidSessionID' in E.message and self.__reConnectCount < 2:
                    self._Session._createSessionID()
                else:
                    raise E

    def readDatas_list(self, variableNames, pathPrefix=RestConstant.PATHPREFIX):
        _tmpResult = self.readDatas_dict(variableNames, pathPrefix)
        _Result = list()
        for _var in variableNames:
            _Result.append(_tmpResult.get(_var, None))

        if len(variableNames) == 1:
            return _Result[0]
        else:
            return _Result

    def writeDatas(self, variablesDict, pathPrefix=RestConstant.PATHPREFIX):
        while True:
            if self.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.connect()
            try:
                __result = self._SendData._SendData(variablesDict, pathPrefix)
                self.__reConnectCount = 0
                return __result
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self._reConnect()
                elif 'invalidSessionID' in E.message and self.__reConnectCount < 2:
                    self._Session._createSessionID()
                else:
                    raise E

    def _reConnect(self):
        logging.INFO('Try to reconnect... ')
        return self.connect()
