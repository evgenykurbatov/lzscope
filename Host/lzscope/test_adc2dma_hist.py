# -*- coding: utf-8 -*-

import time
import numpy as np
import scipy
import scipy.stats
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt

import board



## Init logger
logger = logging.getLogger("")
logger_formatter = logging.Formatter("%(levelname)s: %(name)s - %(message)s")
logger.setLevel(logging.ERROR)
logger_console_handler = logging.StreamHandler()
logger_console_handler.setFormatter(logger_formatter)
logger.addHandler(logger_console_handler)

board = board.Board(url="hwgrep://0483:5740")
board.connect()
board.cmd_reset()

m = 10
n = 16384
dump = np.nan * np.zeros((m, n), dtype=np.uint16)

t1 = time.time()
for i in range(m):
    dump[i,:] = board.cmd_adc2dma(n)
t2 = time.time()
print("done in %.2e sec, rate is %.2f bps\n" % ((t2-t1), m*n*np.uint16(0).itemsize/(t2-t1)))

print(scipy.stats.describe(dump.flatten()))

hist = scipy.stats.itemfreq(dump.flatten())
plt.figure()
plt.bar(hist[:,0], hist[:,1], width=1.0, edgecolor=None)
plt.show()

board.disconnect()
