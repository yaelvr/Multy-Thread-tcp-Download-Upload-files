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
Names_Lis=set()
bytesToSend = None

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))

def PedirFile(nombre,direccion):
    try:
        tcpPedir = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpPedir.connect((direccion))
        paquetes_enviados = 0
        bytesToSend = ('$$NED$$:'+str(nombre)).encode('UTF-8')
        tcpPedir.send(bytesToSend)
        data_doc=list()
        nombre_archivo=''
        bytesToSend = None
        while True:
            data = tcpPedir.recv(200)
            if 'FIN DEL ENVIO' in data.decode("UTF-8", 'ignore'):
                Names_Lis.add(nombre_archivo)
                NewDoc = threading.Thread(target=CrearDoc, args=(data_doc,archivo_path))
                NewDoc.start()
                NewDoc.join()
                CrearDoc(data_doc, archivo_path)
                print(f'RECIBO DEL ARCHIVO: {nombre_archivo} COMPLETADO')
                print(f'''
                            Nombre archivo:{nombre_archivo}
                            PATCHN ARCHIVO: {archivo_path}''')
                break
            elif 'nombre:' in data.decode("UTF-8", 'ignore'):
                nombre_archivo = data.decode("UTF-8", 'ignore')[7:len(data.decode("UTF-8", 'ignore'))]
                archivo_path = carpeta_path + '\\' + str(nombre_archivo)
            else:
                data_doc.append(data)
        tcpPedir.close()
        return True
    except ConnectionRefusedError:
        return False

def ChecarBorrados(Carpeta_Path):
    while True:
        FName = os.listdir(Carpeta_Path)
        FDir=list(Names_Lis)
        for file in FName:
            if file not in FDir:
                if PedirFile(file,(socket.gethostname(),2001)):
                    print('Archivo Adquirido')
                else:
                    PedirFile(file,(socket.gethostname(),2001))
                    print('Archivo Adquirido')
        time.sleep(5)


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
            parte_2 = file.read(size_reduce)
            parte_3 = file.read()
            print(parte_2)
            bytesToSend=('PARTE2$').encode('UTF-8')+parte_2
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
    return


def EnviarArchivo(direccion_linux, archvio, nombre,maquina):
    tcpClientLinux2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcpClientLinux2.connect((host, port))
    tcpClientLinux2.connect(direccion_linux)
    # --------------------------------------------------------------------
    try:
        paquetes_enviados = 0
        bytesToSend = ('nombre:' + str(nombre) + '').encode('UTF-8')
        tcpClientLinux2.send(bytesToSend)
        time.sleep(.5)
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
            if 'FIN DEL ENVIO' in data.decode("UTF-8", 'ignore'):
                Names_Lis.add(nombre_archivo)
                CrearDoc(data_doc, archivo_path)
                paquetes_recividos += 1
                print(f'RECIBO DEL ARCHIVO: {nombre_archivo} COMPLETADO')
                time.sleep(5)
                print(f'''
                    Nombre archivo:{nombre_archivo}
                    PATCHN ARCHIVO: {archivo_path}''')
                linux1 = threading.Thread(target=EnviarArchivo, args=((socket.gethostname(), 2001), archivo_path, nombre_archivo,'Linux 1'))
                linux3 = threading.Thread(target=EnviarArchivo, args=((socket.gethostname(), 2003), archivo_path, nombre_archivo, 'Linux 3'))
                linux1.start()
                linux3.start()
                linux1.join()
                linux3.join()
                break
            elif '3Nv1AR$PART32' in data.decode("UTF-8", 'ignore'):
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
Checar_Existencia = threading.Thread(target=ChecarBorrados, args=(carpeta_path))
Checar_Existencia.start()
Checar_Existencia.join()
# ---------------------------------------------------------------------------------------------------------
while True:
    tcpServer.listen()
    print(f'Multithreaded Python server : Waiting for connections from TCP clients...')
    (conexion, (ip, port)) = tcpServer.accept()
    print(f'conexion {conexion}')
    newthread = threading.Thread(target=client_newDoc, args=(ip, port, conexion, carpeta_path))
    newthread.start()
    newthread.join()
