#!/usr/bin/python
# usage: reset_arduino <DEVICE>
# where <DEVICE> is typically some /dev/ttyfoobar
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys

import serial

ser = serial.Serial()
ser.port = sys.argv[1]
ser.baudrate = 1200
ser.open()
ser.close()
