import socket
import threading
import re
import os
import time
from pathlib import Path
import base64

#Multithreaded Python server : TCP Server Socket Program Stub

parte1 = list()
parte2 = list()
parte3 = list()
FileParts = 0
bytesToSend = None
def client_newDoc(conexxion, nombre,parte):
    bufferSize=200
    bytesToSend = None
    tcpPart = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpPart.connect(conexxion)
# --------------------------------------------------------------------
    paquetes_enviados = 0
    bytesToSend=parte.encode('UTF-8')+nombre.encode('UTF-8')
    tcpPart.send(bytesToSend)
    bytesToSend=None
    while True:
        data = tcpPart.recv(bufferSize+7)
        if '$$TERMINO $$ENVIO PARTE' in data.decode('UTF-8','ignore'):
            break
        elif 'PARTE1$' in data.decode('UTF-8','ignore')[:7]:
            parte1.append(data.decode('UTF-8','ignore')[7:len(data.decode('UTF-8','ignore'))])
            #print(data.decode('UTF-8','ignore')[7:len(data.decode('UTF-8','ignore'))])
        elif 'PARTE2$' in data.decode('UTF-8','ignore')[:7]:
            parte2.append(data.decode('UTF-8','ignore')[7:len(data.decode('UTF-8','ignore'))])
            #print(data.decode('UTF-8', 'ignore')[7:len(data.decode('UTF-8', 'ignore'))])
        elif 'PARTE3$' in data.decode('UTF-8','ignore')[:7]:
            parte3.append(data.decode('UTF-8','ignore')[7:len(data.decode('UTF-8','ignore'))])
            #print(data.decode('UTF-8', 'ignore')[7:len(data.decode('UTF-8', 'ignore'))])
        elif '$$Buffer-Size$$:' in data.decode("UTF-8", 'ignore'):
            bufferSize = int(data.decode("UTF-8", 'ignore')[16:])
    tcpPart.close()
#---------------------------------------------------------------------------------------------------------
direclist=[(socket.gethostname(),2001),(socket.gethostname(),2002),(socket.gethostname(),2003)]
for x in range(0, 3):
    parte = '3Nv1AR$PART3' + str(x+1) + ''
    fileName='reyes_magos_2.png'
    port = 2000 + (x+1)
    print(f'Waiting for the parts of the File')
    newthread = threading.Thread(target=client_newDoc, args=((socket.gethostname(), port),fileName,parte)) #DIRECCION DE LINUX
    newthread.start()
    newthread.join()

if parte1 and parte2 and parte3:
    print(parte1)
    print(parte2)
    print(parte3)
    with open(fileName,'wb') as newFile:
        for p1 in parte1:
            newFile.write(p1.encode('UTF-8'))
        for p2 in parte2:
            newFile.write(p2.encode('UTF-8'))
        for p3 in parte3:
            newFile.write(p3.encode('UTF-8'))
