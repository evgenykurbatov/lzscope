# -*- coding: utf-8 -*-

import logging

import config



def setup():
    logger = logging.getLogger(config.LOGGER_NAME+"."+__name__)
#    logger = logging.getLogger("aaa")
    logger.debug("setup: ...")
    logger.debug("setup: ok")
