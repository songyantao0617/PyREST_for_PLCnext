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
        _status_code, _hearders, _text = self.Client._Http.syncHttpAPI(httpMethod=RestConstant.POST,
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
        _status_code, _hearders, _text = ReadGroup.Client._Http.syncHttpAPI(httpMethod=RestConstant.GET,
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
            ReadGroup.Client.accessToken = None
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
        _status_code, _hearders, _text = self.Client._Http.syncHttpAPI(httpMethod=RestConstant.GET,
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

    #################################################################################################################


import threading, asyncio, time


class AsyncRead(threading.Thread):
    def __init__(self, ReadGroup, threadID, name,poolSize):
        super().__init__(daemon=True)
        self.poolSize = poolSize
        self.threadID = threadID
        self.name = name
        self.disbleThread = False
        self.ReadGroup = ReadGroup
        self.loop = asyncio.get_event_loop()
        self.pause = False
        self._updatedTimeStamp = time.time()
        self._updatedId = 0
        self._updatedTick = 0

    def run(self):
        self.disbleThread = False
        logging.info('AsyncGroup start ')
        tasks = [self._body(i) for i in range(self.poolSize)]
        self.loop.run_until_complete(asyncio.wait(tasks))
        logging.info('AsyncGroup stop ')

    async def _body(self, id):
        while self.disbleThread == False:
            # await asyncio.sleep(0.005)
            time.sleep(0.001)
            await self._Read(id)

    async def _Read(self, id):
        thisTimestamp = time.time()
        while True:
            if self.pause:
                return
            if self.ReadGroup.Client.accessToken == None:
                self.pause = True
                logging.error("Impossible to call " + (sys._getframe().f_code.co_name) + " without token")
                self.ReadGroup.Client.Connect()
            try:
                Result = await self._ReadGroupValues()
                self.ReadGroup.__reConnectCount = 0
                self.ReadGroup.__reFreshCount = 0
                self.pause = False
                rcvTick = int(Result['ESM_DATA.ESM_INFOS[1].TICK_COUNT'])
                if rcvTick > self._updatedTick:
                    self.ReadGroup._Results = Result
                    self._updatedTimeStamp = thisTimestamp
                    self._updatedId = id
                    self._updatedTick = rcvTick
                return
            except RESTException as E:
                self.pause = True
                if 'invalid_token' in E.message and self.ReadGroup.__reConnectCount < 2:
                    self.ReadGroup.__reConnectCount += 1
                    self.ReadGroup.Client._reConnect()
                elif 'invalidGroupID' in E.message and self.ReadGroup.__reFreshCount < 2:
                    logging.info('Trying to refresh group ID')
                    self.ReadGroup.__reFreshCount += 1
                    self.ReadGroup.refreshID()
                elif 'invalidSessionID' in E.message and self.ReadGroup.__reFreshCount < 2:
                    self.ReadGroup.Client._Session._createSessionID()

                else:
                    raise E

    async def _ReadGroupValues(self):

        if self.ReadGroup.groupID == None or self.ReadGroup.Client.accessToken == None:
            return
        _url = RestConstant.READ_GROUP_URI + self.ReadGroup.groupID
        _status_code, _hearders, _text = await self.ReadGroup.Client._Http.asyncHttpAPI(httpMethod=RestConstant.GET,
                                                                                        function_uri=_url,
                                                                                        payload=None, loop=self.loop)

        if _status_code == 200:
            _response = json.loads(_text)
            if _response.get('id') == self.ReadGroup.groupID:
                self.ReadGroup.valves = _response.get('variables')
                Result = dict()
                for _item in self.ReadGroup.valves:
                    Result[_item['path']] = _item['value']
                return Result
        elif _status_code == 404:  # groupID不正确
            self.ReadGroup.groupID = None
            _response = json.loads(_text)
            _reason = _response.get('error').get('details')[0].get('reason')
            logging.error(_reason)
            raise RESTException(_reason)
        elif _status_code == 401:  # 令牌不正确loads
            if self.ReadGroup.Client.accessToken == None:
                pass  # 如果被其他协程上报了，不再处理
            self.ReadGroup.Client.accessToken = None
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


#################################################################################################################


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
        self._asynThread = None
        # for key in varName:
        #     self._Results[key] = None

    @property
    def results_dict(self):
        if self._asynThread != None:
            if self._asynThread.isAlive():
                return self._Results
        else:
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

    def asyncStart(self,poolSize = 100,):
        self.Client._Http.mount(pool_connections=5,pool_maxsize=120)
        if self._asynThread == None:
            self._asynThread = AsyncRead(self, 2, 'AsyncRead_1',poolSize)
            if 'ESM_DATA.ESM_INFOS[1].TICK_COUNT' in self._varName_BACKUP:
                if self._asynThread.isAlive() == False:
                    self._asynThread.start()
            else:
                logging.error("Must have 'ESM_DATA.ESM_INFOS[1].TICK_COUNT' in this group !")
                raise RESTException("Must have 'ESM_DATA.ESM_INFOS[1].TICK_COUNT' in this group !")

    def asyncStop(self):
        if self._asynThread:
            self._asynThread.disbleThread = True
            self._asynThread.join()
            self._asynThread = None
            self.Client._Http.NewSession()
        else:
            logging.error('No asyncTask instance , Have you start ?')
            raise RESTException('No asyncTask instance')
