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
            self.serial = serial.serial_for_url(**self.serial_kwargs)
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



    def cmd_reset(self):
        """
        Send ``RESET\0`` command to the board and wait for an answer.

        Returns
        -------
        str
            b``OK\0``.
        """

        self.logger.debug("cmd_reset: ...")

        try:
            self.write("RESET\0")
            res = self.serial.read(3).decode()
        except serial.SerialException as e:
            self.logger.error("cmd_reset:", e)
            raise e

        self.logger.debug("cmd_reset: '%s'" % res)

        return res



    def cmd_adc1(self):
        """
        See `cmd_adc_p`.
        """
        return self.cmd_adc_p(1)



    def cmd_adc2(self):
        """
        See `cmd_adc_p`.
        """
        return self.cmd_adc_p(2)



    def cmd_adc_p(self, p):
        """
        Send ``ADC<p>\0`` command to the board and wait for an answer.

        Parameters
        ----------
        p : integer
            Port number.

        Returns
        -------
        int
            Integer with 16-bit meaning part.
        """

        self.logger.debug("cmd_adc_p: 'ADC%d'" % p)

        try:
            self.write("ADC%d\0" % p)
            raw = self.serial.read(4)
            data = np.frombuffer(raw, np.dtype(np.uint16), count=1)
        except serial.SerialException as e:
            self.logger.error("cmd_adc_p:", e)
            raise e

        self.logger.debug("cmd_adc_p: '%04x'" % data[0])

        return data[0]



    def cmd_adc1dma(self, n):
        """
        See `cmd_adc_p`.
        """
        return self.cmd_adcdma_p(1, n)



    def cmd_adc2dma(self, n):
        """
        See `cmd_adc_p`.
        """
        return self.cmd_adcdma_p(2, n)



    def cmd_adcdma_p(self, p, n):
        """
        Send ``ADC<p>DMA <n>\0`` command to the board and wait for an answer.

        Parameters
        ----------
        p : integer
            Port number.
        n : integer
            Number of samples to read sequentally.

        Returns
        -------
        int
            Integer with 16-bit meaning part.
        """

        self.logger.debug("cmd_adcdma: 'ADC%dDMA %d'" % (p, n))

        try:
            self.write("ADC%dDMA %d\0" % (p, n))
            self.write("GET\0")
            raw = self.serial.read(n * np.uint16(0).itemsize)
            data = np.frombuffer(raw, np.dtype(np.uint16), count=n)
            self.cmd_reset()
        except serial.SerialException as e:
            self.logger.error("cmd_adcdma_p:", e)
            raise e

        self.logger.debug("cmd_adcdma_p: %d samples ok" % n)

        return data
