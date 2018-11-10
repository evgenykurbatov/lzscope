# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import serial



s = serial.Serial('/dev/ttyACM0')

for i in xrange(5):
    print("> STATUS")
    s.write("STATUS\0")
    print(s.read(3))
