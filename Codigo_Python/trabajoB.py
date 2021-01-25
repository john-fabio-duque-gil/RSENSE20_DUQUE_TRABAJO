# -*- coding: utf-8 -*-
"""
@author: JOHN FABIO DUQUE
"""

import matplotlib.pyplot as plt
import time
import socket


s = socket.socket()         
s.bind(('0.0.0.0', 8090 ))
s.listen(0)



def reads(content):
    read = content.decode().split('\t')
    return read


x = []
y = []
z = []

gx = []
gy = []
gz = []

modsAcc = []
modsGy = []


inicio_Acc = time.time()
inicio_Gy = time.time()

contador_caidas = 0 
print("Empiezo")



posible = False
Giroscopio = False



for i in range(10000):
    
    
    client, addr = s.accept()
    
    
    aux = client.recv(8)
    dato2 = client.recv(64)
    dato = reads(dato2)
    

    if len(dato)==6:
        
        d_x = float(dato[0]) + 1
        d_y = float(dato[1]) + 0.4
        d_z = float(dato[2]) - 0.7
        
        x.append(d_x)
        y.append(d_y)
        z.append(d_z)
        
        
        
        dato_gx = (float(dato[3]) + 22.1)
        dato_gy = (float(dato[4]) + 16.6)
        dato_gz = (float(dato[5]) + 11.4)
            
        
        gx.append(dato_gx)
        gy.append(dato_gy)
        gz.append(dato_gz)
        
        
        modAcc = (d_x*d_x + d_y*d_y + d_z*d_z)**(1/2)
        modAcc = (modAcc / 9.8) 
        modGy = (dato_gx*dato_gx + dato_gy*dato_gy + dato_gz*dato_gz)**(1/2)
        
        
        modsGy.append(modGy)
        modsAcc.append(modAcc)
        
        
        
        if(modAcc < 0.35):
            inicio_Acc = time.time()
            posible = True
        
        
        if (time.time()>inicio_Acc + 0.5):
            posible = False
            
        
        if(modGy > 240):
            inicio_Gy = time.time()
            Giroscopio = True
        
        
        if (time.time()>inicio_Gy + 0.5):
            Giroscopio = False
        
        if posible and modAcc> 2 and Giroscopio:
            print("Me he caido")
            posible = False
            Giroscopio = False
            contador_caidas = contador_caidas + 1
            time.sleep(3)
            print("----------------")


print(contador_caidas)

plt.figure()
plt.plot(gx, 'g')
plt.plot(gy, 'r')
plt.plot(gz, 'b')
plt.show()


plt.figure()
plt.plot(x, 'g')
plt.plot(y, 'r')
plt.plot(z, 'b')
plt.show()


plt.figure()
plt.title("Acelerómetro")
plt.plot(modsAcc)
plt.show()

plt.figure()
plt.title("Giróscopo")
plt.plot(modsGy)
plt.show()


