import socket
import threading
import os
import time
from pathlib import Path
import base64

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2007
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response
HILOS = []
parte1 = list()
parte2 = list()
parte3 = list()
FileParts = 0
bytesToSend = None

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))


def NeedPart(direccion, parte):
    tcpNeedPart = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpNeedPart.connect(direccion)
    bytesToSend = (parte).encode('utf-8')
    tcpNeedPart.send(bytesToSend)
    tcpNeedPart.close()


def CrearDoc(data, path_archivo):
    try:
        open(path_archivo, "w").close()
    except:
        print("An error occurred")
    else:
        print("File created successfully")

    with open(path_archivo, 'ab') as file:
        for line in data:
            file.write(line)


def client_newDoc(ip, port, conexxion, carpeta_path):
    print(f'[+] New server socket thread started for  {ip}  : {str(port)}')
    paquetes_recividos = 0
    nombre_archivo = ''
    data_doc = list()
    if conexxion:
        while True:
            data = conexxion.recv(206)

            if 'PARTE1F1IN$$-/' in data.decode("UTF-8", 'ignore'):
                print(f'SE TERMINO DE RECIBIR PARTE 1 DEL ARCHIVO')
                break

            elif 'PARTE2F1IN$$-/' in data.decode("UTF-8", 'ignore'):
                print(f'SE TERMINO DE RECIBIR PARTE 2 DEL ARCHIVO')
                break

            elif 'PARTE3F1IN$$-/' in data.decode("UTF-8", 'ignore'):
                print(f'SE TERMINO DE RECIBIR PARTE 3 DEL ARCHIVO')
                break

            elif 'PARTE1' in data.decode('UTF-8', 'ignore')[:6]:
                parte1.append(data.decode('UTF-8', 'ignore')[6:len(data.decode("UTF-8", 'ignore'))])

            elif 'PARTE2' in data.decode('UTF-8', 'ignore')[:6]:
                parte2.append(data.decode('UTF-8', 'ignore')[6:len(data.decode("UTF-8", 'ignore'))])

            elif 'PARTE3' in data.decode('UTF-8', 'ignore')[:6]:
                parte3.append(data.decode('UTF-8', 'ignore')[6:len(data.decode("UTF-8", 'ignore'))])

            elif 'nombre:' in data.decode("UTF-8", 'ignore'):
                paquetes_recividos += 1
                nombre_archivo = data.decode("UTF-8", 'ignore')[7:len(data.decode("UTF-8", 'ignore'))]
                archivo_path = carpeta_path + '\\' + str(nombre_archivo)
    conexxion.close()
    return


# ---------------------------------------------------------------------------------------------------------
for x in range(1, 4):
    tcpServer.listen()
    parte = 'PARTE' + x + ''
    port = 2000 + x
    print(f'Waiting for the parts of the File')
    (conexion, (ip, port)) = tcpServer.accept()
    print(f'Conexion succesfull {conexion}')
    NeedPart((socket.gethostname(), port), parte)
    newthread = threading.Thread(target=client_newDoc, args=(ip, port, conexion))
    newthread.start()
    newthread.join()

if parte1 and parte2 and parte3:
    print('SIuuuuuuuuu')