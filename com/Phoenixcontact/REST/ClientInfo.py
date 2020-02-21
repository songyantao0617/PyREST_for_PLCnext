import ipaddress
import logging.config

from com.Phoenixcontact.default import *

class ClientInfo(object):

    def __init__(self):
        self._Ip = DefaultValue.IP
        self._UserName = DefaultValue.USERNAME
        self._PassWord = DefaultValue.PASSWD
        self._Port = DefaultValue.PORT
        self.accessToken = None
        self.authToken = None
        self.groupInfo = None
        self.groupReportResult = None

    def __getPassword(self):
        return self._PassWord

    def __setPassWord(self, Password):
        logging.debug("setting password...")
        if isinstance(Password, str):
            self._PassWord = Password
        else:
            logging.error('Password must be \'str\' type')

    def __getUserName(self):
        return self._UserName

    def __setUserName(self, UserName):
        logging.debug('setting username : {}'.format(UserName))
        if isinstance(UserName, str):
            self._UserName = UserName
        else:
            logging.error('UserName must be \'str\' type')

    def __getPLCnextIp(self):
        return self._Ip

    def __setPLCnextIp(self, PLCnextIp):
        logging.debug('setting IP : {}'.format(PLCnextIp))
        try:
            tmp = ipaddress.ip_address(PLCnextIp)
            self._Ip = str(tmp)
        except ValueError as E:
            logging.error(E)

    def __getPLCnextPort(self):
        return self._Port

    def __setPLCnextPort(self, PLCnextPort):
        logging.debug('setting port : {}'.format(PLCnextPort))
        if isinstance(PLCnextPort, str):
            self._Port = PLCnextPort
        else:
            logging.error('Port must be \'str\' type')

    PLCnIp = property(__getPLCnextIp, __setPLCnextIp)
    PLCnPort = property(__getPLCnextPort, __setPLCnextPort)
    PLCnUserName = property(__getUserName, __setUserName)
    PLCnPasswd = property(__getPassword, __setPassWord)

    def __str__(self):
        return 'IP : ' + self._Ip
