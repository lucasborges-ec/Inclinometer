# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 14:04:21 2021

@author: Lucas Borges
"""

import serial
import struct
import time


#--------------------------------------------------------------------------
'''
Função utilizada para iniciar e configurar a comunicação serial
'''
def intConfig(port, baudRate):
    global ser                                       
    ser = serial.Serial(port, baudRate, timeout=1)
    ser.stopbits = serial.STOPBITS_ONE            # Dois bits como final de cada byte (representou uma melhor comportamento)
    ser.bytesize = 8                              # Tamanho do byte   
    ser.parity = serial.PARITY_NONE               # Não há verificação de paridade
    
    print ("Porta serial aberta " + port + " a um Baudrate de " + str(baudRate))
    
    return ser
#--------------------------------------------------------------------------

#Estabelecendo comunicação serial
print("Especifique a porta serial utilizada para comunicação (ex. COM10)")
port=input()
print("Especifique o baudrate utilizado para comunicação (ex. 9600)")
baudRate=input()


try:
    ser=intConfig(port, baudRate)
except:
    print("Error ao abrir a porta serial")
    
    
#Recebendo dados do Raspberry
startMarker = str('<').encode()
print("Deseja coletar leitura? [y,n]")
ans=input()
while (ans=="y"):
    ser.reset_input_buffer()           # Limpa o buffer de entrada da porta serial
    status=False
    while (status==False):
        if (ser.read()==startMarker and ser.read()==startMarker):
            a=ser.read(16)
            b=struct.unpack_from('d', a, offset=0)
            c=struct.unpack_from('d', a, offset=8)
            print("Sensor 1", b)
            print("Sensor 2", c)
            time.sleep(1)
            status=True
        else:
            print("Aguardando leitura consistente")
            time.sleep(1)
        
    print("Deseja coletar outra leitura? [y,n]")
    ans=input()

ser.reset_input_buffer()
ser.close()
time.sleep(0.2)
print("Porta serial fechada com sucesso")

time.sleep(1)
