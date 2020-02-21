import json

from com.Phoenixcontact.REST.RESTException import *
from com.Phoenixcontact.REST.RESTHttpClient import *


class SendData(object):

    @staticmethod
    def _SendOUT(self, variables, pathPrefix=RestConstant.PATHPREFIX):
        _data = {
            'pathPrefix': pathPrefix,
            'variables': variables
        }

        _status_code, _hearders, _text = RESTHttpClient.invokeAPI(httpMethod=RestConstant.PUT,
                                                                  function_uri=RestConstant.WRITE_VARIABLES_PUT_URI,
                                                                  clientInfo=self,
                                                                  payload=json.dumps(_data))

        if _status_code == 200:
            _response = json.loads(_text)
            return _response.get('variables')

        elif _status_code == 401:  # 令牌不正确
            self.accessToken = None
            _reason = _hearders.get('WWW-Authenticate')
            raise RESTException(_reason)  # Bearer realm="pxcapi", error="invalid_token"

    @staticmethod
    def _SendData(clientInfo, variablesDict, pathPrefix=RestConstant.PATHPREFIX):

        _variables = list()
        for _item in variablesDict.items():
            currentItem = dict()
            currentItem['path'] = _item[0]
            currentItem['value'] = _item[1]
            _variables.append(currentItem)

        _Result = SendData._SendOUT(clientInfo, _variables, pathPrefix)

        ErrList = list()
        for _item in _Result:
            if _item.get('value') == None:
                varFullName = _item.get('path')
                c = varFullName.index('/')
                var = varFullName[c + 1:]
                ErrList.append(var)
        return ErrList
