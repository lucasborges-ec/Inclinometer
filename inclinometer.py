
import time
time.sleep(30) #Wainting for the end of booting time

import serial
import struct
import numpy as np
import spidev


#-----------------------------------------------------------------------------------#
'''
Recebe infomações preliminares como 'porta' e 'baudrate' a fim de dar início à
comunicação serial
'''
def intConfig(port, baudRate):
    global ser
    ser = serial.Serial(port, baudRate, timeout=1)
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = 8                              # Tamanho do byte
    ser.parity = serial.PARITY_NONE               # Não há verificação de paridade

    print ("Serial port opened " + port + " over Baudrate " + str(baudRate))

    return ser
#-----------------------------------------------------------------------------------#
def readSensor(spi):
    start=spi.xfer([0b00000000, 0x0,0x0])
    d1a=spi.xfer([0b00010000, 0x0, 0x0])        # Sending 2 additional bytes (0x0) in order to have enough time to receave 11 bits from the sensor
    d1b=spi.xfer([0b00010001, 0x0, 0x0])        # Try xfer2!!!
    x1=( d1a[1] << 8 ) + d1a[2] >> 5                                           # 11 bits in 2 bytes size mensage
    y1=( d1b[1] << 8 ) + d1b[2] >> 5
    a=(x1-y1)/6554.0
    return a
#-----------------------------------------------------------------------------------#

# Creates a object
spi1=spidev.SpiDev()
spi2=spidev.SpiDev()

# Starts SPI communication
spi1.open(0,0)
spi2.open(0,1)

# SPI settings
spi1.max_speed_hz = 5000
spi2.max_speed_hz = 5000
spi1.mode = 0b00    # Look for this information in datasheet!!!!!
spi2.mode = 0b00

#Starts serial communication
port=['/dev/ttyS0','/dev/ttyAMA0']
baudRate=9600

ser=intConfig(port[1], baudRate)

# READING SENSORS

samples=50
#std=np.deg2rad(np.sin(0.3)) #graus
std=0.3
avr1=np.zeros(samples)
avr2=np.zeros(samples)

try:
    while True:
        for i in range (samples):
            avr1[i]=np.rad2deg(np.arcsin(readSensor(spi1)))
            avr2[i]=np.rad2deg(np.arcsin(readSensor(spi2)))
        if (np.std(avr1)<std or np.std(avr2)<std):
            data1=struct.pack('d',np.mean(avr1))
            data2=struct.pack('d',np.mean(avr2))

            ser.write('<'.encode())
            ser.write('<'.encode())
            ser.write(data1)
            ser.write(data2)
            print(np.mean(avr1))
            print(np.mean(avr2))
        else:
            ser.write('ERROR'.encode())
except KeyboardInterrupt:
    spi1.close()
    spi2.close()
