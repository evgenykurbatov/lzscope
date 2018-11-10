# -*- coding: utf-8 -*-

import numpy as np
import logging
import serial
import time



class Board(object):
    """
    Parameters
    ----------
    logger_base_name : str, optional
        Base name for logger.
    **serial_kwargs : dict, optional
        Argument dictionary for `serial.Serial` constructor.

    Note
    ----
    Exceptions of `Serial` module are logged then transferred upwise.
    """

    def __init__(self, logger_base_name=None, **serial_kwargs):
        logger_name = (logger_base_name+"." if logger_base_name else "") + "board"
        self.logger = logging.getLogger(logger_name)

        self.serial_kwargs = serial_kwargs



    def connect(self):
        """
        """

        self.logger.debug("connect: ...")

        try:
            self.serial = serial.Serial(**self.serial_kwargs)
            #time.sleep(2)
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
        except serial.SerialException as e:
            self.logger.error("disconnect: '%s'" % e)
            raise e

        self.logger.debug("disconnect: ok")



    def write(self, s):
        """
        """

        try:
            self.serial.write(str(s).encode())
        except Exception as e:
            self.logger.error("write:", e)
            raise e



    def cmd_status(self):
        """
        Send 'STATUS' command to the board and wait for an answer.

        Returns
        -------
        str
            Status string.
        """

        self.logger.debug("cmd_status: ...")

        try:
            self.write("STATUS\0")
            status = self.serial.read(3).decode()
        except serial.SerialException as e:
            self.logger.error("cmd_status:", e)
            raise e

        self.logger.debug("cmd_status: '%s'" % status)

        return status



    def cmd_adc(self):
        """
        Send 'ADC' command to the board and wait for an answer.

        Returns
        -------
        int
            Integer with 16-bit meaning part.
        """

        self.logger.debug("cmd_adc: 'ADC'")

        try:
            self.write("ADC\0")
            raw = self.serial.read(4)
            data = np.frombuffer(raw, np.dtype(np.uint16), count=1)
        except serial.SerialException as e:
            self.logger.error("cmd_adc:", e)
            raise e

        self.logger.debug("cmd_adc: '%04x'" % data[0])

        return data[0]



    def cmd_adcdma(self, n):
        """
        Send 'ADCDMA <n>' command to the board and wait for an answer.

        Parameters
        ----------
        n : integer
            Number of samples to read sequentally.

        Returns
        -------
        int
            Integer with 16-bit meaning part.
        """

        self.logger.debug("cmd_adcdma: 'ADCDMA %d'" % n)

        try:
            self.write("ADCDMA %d\0" % n)
            self.write("GET\0")
            raw = self.serial.read(n * np.uint16(0).itemsize)
            data = np.frombuffer(raw, np.dtype(np.uint16), count=n)
            self.cmd_stop()
        except serial.SerialException as e:
            self.logger.error("cmd_adcdma:", e)
            raise e

        self.logger.debug("cmd_adcdma: %d samples ok" % n)

        return data



    def cmd_stop(self):
        """
        Send 'STOP' command to the board and wait for an answer.
        """

        self.logger.debug("cmd_stop: ...")

        try:
            self.write("STOP\0")
            status = self.serial.read(3).decode()
        except serial.SerialException as e:
            self.logger.error("cmd_stop:", e)
            raise e

        self.logger.debug("cmd_stop: '%s'" % status)
