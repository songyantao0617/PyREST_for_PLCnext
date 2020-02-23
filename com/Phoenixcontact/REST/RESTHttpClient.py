from com.Phoenixcontact.REST.Constant import RestConstant
from com.Phoenixcontact.utils.Http import HttpClient
import asyncio

class RESTHttpclient(HttpClient):
    def __init__(self,Client):
        super().__init__()
        self.Client = Client



    def syncHttpAPI(self, httpMethod, function_uri, payload, Params=None, headers_=None):

        self.Client._acvite = True
        if self.Client.sessionMode and self.Client._Session.sessionID != None:

            if Params == None:
                Params = dict()
            Params[RestConstant.SESSIONID] = self.Client._Session.sessionID

        url = RestConstant.BASE_URL + self.Client.PLCnIp + ':' + self.Client.PLCnPort + '/' + function_uri
        if headers_ == None:

            if self.Client.accessToken == None:
                headers = {
                    RestConstant.HEADER_TYPE: RestConstant.HEADER_TYPE_JSON
                }
            else:
                headers = {
                    RestConstant.HEADER_TYPE: RestConstant.HEADER_TYPE_JSON,
                    RestConstant.HEADER_AUTH: RestConstant.HEADER_BEARER + self.Client.accessToken,
                    'Connection': 'keep-alive'
                }
            headers_ = headers

            return self.syncRequest(httpMethod, url, headers_, payload, Params)

    async def asyncHttpAPI(self, httpMethod, function_uri, payload,loop=None,Params=None,headers_=None):
        self.Client._acvite = True
        if self.Client.sessionMode and self.Client._Session.sessionID != None:

            if Params == None:
                Params = dict()
            Params[RestConstant.SESSIONID] = self.Client._Session.sessionID

        url = RestConstant.BASE_URL + self.Client.PLCnIp + ':' + self.Client.PLCnPort + '/' + function_uri
        if headers_ == None:

            if self.Client.accessToken == None:
                headers = {
                    RestConstant.HEADER_TYPE: RestConstant.HEADER_TYPE_JSON
                }
            else:
                headers = {
                    RestConstant.HEADER_TYPE: RestConstant.HEADER_TYPE_JSON,
                    RestConstant.HEADER_AUTH: RestConstant.HEADER_BEARER + self.Client.accessToken,
                    'Connection': 'keep-alive'
                }
            headers_ = headers

            return await self.asyncRequest(httpMethod, url, headers_, payload,loop,Params)