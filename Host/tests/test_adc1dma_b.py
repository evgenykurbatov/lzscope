# -*- coding: utf-8 -*-

import time
import serial
import binascii
import numpy as np



s = serial.serial_for_url(url="hwgrep://0483:5740")

print("> RESET")
s.write("RESET\0".encode())
print(s.read(3))

dtype = np.uint16
len_block = 16
dtype_size = dtype(0).itemsize
print("> ADC1DMA %d" % len_block)
s.write(("ADC1DMA %d\0" % len_block).encode())
for i in range(5):
    print("> GET")
    s.write("GET\0".encode())
    raw = s.read(len_block*dtype_size)
    block = np.frombuffer(raw, np.dtype(dtype), count=len_block)
    line = "".join(("%04x " % _) for _ in block)
    print(line)
print("> RESET")
s.write("RESET\0".encode())
print(s.read(3))
