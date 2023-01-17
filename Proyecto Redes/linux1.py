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

def EnviarPartArchivo(conexion, path_archvio, nombre_archivo):
    print('Enviar parte del archivo')
    # --------------------------------------------------------------------
    try:
        # Determinar el largo del archivo y dividirlo en 3 partes enteras
        with open(path_archvio, 'rb') as filex:
            size_reduce = len(filex.read()) // 3
        with open(path_archvio, 'rb') as file:
            bytesToSend= ('$$Buffer-Size$$:').encode('UTF-8')+(str(size_reduce)).encode('UTF-8')
            conexion.send(bytesToSend)
            bytesToSend=None
            parte_1 = file.read(size_reduce)
            print(parte_1)
            bytesToSend=('PARTE1$').encode('UTF-8')+parte_1
            conexion.send(bytesToSend)
            bytesToSend=('$$TERMINO $$ENVIO PARTE').encode('UTF-8')
            conexion.send(bytesToSend)


    except FileNotFoundError:
        print(f'Ese archivo no existe en el directorio actual {path_archvio}')
        return False
    print('Funcion enviar partes del  archivo "CLOSE"')
    return True


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
            elif '3Nv1AR$PART31' in data.decode("UTF-8", 'ignore'):
                print('Siuuuu')
                direccion_servidor = (socket.gethostname(), 2007)
                nombre = data.decode("UTF-8", 'ignore')[13:len(data.decode("UTF-8", 'ignore'))]
                archivo_pathX = carpeta_path + '\\' + str(nombre)
                paquetes_recividos += 1
                PART = EnviarPartArchivo(conexxion, archivo_pathX, nombre)
                if PART:
                    conexxion.close()
                    break
                else:
                    print('NO SE PUDO ABRIR EL ARCHIVO')
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
