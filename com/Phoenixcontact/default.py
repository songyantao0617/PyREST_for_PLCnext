import logging


class DefaultValue():
    USERNAME = 'admin'
    PASSWD = '123456'
    PORT = '443'
    IP = '192.168.1.10'

    DEFAULT_LOG_PATH = '/opt/plcnext/logs/'
    DEFAULT_LOG_LEVEL = logging.ERROR
    DEFAULT_LOG_FILENAME = 'OutputPy.log'
