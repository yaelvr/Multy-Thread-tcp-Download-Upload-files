import socket
import threading
import os
import time
from pathlib import Path
import base64

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2002
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response
HILOS = []
parte1=list()
parte2=list()
parte3=list()
FileParts=0
bytesToSend = None

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))

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


def EnviarArchivo(direccion_linux, archvio, nombre,maquina):
    host = socket.gethostname()
    BUFFER_SIZE = 2000
    port = 2001
    tcpClientLinux2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcpClientLinux2.connect((host, port))
    tcpClientLinux2.connect(direccion_linux)
    # --------------------------------------------------------------------
    try:
        paquetes_enviados = 0
        bytesToSend = ('nombre:' + str(nombre) + '').encode('UTF-8')
        tcpClientLinux2.send(bytesToSend)
        with open(archvio, 'rb') as file:
            bytesToSend = None
            while piece := file.read(150):
                bytesToSend = None
                bytesToSend = piece
                tcpClientLinux2.send(bytesToSend)
                bytesToSend = None
                paquetes_enviados += 1
                # print(f'Largo del paquete; {len(piece)} paquete: {piece}')
                # print(f'Paquetes enviados: {paquetes_enviados}')
        bytesToSend = 'FIN DEL ENVIO'.encode("UTF-8")
        tcpClientLinux2.send(bytesToSend)
        tcpClientLinux2.close()

    except FileNotFoundError:
        print(f'Ese archivo no existe en el directorio actual  {archvio}')
        pass
    tcpClientLinux2.close()
    print(f'ENVIO DEL ARCHIVO {nombre} A {maquina} TERMINADO')
    return


def client_newDoc(ip, port, conexxion, carpeta_path):
    print(f'[+] New server socket thread started for  {ip}  : {str(port)}')
    paquetes_recividos = 0
    nombre_archivo = ''
    data_doc = list()
    if conexxion:
        while True:
            data = conexxion.recv(206)
            # print(data)
            # print(f'DATA: {data.decode("UTF-8")}')
            if 'FIN DEL ENVIO' in data.decode("UTF-8", 'ignore'):
                CrearDoc(data_doc, archivo_path)
                paquetes_recividos += 1
                print(f'RECIBO DEL ARCHIVO: {nombre_archivo} COMPLETADO')
                time.sleep(5)
                linux1 = threading.Thread(target=EnviarArchivo, args=((socket.gethostname(), 2001), archivo_path, nombre_archivo,'Linux 1'))
                linux3 = threading.Thread(target=EnviarArchivo, args=((socket.gethostname(), 2003), archivo_path, nombre_archivo, 'Linux 3'))
                linux1.start()
                linux3.start()
                break
            elif 'ENVIAR PARTE' in data.decode("UTF-8", 'ignore'):
                paquetes_recividos += 1
                pass
                # enviarParte= threading.Thread(target=EnviarPartArchivo, args=(direccion_servidor,archivo_path,nombre_archivo))
                # enviarParte.start()
                # HILOS.append(enviarParte)

            elif 'PARTE1' in data.decode('UTF-8','ignore'):
                parte1.append(data.decode('UTF-8','ignore')[6:len(data.decode("UTF-8", 'ignore'))])

            elif 'PARTE2' in data.decode('UTF-8','ignore'):
                parte2.append(data.decode('UTF-8','ignore')[6:len(data.decode("UTF-8", 'ignore'))])

            elif 'PARTE3' in data.decode('UTF-8', 'ignore'):
                parte3.append(data.decode('UTF-8', 'ignore')[6:len(data.decode("UTF-8", 'ignore'))])

            elif 'nombre:' in data.decode("UTF-8", 'ignore'):
                paquetes_recividos += 1
                nombre_archivo = data.decode("UTF-8", 'ignore')[7:len(data.decode("UTF-8", 'ignore'))]
                archivo_path = carpeta_path + '\\' + str(nombre_archivo)

    linux1.join()
    linux3.join()
    conexxion.close()
    return

# ---------------------------------------------------------------------------------------------------------
while True:
    tcpServer.listen()
    print(f'Waiting for the parts of the File')
    (conexion, (ip, port)) = tcpServer.accept()
    print(f'Conexion succesfull {conexion}')
    newthread = threading.Thread(target=client_newDoc, args=(ip, port, conexion))
    newthread.start()
    newthread.join()
