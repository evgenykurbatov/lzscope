# -*- coding: utf-8 -*-

import time
import serial
import numpy as np



s = serial.serial_for_url(url="hwgrep://0483:5740")

print("*** ADC1")
for i in range(5):
    print("> ADC1")
    s.write("ADC1\0".encode())
    raw = s.read(4)
    data = np.frombuffer(raw, np.dtype(np.uint16), count=1)
    print("%04x" % data[0])

print("*** ADC2")
for i in range(5):
    print("> ADC2")
    s.write("ADC2\0".encode())
    raw = s.read(4)
    data = np.frombuffer(raw, np.dtype(np.uint16), count=1)
    print("%04x" % data[0])
