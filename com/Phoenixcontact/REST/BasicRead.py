import json

from com.Phoenixcontact.REST.RESTException import *
from com.Phoenixcontact.REST.RESTHttpClient import *


class BasicRead(object):

    @staticmethod
    def _ReadVariables(self, variableNames, pathPrefix=RestConstant.PATHPREFIX):
        if self.accessToken == None:
            return

        _data = {
            'pathPrefix': pathPrefix,
            'paths': ','.join(variableNames)
        }

        _status_code, _hearders, _text = RESTHttpClient.invokeAPI(httpMethod=RestConstant.GET,
                                                                  function_uri=RestConstant.READ_VARIABLES_GET_URI,
                                                                  clientInfo=self,
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
            self.accessToken = None
            _reason = _hearders.get('WWW-Authenticate')
            raise RESTException(_reason)  # Bearer realm="pxcapi", error="invalid_token"
