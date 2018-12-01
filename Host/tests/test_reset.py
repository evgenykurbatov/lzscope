# -*- coding: utf-8 -*-

import time
import serial



s = serial.serial_for_url(url="hwgrep://0483:5740")

for i in range(5):
    print("> RESET")
    s.write("RESET\0".encode())
    print(s.read(3))
