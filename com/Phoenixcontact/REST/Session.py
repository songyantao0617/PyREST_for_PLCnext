import json
import logging.config
import random
import threading
import time

from com.Phoenixcontact.REST.RESTException import *
from com.Phoenixcontact.REST.RESTHttpClient import *


class Session(threading.Thread):

    def __init__(self, Client, threadID, name):
        super().__init__(daemon=True)
        self.sessionID = None
        self.apiversion = list()
        self.client = Client
        self.threadID = threadID
        self.name = name
        self.disbleThread = False
        self._timeout = 2

    def run(self):
        logging.info('Start session thread ...')
        self._Theady_KeepAlive()
        logging.info('Session thread stop ...  ')

    def _Theady_KeepAlive(self):
        while not self.disbleThread:
            try:
                if self.client._acvite == False:
                    time.sleep(self._timeout)
                    if self.client._acvite == False:
                        self._keep_alive()
                else:
                    self.client._acvite = False
            except Exception as E:
                pass

    def _getApiInfo(self):
        logging.debug('trying to get api information ...')
        for i in range(3):
            _status_code, _hearders, _text = self.client._Http.invokeAPI(httpMethod=RestConstant.GET,
                                                                         function_uri=RestConstant.SERVICE_DESCRIPTION_URI,
                                                                         payload=None)
            if _status_code == 200:
                _response = json.loads(_text)
                if 'apiVersion' in _response and 'version' in _response:
                    self.apiversion.append(_response['apiVersion'])
                    self.apiversion.append(_response['version'])
                    logging.info('Get PLCnext API version : {}'.format(self.apiversion[1]))
                    return
                else:
                    logging.error('Can not recognize API')
                    raise RESTException('Can not recognize API')

            # 其他状态字以后再议
        logging.error('Status return code is unexcepted')
        raise RESTException('Status return code is unexcepted')

    def _createSessionID(self):
        logging.debug('trying to creat session id ...')
        for i in range(3):
            _randint = random.randint(100, 999)
            _payload = 'stationID=' + str(_randint)
            _status_code, _hearders, _text = self.client._Http.invokeAPI(httpMethod=RestConstant.POST,
                                                                         function_uri=RestConstant.CREATE_SESSION_URI,
                                                                         payload=_payload)
            if _status_code == 201:
                _response = json.loads(_text)
                if 'sessionID' in _response:
                    self.sessionID = _response['sessionID']
                    logging.info('Get session ID : {}'.format(self.sessionID))
                    return
            if _status_code == 409:  # 冲突
                pass
        logging.error('Can not creat session ID')
        raise RESTException('Can not creat session ID')

    def _maintainSessionID(self):
        logging.debug('Maintain SessionID ...')
        _uri = RestConstant.MAINTAIN_SESSION_URI + self.sessionID
        for i in range(3):
            _status_code, _hearders, _text = self.client._Http.invokeAPI(httpMethod=RestConstant.POST,
                                                                         function_uri=_uri,
                                                                         payload=None)
            if _status_code == 200:
                return
            if _status_code == 410:  # ID失效
                logging.error('invalidSessionID')
                raise RESTException('invalidSessionID')

        _r = json.loads(_text)
        logging.error('Can not maintain session ID' + str(_r))
        raise RESTException('Can not maintain session ID' + str(_r))

    def _keep_alive(self):
        print('----------')
        _retryConut = 0
        if self.sessionID == None:
            self._getApiInfo()
            if self.apiversion[1] == 'v1.2':
                self._createSessionID()
        while True:
            try:
                self._maintainSessionID()
                return
            except RESTException as E:
                if 'invalidSessionID' in E.message and _retryConut < 2:
                    self.sessionID = None
                    _retryConut += 1
                    self._createSessionID()
                else:
                    raise E

