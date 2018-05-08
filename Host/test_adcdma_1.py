# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import serial
import binascii
import numpy as np



s = serial.Serial('/dev/ttyACM0')

print("> STATUS")
s.write("STATUS\0")
print(s.read(3))

dtype = np.uint16
len_block = 128
dtype_size = dtype(0).itemsize
print("> ADCDMA %d" % (2*len_block))
s.write("ADCDMA %d\0" % (2*len_block))
for i in xrange(5):
    print("> GET")
    s.write("GET\0")
    raw = s.read(len_block*dtype_size)
    block = np.frombuffer(raw, np.dtype(dtype), count=len_block)
    line = "".join(("%04x " % _) for _ in block)
    print(line)
print("> STOP")
s.write("STOP\0")
print(s.read(3))
