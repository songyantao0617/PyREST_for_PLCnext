import logging
import os
from logging.handlers import RotatingFileHandler
from com.Phoenixcontact.default import DefaultValue



class Log(object):
    def setLogConfig(self,
                     logPath=DefaultValue.DEFAULT_LOG_PATH,
                     level=DefaultValue.DEFAULT_LOG_LEVEL,
                     logFilename=DefaultValue.DEFAULT_LOG_FILENAME):
        if level == 0:
            return
        if logPath == None:
            logPath = DEFAULT_LOG_PATH
        logger = logging.getLogger()
        logger.setLevel(level)
        if os.path.exists(logPath):
            filename = str(logPath) + logFilename
        else:
            os.makedirs(logPath, 0o777)
            filename = str(logPath) + logFilename
        Rthandler = RotatingFileHandler(filename=filename, maxBytes=1024 * 1024, backupCount=5)
        formatter = logging.Formatter(datefmt='%Y-%m-%d %A %H:%M:%S',
                                      fmt='%(asctime)s  [%(levelname)s]:  %(funcName)s  %(message)s')
        Rthandler.setFormatter(formatter)
        logger.addHandler(Rthandler)

    def LogTest(self):
        log = Log()
        log.setLogConfig()
        logging.debug('logger debug-debug message')
        logging.info('logger info-info message')
        logging.warning('logger warning-warning message')
        logging.error('logger error-error message')
        logging.critical('logger critical-critical message')
        print("Log output succeeded!")


if __name__ == "__main__":
    log = Log()

    # LogTest
    log.LogTest()
