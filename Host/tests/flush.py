# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import serial



s = serial.Serial('/dev/ttyACM0')

while True:
    print(s.readline())
