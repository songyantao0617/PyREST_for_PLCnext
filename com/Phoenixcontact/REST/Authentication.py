import json
import logging.config
import uuid

from com.Phoenixcontact.REST.RESTException import *
from com.Phoenixcontact.REST.RESTHttpClient import *


class Authentication(object):

    def __getAuthToken(self):
        logging.debug('getAuthToken ...')
        self.authToken = None
        self.accessToken = None
        _uuid = str(uuid.uuid1())
        _payload = {'state': _uuid,
                    'scope': RestConstant.TEMPORARY_TOCKEN_BODY_SCOPE_VALUES}

        for i in range(3):
            _status_code, _hearders, _text = RESTHttpClient.invokeAPI(httpMethod=RestConstant.POST,
                                                                      function_uri=RestConstant.TEMPORARY_TOCKEN_URI,
                                                                      clientInfo=self,
                                                                      payload=json.dumps(_payload))
            if _status_code == 200:
                _response = json.loads(_text)
                if _response['state'] == _uuid:
                    self.authToken = _response['code']
                    break

    @staticmethod
    def _Login(self):
        logging.debug('logging ...')
        for i in range(3):
            Authentication.__getAuthToken(self)
            _payload = {
                'code': self.authToken,
                'grant_type': 'authorization_code',
                'username': self.PLCnUserName,
                'password': self.PLCnPasswd
            }
            _status_code, _hearders, _text = RESTHttpClient.invokeAPI(httpMethod=RestConstant.POST,
                                                                      function_uri=RestConstant.ACCESS_TOCKEN_URI,
                                                                      clientInfo=self,
                                                                      payload=json.dumps(_payload))
            if _status_code == 200:
                _response = json.loads(_text)
                if _response['state'] == self.authToken:
                    self.accessToken = _response['access_token']
                    break
            elif _status_code == 401:
                _response = json.loads(_text)
                _reason = _response['error']['details'][0]['reason']
                if _reason == 'wrongPassword':
                    logging.error('Wrong password')
                    raise RESTException('Wrong password')
