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

print("> ADCDMA 0x8")
s.write("ADCDMA 0x8\0")
print("> STOP")
s.write("STOP\0")
print(s.read(3))
