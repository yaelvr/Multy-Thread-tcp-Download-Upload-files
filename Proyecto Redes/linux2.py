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
bytesToSend = None

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))


def EnviarPartArchivo(direccion_servidor, path_archvio, nombre_archivo):
    # host = socket.gethostname()
    # port = 2004
    tcpClientDocLoader = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcpClientA.connect((host, port))
    tcpClientDocLoader.connect((direccion_servidor))
    # --------------------------------------------------------------------
    try:
        # Determinar el largo del archivo y dividirlo en 3 partes enteras
        with open(path_archvio, 'rb') as filex:
            size_reduce = len(filex.read()) // 3
        with open(path_archvio, 'rb') as file:
            bytesToSend = ('nombre:' + str(nombre_archivo) + '').encode('UTF-8')
            tcpClientDocLoader.send(bytesToSend)
            time.sleep(.5)
            bytesToSend = ('PARTE2').encode('UTF-8')
            tcpClientDocLoader.send(bytesToSend)
            time.sleep(.5)
            parte_1 = file.read(size_reduce)
            parte_2 = file.read(size_reduce)
            parte_3 = file.read()
            # Envia la parte 1 del archivo
            tcpClientDocLoader.send(parte_1)
            bytesToSend = 'FIN DEL ENVIO'.encode("UTF-8")
        tcpClientDocLoader.send(bytesToSend)
    except FileNotFoundError:
        print(f'Ese archivo no existe en el directorio actual {path_archvio}')

        # --------------------------------------------------------------------
    tcpClientDocLoader.close()
    print('Funcion enviar archivo close')


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
            data = conexxion.recv(200)
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
    linux1.join()
    linux3.join()
    conexxion.close()
    return


# ----------------- CREACION DE LA CARPETA QUE GUARDA LOS ARCHIVOS----------------------------

carpeta = 'Lista_Archivos'
carpeta_path = os.path.join(str(Path(__file__).parent), carpeta)
print(carpeta_path)
if os.path.exists(carpeta):
    print("Carpeta Lista_Archivos existente")
else:
    try:
        os.mkdir(carpeta)
    except OSError:
        print("La creación del directorio %s falló" % carpeta)
    else:
        print("Se ha creado el directorio: %s " % carpeta)
# ---------------------------------------------------------------------------------------------------------
while True:
    tcpServer.listen()
    print(f'Multithreaded Python server : Waiting for connections from TCP clients...')
    (conexion, (ip, port)) = tcpServer.accept()
    print(f'conexion {conexion}')
    newthread = threading.Thread(target=client_newDoc, args=(ip, port, conexion, carpeta_path))
    newthread.start()
    newthread.join()
