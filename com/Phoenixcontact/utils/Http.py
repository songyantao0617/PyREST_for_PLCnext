import logging.config

import requests
from requests import RequestException, ReadTimeout



class HttpClient(object):

    def __init__(self):
        self.request = requests.Session()
        self.cert = None
        requests.packages.urllib3.disable_warnings()

    def invokeAPI2(self, httpMethod, url, headers, payload, Params=None):
        try:
            if self.request == None:
                self.request = requests.Session()
            # HttpClient.request.mount('https://', HTTPAdapter(pool_connections=11, pool_maxsize=11))

            # global response
            if httpMethod == "POST":
                response = self.request.post(url, headers=headers, data=payload, cert=self.cert, verify=False,
                                             params=Params)
            elif httpMethod == "PUT":
                response = self.request.put(url, headers=headers, data=payload, cert=self.cert, verify=False,
                                            params=Params)
            elif httpMethod == "DELETE":
                response = self.request.delete(url, headers=headers, data=payload, cert=self.cert, verify=False,
                                               params=Params)
            elif httpMethod == "GET":
                response = self.request.get(url, headers=headers, data=payload, cert=self.cert, verify=False,
                                            params=Params)

            # logging.debug(url), logging.debug(headers), logging.debug(payload), logging.debug(response.text)

            return response.status_code, response.headers, response.text


        except ReadTimeout as e:
            logging.error(e)
            raise ReadTimeout(e)
        except ConnectionError as e:
            logging.error(e)
            raise ConnectionError(e)
        except RequestException as e:
            logging.error(e)
            raise RequestException(e)
        except Exception as e:
            logging.error(e)
            raise Exception(e)
