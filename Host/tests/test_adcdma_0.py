# -*- coding: utf-8 -*-

import time
import serial
import binascii
import numpy as np



s = serial.Serial('/dev/ttyACM0')

print("> RESET")
s.write("RESET\0".encode())
print(s.read(3))

print("> ADCDMA 0x8")
s.write("ADCDMA 0x8\0".encode())
print("> RESET")
s.write("RESET\0".encode())
print(s.read(3))
