import json
import logging.config
import sys

from com.Phoenixcontact.REST.RESTException import *
from com.Phoenixcontact.REST.RESTHttpClient import *


class DataGroup(object):

    def __init__(self, Client):
        self.Client = Client

    def _RegisterGroup(self, variableNames, pathPrefix=RestConstant.PATHPREFIX):
        if self.Client.accessToken == None:
            return

        _payload = {
            'pathPrefix': pathPrefix,
            'paths': variableNames
        }
        _status_code, _hearders, _text = self.Client._Http.invokeAPI(httpMethod=RestConstant.POST,
                                                                     function_uri=RestConstant.REGISTER_GROUP_URI,
                                                                     payload=json.dumps(_payload))
        if _status_code == 201:  # Creat success
            _response = json.loads(_text)
            if _response.get('variables'):
                # return ReadGroup(groupID=_response.get('id'), vars=_response.get('variables'), clientInfo=clientInfo)
                logging.info('Group ID : {}'.format(_response.get('id')))
                return _response.get('id'), _response.get('variables')
        elif _status_code == 404:  # 变量名不正确
            _response = json.loads(_text)
            _reason = _response.get('error').get('details')[0].get('reason')
            logging.error(str(_reason))
            raise RESTException(_reason)
        elif _status_code == 401:  # 令牌不正确
            self.accessToken = None
            _reason = _hearders.get('WWW-Authenticate')
            logging.error(str(_reason))
            raise RESTException(_reason)  # Bearer realm="pxcapi", error="invalid_token"
        elif _status_code == 410:  # sessionID不正确
            logging.error('invalidSessionID')
            raise RESTException('invalidSessionID')

    @staticmethod
    def _ReadGroupValues(ReadGroup):
        if ReadGroup.groupID == None or ReadGroup.Client.accessToken == None:
            return
        _url = RestConstant.READ_GROUP_URI + ReadGroup.groupID
        _status_code, _hearders, _text = ReadGroup.Client._Http.invokeAPI(httpMethod=RestConstant.GET,
                                                                          function_uri=_url,
                                                                          payload=None)
        if _status_code == 200:
            _response = json.loads(_text)
            if _response.get('id') == ReadGroup.groupID:
                ReadGroup.valves = _response.get('variables')
                Result = dict()
                for _item in ReadGroup.valves:
                    Result[_item['path']] = _item['value']
                return Result
        elif _status_code == 404:  # groupID不正确
            ReadGroup.groupID = None
            _response = json.loads(_text)
            _reason = _response.get('error').get('details')[0].get('reason')
            logging.error(_reason)
            raise RESTException(_reason)
        elif _status_code == 401:  # 令牌不正确loads
            ReadGroup.clientInfo.accessToken = None
            _reason = _hearders.get('WWW-Authenticate')
            logging.error(_reason)
            raise RESTException(_reason)  # Bearer realm="pxcapi", error="invalid_token"
        elif _status_code == 400:  # 指令不正确
            _response = json.loads(_text)
            _reason = _response.get('error').get('details')[0].get('reason')
            logging.error(_reason)
            raise RESTException(_reason)
        elif _status_code == 410:  # sessionID不正确
            logging.error('invalidSessionID')
            raise RESTException('invalidSessionID')

    # @staticmethod
    # def Unregister(GroupInfo):
    #     if GroupInfo.groupID == None:
    #         return
    #     _url = RestConstant.UNREGISTER_GROUP_URI + GroupInfo.groupID
    #
    #     _status_code, _hearders, _text = RESTHttpClient.invokeAPI(httpMethod=RestConstant.DELETE,
    #                                                               authUri=_url,
    #                                                               ClientInfo=GroupInfo.clientInfo,
    #                                                               payload=None)
    #     pass

    def _ReportGroups(self):
        if self.Client.accessToken == None:
            return
        _status_code, _hearders, _text = self.Client._Http.invokeAPI(httpMethod=RestConstant.GET,
                                                                     function_uri=RestConstant.REPORT_GROUP_URI,
                                                                     payload=None)
        if _status_code == 200:
            _response = json.loads(_text).get('groups')
            self.Client.groupReportResult = _response
            return _response
        elif _status_code == 401:  # 令牌不正确loads
            self.accessToken = None
            _reason = _hearders.get('WWW-Authenticate')
            logging.error(_reason)
            raise RESTException(_reason)  # Bearer realm="pxcapi", error="invalid_token"
        elif _status_code == 400:  # 指令不正确
            _response = json.loads(_text)
            _reason = _response.get('error').get('details')[0].get('reason')
            logging.error(_reason)
            raise RESTException(_reason)
        elif _status_code == 410:  # sessionID不正确
            logging.error('invalidSessionID')
            raise RESTException('invalidSessionID')


class ReadGroup(object):
    def __init__(self, vars, Client, groupID=None, varName=None, prefix=None):
        self.groupID = groupID
        self.vars = vars
        self.valves = None
        # self.clientInfo = Client
        self.Client = Client
        self.__reConnectCount = 0
        self.__reFreshCount = 0
        self._Results = {}
        self._varName_BACKUP = varName
        self._prefix_BACKUP = prefix

    @property
    def results_dict(self):
        self._Read()
        return self._Results

    @property
    def results_list(self):
        _res = self.results_dict
        _resultList = list()
        for var in self._varName_BACKUP:
            _resultList.append(_res.get(var, None))
        if len(self._varName_BACKUP) == 1:
            return _resultList[0]
        else:
            return _resultList

    def __getitem__(self, item):
        self._Read()
        return self._Results.get(item, None)

    def __str__(self):
        return 'groupID : ' + str(self.groupID) + ' | vars : ' + str(self.vars) + ' | valves : ' + str(
            self.valves) + " | " + str(self.Client)

    def checkMemberType(self):
        _ResultDict = dict()
        for _item in self.vars:
            _varName = _item.get('path')
            _ResultDict[_varName] = _item.get('type')
        return _ResultDict

    def _Read(self):
        while True:
            if self.Client.accessToken == None:
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.Client.Connect()
            try:
                Result = DataGroup._ReadGroupValues(self)
                self.__reConnectCount = 0
                self.__reFreshCount = 0
                self._Results = Result
                return self._Results
            except RESTException as E:
                if 'invalid_token' in E.message and self.__reConnectCount < 2:
                    self.__reConnectCount += 1
                    self.Client._reConnect()
                elif 'invalidGroupID' in E.message and self.__reFreshCount < 2:
                    logging.info('Trying to refresh group ID')
                    self.__reFreshCount += 1
                    self.refreshID()
                elif 'invalidSessionID' in E.message and self.__reFreshCount < 2:
                    self.Client._Session._createSessionID()

                else:
                    raise E

    def refreshID(self):
        __newID, __NewRes = self.Client.registerReadGroups(self._varName_BACKUP, self._prefix_BACKUP, _object=False)
        self.groupID = __newID
