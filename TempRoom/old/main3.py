#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Copyright (C) 2021  George Farris <farrisg@gmsys.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Anemometer.py is reference code to read a PR-3000-FS-N01, RS465 Anemometer
# on a raspberry pi 4 using a Waveshare 2 channel RS485 HAT.
# https://www.waveshare.com/2-ch-rs485-hat.htm

import serial
import os
import sys
import time
import RPi.GPIO as GPIO

SERIAL_PORT = "/dev/ttySC0"
TXDEN_1 = 27
TXDEN_2 = 22

# Calculate CRC16 Checksum
def _crc16(data, no):
    crc = 0xffff
    poly = 0xa001   # Polynomial used for Modbus RS485 applications
    temp = no

    while True:
        crc ^= data[temp - no]        
        for i in range(0, 8):
            if crc & 0x0001:
                crc = (crc>>1) ^ poly
            else:
                crc >>= 1
        no -= 1;
        if no == 0:
            break

    return crc & 0xffff

# Open the serial port at 4800 buad
ser = serial.Serial(port=SERIAL_PORT, baudrate=115200)

# Set the mode on the Raspberry Pi GPIO
GPIO.setmode(GPIO.BCM)
# Set this to avoid warning of channel in use
GPIO.setwarnings(False)

# Set the GPIO pin as output for port 1 and 2 on the WAVESHARE RS485 HAT (SC16IS752)
# and then set the bit HIGH to enable the ports
GPIO.setup(TXDEN_1, GPIO.OUT)
GPIO.setup(TXDEN_2, GPIO.OUT)
GPIO.output(TXDEN_1, GPIO.HIGH)
GPIO.output(TXDEN_2, GPIO.HIGH)

# Now lets setup and inquiry packaet for the PR-3000-FS-N01, RS485 Anemometer

# Set the length of the transmit buffer
tx_buf = [0] * 8
tx_buf[0] = 1    # MODBUS ID
tx_buf[1] = 3    # MODBUS Function code (read holding register)
tx_buf[2] = 0    # Starting address of register - High byte
tx_buf[3] = 1    # Low byte
tx_buf[4] = 0    # How many registers to read - High byte
tx_buf[5] = 1    # Low byte

# Get the CRC of the packet
crc = _crc16(bytearray(tx_buf), 6)
# Add the crc bytes to the end of the transmit buffer
tx_buf[6] = (crc & 0x00ff)
tx_buf[7] = ((crc >> 8) & 0xff)

# pack the buffer
data = bytearray(tx_buf)

# Set board in transmit mode and write data
GPIO.output(TXDEN_1, GPIO.LOW) 
ser.write(data)
# Waiting to finish sending
time.sleep(0.01)
# Set board to receive mode
GPIO.output(TXDEN_1, GPIO.HIGH)

""" NOT USED
# get six bytes plus crc = 8 bytes total
data_t = [0] * 8
for i in range(7):
    data_t[i] = ser.read(1)

# Current wind speed example: 0056 H (hexadecimal) = 86 => Winds = 8.6m / s
# Add bytes 3 and 4 then divide by 10 to get meters per second
# Then divide by 1000 to get Kilometers per second
# now mutitply by 3600 to get kmh
ms = float(data_t[3] + data_t[4])
print(ms)

# Typical response example
#b'\x01'
#b'\x03'
#b'\x02'
#b'\x00'
#b'\x56' Current wind speed: 0056 H (hexadecimal) = 86 => Winds = 8.6m / s
#b'\xb8'
#b'D'
"""

