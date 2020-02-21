import logging.config

import requests
from requests import RequestException, ReadTimeout
from requests.adapters import HTTPAdapter


class HttpClient(object):
    requests.packages.urllib3.disable_warnings()
    cert = None

    @staticmethod
    def invokeAPI2(httpMethod, url, headers, payload, Params=None):
        try:
            request = requests.Session()
            request.mount('https://', HTTPAdapter(pool_connections=11, pool_maxsize=11))

            # global response
            if httpMethod == "POST":
                response = requests.post(url, headers=headers, data=payload, cert=HttpClient.cert, verify=False,
                                         params=Params)
            elif httpMethod == "PUT":
                response = request.put(url, headers=headers, data=payload, cert=HttpClient.cert, verify=False,
                                       params=Params)
            elif httpMethod == "DELETE":
                response = request.delete(url, headers=headers, data=payload, cert=HttpClient.cert, verify=False,
                                          params=Params)
            elif httpMethod == "GET":
                response = request.get(url, headers=headers, data=payload, cert=HttpClient.cert, verify=False,
                                       params=Params)
            logging.debug(url), logging.debug(headers), logging.debug(payload), logging.debug(response.text)

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
