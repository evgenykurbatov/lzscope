# -*- coding: utf-8 -*-

import time
import serial
import binascii
import numpy as np



s = serial.serial_for_url(url="hwgrep://0483:5740")

print("> RESET")
s.write("RESET\0".encode())
print(s.read(3))

print("> ADC1DMA 0x8")
s.write("ADC1DMA 0x8\0".encode())
print("> RESET")
s.write("RESET\0".encode())
print(s.read(3))
