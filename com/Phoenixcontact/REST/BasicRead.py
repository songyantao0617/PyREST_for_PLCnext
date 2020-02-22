import json
import logging

from com.Phoenixcontact.REST.RESTException import *
from com.Phoenixcontact.REST.RESTHttpClient import *


class BasicRead(object):

    def __init__(self, Client):
        self.Client = Client

    def _ReadVariables(self, variableNames, pathPrefix=RestConstant.PATHPREFIX):
        if self.Client.accessToken == None:
            return

        _data = {
            'pathPrefix': pathPrefix,
            'paths': ','.join(variableNames)
        }

        _status_code, _hearders, _text = self.Client._Http.invokeAPI(httpMethod=RestConstant.GET,
                                                                     function_uri=RestConstant.READ_VARIABLES_GET_URI,
                                                                     payload=None, Params=_data)

        if _status_code == 200:
            _response = json.loads(_text)
            tmp = _response.get('variables')
            _ResultDict = dict()
            for _item in tmp:
                _varFullName = _item.get('path')
                c = _varFullName.index('/')
                _ResultDict[_varFullName[c + 1:]] = _item.get('value')
            return _ResultDict

        elif _status_code == 401:  # 令牌不正确
            self.Client.accessToken = None
            _reason = _hearders.get('WWW-Authenticate')
            raise RESTException(_reason)  # Bearer realm="pxcapi", error="invalid_token"

        elif _status_code == 410:  # sessionID不正确
            logging.error('invalidSessionID')
            raise RESTException('invalidSessionID')
