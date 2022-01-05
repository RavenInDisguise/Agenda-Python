#########################################################################
#Elaborado por Mónica Alfaro Parrales y Jennifer Alvarado Brenes
#Inicio 27/06/2020 02:30 pm
#Última modificación 19/07/2020 12:10 am
#Versión 3.8.2
#########################################################################

#Importación de librerías:

import re
from tkinter import messagebox

#########################################################################

def validarExistente(nombre,lista):
    """
    Funcionalidad: Validar si el nombre ingresado ya existe en la liosta de amigos.
    Entradas: EL nombre y la lista.
    Salidas: False (sí existe) o True (no existe).
    """
    nombre=nombre.split(",")
    if lista==[]:
        return True
    else:
        for persona in lista:
            nombre2=persona[0]
            if (nombre2[0]==nombre[0])and(nombre2[1]==nombre[1])and(nombre2[2]==nombre[2]):
                return False
        return True

#########################################################################
    
def validarTelefono(telefono):
    """
    Funcionalidad: Validar que el teléfono tenga un largo de 8 dígitos.
    Entradas: El número de teléfono.
    Salidas: True (es correcto) o False (es incorrecto).
    """
    if re.match(r'(\d{8})$',telefono):
        return True
    else:
        return False
def validarCorreo(correo):
    """
    Funcionalidad: Validar que el formato del correo sea correcto.
    Entradas: El correo.
    Salidas: True (es correcto) o False (es incorrecto).
    """
    if re.match(r'(^[\w_.-]+)@([\w]+)([\w]+).([\w]+)$',correo): #dejar así
        return True
    else:
        return False

#########################################################################
    
def validarNombre(nombre):
    """
    Funcionalidad: Validar que el formato del nombre sea correcto.
    Entradas: El nombre.
    Salidas: True (es correcto) o False (es incorrecto).
    """
    if re.match(r'(^[\w]+),([\w]+),([\w]+)$',nombre):
        for caracter in nombre:
            if caracter in '0123456789_-.#$%&/()=?¡![]¿@"¨*{};:' or caracter=="'":
                return False
        return True
    else:
        return False

#########################################################################
    
def validarFecha(fecha):
    """
    Funcionalidad: Validar que el formato de la fecha sea correcto.
    Entradas: La fecha.
    Salidas: True (es correcto) o False (es incorrecto).
    """
    if re.match(r'(\d{2})/(\d{2})/(\d{4})$',fecha):
        fecha=fecha.split("/")
        dia=int(fecha[0])
        mes=int(fecha[1])
        anno=int(fecha[2])
        if ((dia not in range(1,32))or(mes not in range(1,13)))or(dia>29 and mes==2):
            return False
        else:
            return True
    else:
        return False
    
#########################################################################
    
def validarString(datos,lista):
    """
    Funcionalidad: Validar que el formato del string sea correcto.
    Entradas: El string de los datos de una sola persona.
    Salidas: True (es correcto) o False (es incorrecto).
    """
    if re.match(r'([\w,]+)°([\w/]+)°([\w@.]+)°([\d]+)$',datos):
        datos=datos.split("°")
        if validarNombre(datos[0]):
            if validarFecha(datos[1]):
                if validarCorreo(datos[2]):
                    if validarTelefono(datos[3]):
                        if validarExistente(datos[0],lista):
                            return True
                        else:
                            nombre=datos[0].split(",")
                            messagebox.showinfo(message="La persona con el nombre "+nombre[0]+" "+nombre[1]+" "+nombre[2]+" ya se encuentra registrada.", title="Error")
                            return False
                    else:
                        messagebox.showinfo(message="Formato de número de teléfono incorrecto en "+datos[3], title="Error")
                        return False
                else:
                    messagebox.showinfo(message="Formato de correo incorrecto en "+datos[2], title="Error")
                    return False
            else:
                messagebox.showinfo(message="Formato de fecha incorrecto en "+datos[1], title="Error")
                return False
        else:
            messagebox.showinfo(message="Formato de nombre incorrecto en "+datos[0], title="Error")
            return False
    else:
        messagebox.showinfo(message="Formato de datos incorrecto.", title="Error")
        return False

#########################################################################
    
def validarCantidad(string,lista):
    """
    Funcionalidad: Valida si son los datos de una o más personas.
    Entradas: El string ingresado por el usuario.
    Salidas: True (es correcto) o False (es incorrecto).
    """
    if "|" in string:
        string=string.split("|")
        for persona in string:
            if validarString(persona,lista)==False:
                return False
        return True
    else:
        if validarString(string,lista):
            return True
        else:
            return False
