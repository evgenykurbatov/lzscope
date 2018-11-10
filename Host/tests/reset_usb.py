# -*- coding: utf-8 -*-

import usb.core
import usb.util

dev = usb.core.find(idVendor=0x0483, idProduct=0x5740)
if dev is None:
    raise ValueError("Device is not found")
#print dev

if dev.is_kernel_driver_active(0):
    ## Detach kernel driver
    print("Detach kernel driver")
    dev.detach_kernel_driver(0)

print("Reset device")
dev.reset()

if not dev.is_kernel_driver_active(0):
    ## Attach kernel driver back
    print("Attach kernel driver")
    dev.attach_kernel_driver(0)
