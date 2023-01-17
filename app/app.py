from flask import Flask,render_template,request,send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import socket
import time
import subprocess
import socket
import threading


app=Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
@app.route('/download')
def download_file(nombre):
    print(f'AAAAAAAAAAAA:  {nombre}')

@app.route('/', methods=['GET',"POST"])
def home():
        
    # Funcion para pedir parte del archivo a linux 1 y 3
    names=list()
    data= dict()
    
    with open('namelis.txt','a') as namelist: #Create the list names file
        print('Open file')

    with open('namelis.txt','r') as namelist: #Appendn the names into name list()
        for line in namelist.readlines():
            names.append(line)
    print(names)
#----------------------------------------------DESCARGA DE ARCHIVO---------------------------------------------------------------------------------------
    if request.method == 'POST':
        if request.form.get('action1'):
            fileNamexx=request.form.get('action1')
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
                port = 2000 + (x+1)
                print(f'Waiting for the parts of the File')
                newthread = threading.Thread(target=client_newDoc, args=((socket.gethostname(), port),fileNamexx,parte)) #DIRECCION DE LINUX
                newthread.start()
                newthread.join()

            if parte1 and parte2 and parte3:
                print(parte1)
                print(parte2)
                print(parte3)
                NP=os.path.abspath(os.path.dirname(__file__))
                with open((NP+'\\new_'+fileNamexx),'wb') as newFile:
                    for p1 in parte1:
                        newFile.write(p1.encode('UTF-8'))
                    for p2 in parte2:
                        newFile.write(p2.encode('UTF-8'))
                    for p3 in parte3:
                        newFile.write(p3.encode('UTF-8'))
                NP=os.path.abspath(os.path.dirname(__file__))
                time.sleep(1)
                NewArch=NP+"\\new_"+fileNamexx
                print(f'QUE ESSSSSSSSSS: {NewArch}')
                return send_file(NewArch,as_attachment=True)



            

#_----------------------------------------------------------------------------------------------------------------------------------------
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        nombre=file.filename    
        newname=nombre.replace(" ", "_")
        print(newname)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file

        with open('namelis.txt','a') as namelist: #Then open the lis names file
            namelist.write(newname+'\n')

        time.sleep(1)
        host = socket.gethostname()
        print(host)
        port = 2002
        BUFFER_SIZE = 2000
        bytesToSend=None
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect((host, port))
        F=os.path.abspath(os.path.dirname(__file__))
        archvio=F+'\\static\\files\\'+newname
        paquetes_enviados = 0

        with open(archvio, 'rb') as file:
            bytesToSend = ('nombre:' + str(newname) + '').encode('UTF-8')
            print(bytesToSend)
            tcpClientA.send(bytesToSend)
            time.sleep(1)
            bytesToSend=None
            while piece := file.read(200):
                bytesToSend=None
                bytesToSend = piece
                tcpClientA.send(bytesToSend)
                bytesToSend = None
                paquetes_enviados += 1        
        bytesToSend = 'FIN DEL ENVIO'.encode("UTF-8")
        tcpClientA.send(bytesToSend)
        tcpClientA.close()
        return "File has been uploaded."
    
    namesset=set(names)
    data={
        'namex':namesset,
    }
    return render_template('index.html', form=form,data=data)

if __name__ == '__main__':
    app.run(debug=True)