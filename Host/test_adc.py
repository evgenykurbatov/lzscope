# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import serial
import numpy as np



s = serial.Serial('/dev/ttyACM0')

for i in xrange(5):
    print("> ADC")
    s.write("ADC\0")
    raw = s.read(4)
    data = np.frombuffer(raw, np.dtype(np.uint16), count=1)
    print("%04x" % data)
