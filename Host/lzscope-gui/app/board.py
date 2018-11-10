# -*- coding: utf-8 -*-

import logging
import serial



class Board(object):
    """
    Parameters
    ----------
    logger
        Logger instance.
    *serial_args : list, optional
        Argument list for `serial.Serial` constructor.
    **serial_kwargs : dict, optional
        Argument dictionary for `serial.Serial` constructor.

    Note
    ----
    Exceptions of `Serial` module are logged then transferred upwise.
    """

    def __init__(self, logger_name, *serial_args, **serial_kwargs):
        self.logger = logging.getLogger(logger_name)

        self.serial_args = *serial_args
        self.serial_kwargs = **serial_kwargs



    def connect(self):
        """
        """

        self.logger.debug("connect: ...")

        try:
            self.serial = serial.Serial(*self.serial_args, **self.serial_kwargs)
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
        except Exception as e:
            self.logger.error("connect: '%s'" % e)
            raise e

        self.logger.debug("connect: ok")



    def disconnect(self):
        """
        """

        self.logger.debug("disconnect: ...")

        try:
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
            self.serial.close()
        except Exception as e:
            self.logger.error("disconnect: '%s'" % e)
            raise e

        self.logger.debug("disconnect: ok")



    def cmd_status(self):
        """
        Send "STATUS" command to the board and wait for an answer.

        Returns
        -------
        str
            Status string.
        """

        self.logger.debug("cmd_status: ...")

        try:
            self.serial.write("STATUS\0")
            status = self.serial.read(3).decode()
        except Exception as e:
            self.logger.error("cmd_status: '%s'" % status)
            raise e

        self.logger.debug("cmd_status: '%s'" % status)

        return status
