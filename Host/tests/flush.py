# -*- coding: utf-8 -*-

import time
import serial



s = serial.Serial('/dev/ttyACM0')

while True:
    print(s.readline())
