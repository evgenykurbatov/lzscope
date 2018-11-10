# -*- coding: utf-8 -*-

from __future__ import print_function
import logging

import app
import app.config as config



if __name__ == "__main__":
    config.from_object('config', verbose=True)

    ## Init logger
    logger = logging.getLogger(config.LOGGER_NAME)
    logger_formatter = logging.Formatter(config.LOGGER_FORMAT)
    logger.setLevel(logging.DEBUG)
    logger_console_handler = logging.StreamHandler()
    logger_console_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_console_handler)

    logger.debug("Initialization ...")

    app.setup()

    logger.debug("Initialization ok")
