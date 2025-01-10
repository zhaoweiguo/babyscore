#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config
import os

class Logger(object):

    instance = None

    def __init__(self):
        config_file = "config/logger.ini"
        if os.path.exists(config_file):
            logging.config.fileConfig(config_file, encoding="utf-8")
        # 默认的root logger
        self._logger = logging.getLogger()
        # 存储不同名字的logger, 不包括root logger
        self._logger_dict = {}

    @staticmethod
    def get_instance():
        if not Logger.instance:
            Logger.instance = Logger()
        return Logger.instance
    def get_logger(self, name):
        if name not in self._logger_dict:
            self._logger_dict[name] = logging.getLogger(name)
        return self._logger_dict[name]


log=Logger.get_instance().get_logger("")


if __name__ == "__main__":
    log.debug("hello world")
    log.info("hello world")
    log.warning("hello world")
    log.error("hello world")




