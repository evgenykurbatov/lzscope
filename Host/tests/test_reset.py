# -*- coding: utf-8 -*-

import time
import serial



s = serial.Serial('/dev/ttyACM0')

for i in range(5):
    print("> RESET")
    s.write("RESET\0".encode())
    print(s.read(3))
