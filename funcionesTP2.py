#########################################################################
#Elaborado por Mónica Alfaro Parrales y Jennifer Alvarado Brenes
#Inicio 27/06/2020 02:30 pm
#Última modificación 19/07/2020 12:10 am
#Versión 3.8.2
#########################################################################

#Importación de librerías:

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib
import socket
#########################################################################

def enviarCorreo(correo):
    """
    Funcionalidad: Enviar un correo si hay internet.
    Entradas: El correo.
    Salidas: El correo enviado si hay internet, sino hay, entonces envía un mensaje de error.
    """
    try:
        #Crear el objeto de mensaje:
        msg = MIMEMultipart()
         
        message = "Te estás haciendo viejo(a)."
        body = MIMEText('<p><img src="https://felizcumpleanos.date/wp-content/uploads/2019/06/happy-birthday-3416524_1280-1024x521.png" /></p>', _subtype='html')

        #Generar los parámetros del correo por enviar:
        password = "tareaProgramada15"
        msg['From'] = "enviarcorreosausuario@gmail.com"
        msg['To'] = correo
        msg['Subject'] = "¡Feliz cumpleaños!"
         
        #Agregar el mensaje y la imagen:
        msg.attach(MIMEText(message, 'plain',_charset="utf-8"))
        msg.attach(body)
         
        #Crear el servidor:
        server = smtplib.SMTP('smtp.gmail.com: 587')
         
        server.starttls()
        socket.gethostbyname('google.com')
        c = socket.create_connection(('google.com', 80), 1)
        c.close()
        #Credenciales del login para enviar el correo:
        server.login(msg['From'], password)
     
        #Enviar el correo mediante el servidor:
        server.sendmail(msg['From'], msg['To'], msg.as_string())
     
        server.quit()
        mensajeCorrecto="Correo exitosamente enviado a: \n %s" % (msg['To'])
     
    except socket.gaierror:
        mensajeCorrecto="Correo no enviado: \n Error de DNS (internet)."

    except socket.error:
        mensajeCorrecto="Correo no enviado: \n Error de conexión a internet."

    except:
        mensajeCorrecto="Correo no enviado: \n Error de conexión a internet."
        
    return mensajeCorrecto
