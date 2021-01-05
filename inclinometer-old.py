#!/usr/bin/env python

import spidev
import time
import datetime
import os

# Creates a object
spi1=spidev.SpiDev()
spi2=spidev.SpiDev()

# Starts SPI communication
spi1.open(0,0)
spi2.open(0,1)

# SPI settings
spi1.max_speed_hz = 5000
spi2.max_speed_hz = 5000
spi1.mode = 0b01    # Look for this information in datasheet!!!!!
spi2.mode = 0b01


# READING SENSORS
# Sensor 1
d1=spi1.xfer([0b00010000, 0x0, 0x0])        # Sendind 2 additional bytes (0x0) in order to have enough time to receave 11 bits from the sensor
d2=spi1.xfer([0b00010001, 0x0, 0x0])        # Try xfer2!!!
x=( d1[1] << 8 ) + d1[2] >> 5                                           # 11 bits in 2 bytes size mensage
y=( d2[1] << 8 ) + d2[2] >> 5
a1=(x-y)/6554.0

# Sensor 2
d1=spi2.xfer([0b00010000, 0x0, 0x0])
d2=spi2.xfer([0b00010001, 0x0, 0x0])
x=( d1[1] << 8 ) + d1[2] >> 5
y=( d2[1] << 8 ) + d2[2] >> 5
a2=(x-y)/6554.0