import logging.config
import sys

from com.Phoenixcontact.REST.Authentication import Authentication
from com.Phoenixcontact.REST.BasicRead import BasicRead
from com.Phoenixcontact.REST.ClientInfo import ClientInfo
from com.Phoenixcontact.REST.Constant import RestConstant
from com.Phoenixcontact.REST.DataGroup import DataGroup, ReadGroup
from com.Phoenixcontact.REST.RESTException import RESTException
from com.Phoenixcontact.REST.SendData import SendData


class NewClient(ClientInfo, DataGroup, Authentication, SendData, BasicRead):

    def __init__(self, IPaddress):
        super().__init__()
        self.PLCnIp = IPaddress
        self.__reConnectCount = 0

    def reportGroups(self):
        while True:
            if self.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.connect()
            try:
                self._ReportGroups(self)
                self.__reConnectCount = 0
                return self.groupReportResult
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self._reConnect()
                else:
                    raise E

    def registerReadGroups(self, variableNames, pathPrefix=RestConstant.PATHPREFIX, _object=True):
        while True:
            if self.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.connect()
            try:

                __id, __variables = self._RegisterGroup(self, variableNames, pathPrefix)
                self.__reConnectCount = 0
                if _object:
                    return ReadGroup(groupID=__id, Parent=self, vars=__variables, varName=variableNames,
                                     prefix=pathPrefix)
                else:
                    return __id, __variables
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self._reConnect()
                else:
                    raise E

    def connect(self):
        logging.info('Connecting...')
        self._Login(self)
        logging.info('Connect success')
        return

    def readDatas_dict(self, variableNames, pathPrefix=RestConstant.PATHPREFIX):
        while True:
            if self.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.connect()
            try:
                __result = self._ReadVariables(self, variableNames, pathPrefix)
                self.__reConnectCount = 0
                return __result
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self._reConnect()
                else:
                    raise E

    def readDatas_list(self, variableNames, pathPrefix=RestConstant.PATHPREFIX):
        _tmpResult = self.readDatas_dict(variableNames, pathPrefix)
        _Result = list()
        for _var in variableNames:
            _Result.append(_tmpResult.get(_var, None))
        return _Result

    def writeDatas(self, variablesDict, pathPrefix=RestConstant.PATHPREFIX):
        while True:
            if self.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.connect()
            try:
                __result = self._SendData(self, variablesDict, pathPrefix)
                self.__reConnectCount = 0
                return __result
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self._reConnect()
                else:
                    raise E

    def _reConnect(self):
        logging.INFO('Try to reconnect... ')
        return self.connect()
