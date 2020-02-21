from com.Phoenixcontact.REST.Constant import RestConstant
from com.Phoenixcontact.utils.Http import *


class RESTHttpClient(HttpClient):

    @staticmethod
    def invokeAPI(httpMethod, function_uri, payload, clientInfo, Params=None):
        url = RestConstant.BASE_URL + clientInfo.PLCnIp + ':' + clientInfo.PLCnPort + '/' + function_uri
        if clientInfo.accessToken == None:
            headers = {
                RestConstant.HEADER_TYPE: RestConstant.HEADER_TYPE_JSON
            }
        else:
            headers = {
                RestConstant.HEADER_TYPE: RestConstant.HEADER_TYPE_JSON,
                RestConstant.HEADER_AUTH: RestConstant.HEADER_BEARER + clientInfo.accessToken,
            }
        return HttpClient.invokeAPI2(httpMethod, url, headers, payload, Params)
