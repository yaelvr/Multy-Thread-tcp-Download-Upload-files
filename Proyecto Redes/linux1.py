import socket
import threading
import os
import time
from pathlib import Path
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2001
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response
HILOS=[]
direccion_servidor=[]

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))

def EnviarPartArchivo(direccion_servidor,path_archvio,nombre_archivo):
    #host = socket.gethostname()
    #port = 2004
    tcpClientDocLoader = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #tcpClientA.connect((host, port))
    tcpClientDocLoader.connect((direccion_servidor))
    # --------------------------------------------------------------------
    try:
        # Determinar el largo del archivo y dividirlo en 3 partes enteras
        with open(path_archvio, 'rb') as filex:
            size_reduce=len(filex.read())//3
        with open(path_archvio, 'rb') as file:
            bytesToSend = ('nombre:' + str(nombre_archivo) + '').encode('UTF-8')
            tcpClientDocLoader.send(bytesToSend)
            time.sleep(.5)
            bytesToSend = ('PARTE1').encode('UTF-8')
            tcpClientDocLoader.send(bytesToSend)
            time.sleep(.5)
            parte_1 = file.read(size_reduce)
            parte_2 = file.read(size_reduce)
            parte_3 = file.read()
            #Envia la parte 1 del archivo
            tcpClientDocLoader.send(parte_1)
            bytesToSend = 'FIN DEL ENVIO'.encode("UTF-8")
        tcpClientDocLoader.send(bytesToSend)
    except FileNotFoundError:
        print('Ese archivo no existe en el directorio actual')
        pass
            # --------------------------------------------------------------------
    tcpClientDocLoader.close()
    return None


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
            data = conexxion.recv(200)
            if 'FIN DEL ENVIO' in data.decode("UTF-8", 'ignore'):
                CrearDoc(data_doc, archivo_path)
                paquetes_recividos += 1
                break
            elif 'ENVIAR PARTE' in data.decode("UTF-8", 'ignore'):
                paquetes_recividos += 1
                pass
                # enviarParte= threading.Thread(target=EnviarPartArchivo, args=(direccion_servidor,archivo_path,nombre_archivo))
                # enviarParte.start()
                # HILOS.append(enviarParte)

            elif 'nombre:' in data.decode("UTF-8", 'ignore'):
                paquetes_recividos += 1
                nombre_archivo = data.decode("UTF-8", 'ignore')[7:len(data.decode("UTF-8", 'ignore'))]
                archivo_path = carpeta_path + '\\' + str(nombre_archivo)
            else:
                data_doc.append(data)
                # print(f'Server received data: {data} ')
                paquetes_recividos += 1
                # print(paquetes_recividos)
        # print(f'Paquetes Recividos: {paquetes_recividos}')
    conexxion.close()
    return
#----------------- CREACION DE LA CARPETA QUE GUARDA LOS ARCHIVOS----------------------------

carpeta = 'Lista_Archivos_linux1'
carpeta_path = os.path.join(str(Path(__file__).parent), carpeta)

if os.path.exists(carpeta):
    print("Carpeta Lista_Archivos existente")
else:
    try:
        os.mkdir(carpeta)
    except OSError:
        print("La creación del directorio %s falló" % carpeta_path)
    else:
        print("Se ha creado el directorio: %s " % carpeta)
#---------------------------------------------------------------------------------------------------------

while True:
    tcpServer.listen()
    print(f'Multithreaded Python server : Waiting for connections from TCP clients...')
    (conexion, (ip, port)) = tcpServer.accept()
    print(f'conexion {conexion}')
    newthread = threading.Thread(target=client_newDoc, args=(ip, port, conexion,carpeta_path))
    newthread.start()
    newthread.join()
