import spidev
import time
import datetime
import os
import numpy as np
import serial
import struct


#-----------------------------------------------------------------------------------#
'''
Recebe infomações preliminares como 'porta' e 'baudrate' a fim de dar início à
comunicação serial
'''
def intConfig(port, baudRate):
    global ser                                       
    ser = serial.Serial(port, baudRate, timeout=1)
    ser.stopbits = serial.STOPBITS_ONE            # Dois bits como final de cada byte (representou uma melhor comportamento)
    ser.bytesize = 8                              # Tamanho do byte   
    ser.parity = serial.PARITY_NONE               # Não há verificação de paridade
    
    print ("Serial port opened " + port + " over Baudrate " + str(baudRate))
    
    return ser
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
port=['/dev/ttyS0']
baudRate=9600

ser=intConfig(port[0], baudRate)

# READING SENSORS

try:
    while True:
        # Sensor 1
        d1a=spi1.xfer([0b00010000, 0x0, 0x0])        # Sending 2 additional bytes (0x0) in order to have enough time to receave 11 bits from the sensor
        d1b=spi1.xfer([0b00010001, 0x0, 0x0])        # Try xfer2!!!
        x1=( d1a[1] << 8 ) + d1a[2] >> 5                                           # 11 bits in 2 bytes size mensage
        y1=( d1b[1] << 8 ) + d1b[2] >> 5
        a1=(x1-y1)/6554.0

        # Sensor 2
        d2a=spi2.xfer([0b00010000, 0x0, 0x0])
        d2b=spi2.xfer([0b00010001, 0x0, 0x0])
        x2=( d2a[1] << 8 ) + d2a[2] >> 5
        y2=( d2b[1] << 8 ) + d2b[2] >> 5
        a2=(x2-y2)/6554.0

   
        s1=np.rad2deg(np.arcsin(a1))
        s2=np.rad2deg(np.arcsin(a2))
        print("SENSOR 1 \t         SENSOR 2")
        print(s1,"° \t",s2,"°")
        
        data1=struct.pack('d',s1)
        data2=struct.pack('d',s2)
        data=[data1,data2]
        ser.write('<<'.encode())
        ser.write(data1)
        ser.write(data2)
        
        time.sleep(1)
except KeyboardInterrupt:
    spi1.close()
    spi2.close()