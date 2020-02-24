import logging.config

import requests
from requests import RequestException, ReadTimeout
import asyncio, functools

from requests.adapters import HTTPAdapter


class HttpClient_requests(object):

    def __init__(self):
        self.request = requests.Session()
        self.cert = None
        requests.packages.urllib3.disable_warnings()
        # self.loop = asyncio.get_event_loop()

    def mount(self, pool_connections=5, pool_maxsize=120):
        self.request.mount('https://', HTTPAdapter(pool_connections, pool_maxsize))

    def NewSession(self):
        self.request = requests.Session()

    def syncRequest(self, httpMethod, url, headers, payload, Params=None):
        try:
            if self.request == None:
                self.request = requests.Session()
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

    async def asyncRequest(self, httpMethod, url, headers, payload, loop, Params=None):
        try:
            if self.request == None:
                self.request = requests.Session()
            # HttpClient_requests.request.mount('https://', HTTPAdapter(pool_connections=11, pool_maxsize=11))

            # global response
            if httpMethod == "POST":
                future = loop.run_in_executor(None, functools.partial(self.request.post, url, headers=headers,
                                                                      data=payload, cert=self.cert, verify=False,
                                                                      params=Params))

            elif httpMethod == "PUT":
                future = loop.run_in_executor(None, functools.partial(self.request.put, url, headers=headers,
                                                                      data=payload, cert=self.cert, verify=False,
                                                                      params=Params))



            elif httpMethod == "DELETE":
                future = loop.run_in_executor(None, functools.partial(self.request.delete, url, headers=headers,
                                                                      data=payload, cert=self.cert, verify=False,
                                                                      params=Params))


            elif httpMethod == "GET":
                future = loop.run_in_executor(None, functools.partial(self.request.get, url, headers=headers,
                                                                      data=payload, cert=self.cert, verify=False,
                                                                      params=Params))

                response = await future
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


###################################################################################################
import aiohttp


class HttpClient_aiohttp(object):

    def __init__(self):
        self.request = aiohttp.ClientSession()
        self.cert = None
        # requests.packages.urllib3.disable_warnings()
        # self.loop = asyncio.get_event_loop()

        pass

    def mount(self, pool_connections=5, pool_maxsize=120):
        # self.request.mount('https://', HTTPAdapter(pool_connections, pool_maxsize))
        pass

    def NewSession(self):
        # self.request = requests.Session()
        pass

    def syncRequest(self, httpMethod, url, headers, payload, Params=None):
        try:
            if self.request == None:
                self.request = aiohttp.ClientSession()
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
        pass

    async def asyncRequest(self, httpMethod, url, headers, payload, loop, Params=None):
        try:
            if self.request == None:
                self.request = requests.Session()
            # HttpClient_requests.request.mount('https://', HTTPAdapter(pool_connections=11, pool_maxsize=11))

            # global response
            if httpMethod == "POST":

                async with self.request.post(url, headers=headers, data=payload, cert=self.cert, verify=False,
                                             params=Params) as resp:

                    response = await resp

            elif httpMethod == "PUT":
                async with self.request.put(url, headers=headers, data=payload, cert=self.cert, verify=False,
                                             params=Params) as resp:

                    response = await resp

            elif httpMethod == "DELETE":
                async with self.request.delete(url, headers=headers, data=payload, cert=self.cert, verify=False,
                                             params=Params) as resp:

                    response = await resp

            elif httpMethod == "GET":
                async with self.request.get(url, headers=headers, data=payload, cert=self.cert, verify=False,
                                             params=Params) as resp:

                    response = await resp

                # response = resp.
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
        pass
