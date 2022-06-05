import traceback
import sys
import logging
import dotenv
import requests
import os
from enum import Enum
from pathlib import Path
import sys


class Config:
    __CONFIG = dict()
    __DOTENVPATH = None

    def __init__(self):
        if len(self.__CONFIG) == 0:
            self.loadConfig()
            self.__configLogger(self)

    def loadConfig(self, dotenvPath=None):
        if not dotenvPath:
            dotenvPath = dotenv.find_dotenv()

        # TODO: decide whether to fail or attempt rescue via .env.example
        dotenvPath = ".env.example" if not dotenvPath else dotenvPath
        config = dotenv.dotenv_values(dotenvPath)

        self.__CONFIG = config
        self.__DOTENVPATH = dotenvPath

    def globalExceptionHandler(self, exctype, value, tb):
        logger = logging.getLogger(__name__)
        logger.error(exctype)
        logger.error(value)
        logger.error(traceback.extract_tb(tb))

    @property
    def data(self):
        return self.__CONFIG

    @data.setter
    def data(self, data):
        self.__CONFIG = data

    @staticmethod
    def __configLogger(self):
        logspath = self.get("LOGSPATH")
        logspath = "./" if not logspath else logspath
        logging.basicConfig(
            filename=f"{logspath}/execution.log",
            filemode="a+",
            format="%(asctime)s, %(msecs)d %(name)s %(levelname)s [ %(filename)s-%(lineno)d-%(funcName)20s() ]  : %(message)s",
            # format="%(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )
        sys.excepthook = Config.globalExceptionHandler

    def set(self, key, value, saveToEnv=False):
        if saveToEnv:
            dotenv.set_key(self.__DOTENVPATH, key, value)
        return self.__CONFIG.update({key: value})

    def get(self, key):
        return self.__CONFIG.get(key)

    def getLogger(self, name):
        return logging.getLogger(name)

    # TODO create @properties for all compulsory configuration varibles in .env

    # def __customize(self):
    #   self.set(
    #     'AUTH_PARAMS_PRESETS_SHIP',
    #     {
    #       'preprocessTokenEndpointResponse':True,
    #       'tokenEndpointResponsePreprocessor': Auth.parseSHIPTokenEndpointResponse,
    #       'headers':{'Acept':'*/*'}
    #     }
    #   )
