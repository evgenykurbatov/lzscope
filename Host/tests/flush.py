# -*- coding: utf-8 -*-

import time
import serial



s = serial.serial_for_url(url="hwgrep://0483:5740")

while True:
    print(s.readline())
