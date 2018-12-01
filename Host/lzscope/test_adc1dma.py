# -*- coding: utf-8 -*-

import logging

import board



## Init logger
logger = logging.getLogger("")
logger_formatter = logging.Formatter("%(levelname)s: %(name)s - %(message)s")
logger.setLevel(logging.DEBUG)
logger_console_handler = logging.StreamHandler()
logger_console_handler.setFormatter(logger_formatter)
logger.addHandler(logger_console_handler)

board = board.Board(url="hwgrep://0483:5740")

board.connect()

print("--------------------")
board.cmd_reset()

print("--------------------")
data = board.cmd_adc1()
print("ADC1: %04x" % data)

print("--------------------")
n = 6
data = board.cmd_adc1dma(n)
print("ADC1DMA %d: " % n + "".join(("%04x " % _) for _ in data))

print("--------------------")
board.disconnect()
