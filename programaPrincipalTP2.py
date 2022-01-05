#########################################################################
#Elaborado por Mónica Alfaro Parrales y Jennifer Alvarado Brenes
#Inicio 27/06/2020 02:30 pm
#Última modificación 19/07/2020 12:10 am
#Versión 3.8.2
#########################################################################

#Importación de librerías:

from tkinter import*
from tkinter import messagebox
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import filedialog
from tkinter import ttk
import pickle
import webbrowser
import re
from datetime import date
from datetime import datetime
from funcionesTP2 import *
from validacionesTP2 import*

##########################################################################################

#Variables globales

diaHoy = date.today()
fechaTotal = datetime.now()
global calendario
calendario=[[["Enero"],],
            [["Febrero"],],
            [["Marzo"],],
            [["Abril"],],
            [["Mayo"],],
            [["Junio"],],
            [["Julio"],],
            [["Agosto"],],
            [["Setiembre"],],
            [["Octubre"],],
            [["Noviembre"],],
            [["Diciembre"],]]
global lista
lista=[]
global matriz
matriz=[]

##########################################################################################

#Funciones del programa principal

def cerrarPrograma():
    amigos=open("amigos.txt","r")
    pickle.dump("",amigos)
    amigos.close()
    ventana.destroy()

##########################################################################################
    
def crearHTML():
    """
    Funcionalidad: Crea el HTML con los datos de las matrices.
    Entradas: Ninguna.
    Salidas: El HTML creado.
    """
    registro=open("amigos.txt","r")
    amigos=registro.readlines()
    amigos=amigos[0].split("|")
    fechaTotal = datetime.now()
    fechaTotal=str(fechaTotal)
    annoActual=fechaTotal[:4]
    mesActual=fechaTotal[5:7]
    diaActual=fechaTotal[8:10]
    horaActual=fechaTotal[11:13]
    minActual=fechaTotal[14:16]
    segActual=fechaTotal[17:19]
    nombreArchivo='cumpleañeros-'+diaActual+'-'+mesActual+'-'+annoActual+'-'+horaActual+'-'+minActual+'-'+segActual+'.html'
    f = open(nombreArchivo,'w')
    mensaje = """<html lang="es">
    <head>
    <title>Agenda de amigos</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1' >
    <link rel="stylesheet" href="estilos.css"/>
    </head>
    <style type="text/css">
    table, th, td {border: 1px solid black;border-collapse: collapse;;}
    </style>
    <body>
    <table style="width: 100%">
    <tr bgcolor="#FF83DA">
    <th colspan="5"><h1><span style="background: white;">Cumpleañeros</span></h1></th>
    </tr>
    <tr>
    <th><h3>Fecha</h3></th>
    <th><h3>Nombre</h3></th>
    <th><h3>Apellidos</h3></th>
    <th><h3>Teléfono</h3></th>
    <th><h3>Correo</h3></th>
    </tr>"""
    for mes in calendario:
        nomMes=(str(mes[0])).strip("['']")
        mensaje+="""<tr bgcolor="#FF83DA">
        <th colspan="5" align="left"><h3><span style="background: white;">"""+nomMes+"""</span></h3></th>'
        </tr>"""
        if len(mes)>1:
            for persona in mes:
                if persona==mes[0]:
                    continue
                else:
                    nombreCom=persona[0]
                    nombre=nombreCom[0]
                    apellidos=nombreCom[1]+" "+nombreCom[2]
                    fecha=persona[1]
                    dia=fecha[:2]
                    correo=persona[2]
                    tel=persona[3]
                    mensaje+="""
                    <tr>
		    <td align="center">"""+dia+"""</td>
		    <td align="center">"""+nombre+"""</td>
		    <td align="center">"""+apellidos+"""</td>
		    <td align="center">"""+tel+"""</td>
		    <td align="left">"""+correo+"""</td>
                    </tr>"""
        else:
            mensaje+="""<tr>
            <td colspan="5">No hay cumpleañeros registrados en este mes.</td>
            </tr>"""
    mensaje+="""</table>"""
    for persona in amigos:
        mensaje+="""<p>"""+persona+"""</p>"""
    mensaje+="</body></html>"  
    f.write(mensaje)
    f.close()
    webbrowser.open_new_tab(nombreArchivo)
    
##########################################################################################
    
#Funciones de cumpleañero del día (envío del correo)

def abrirHoy():
    def selec():
        """
        Funcionalidad: Selecciona una persona del radio button.
        Entradas: Ninguna.
        Salidas:  Persona seleccionada.
        """
        cumpleanero=opcion.get()
        if(cumpleanero=="None"):
            valor.config(text = " Cumpleañero del día seleccionado: \n{} ".format(" Ninguno."))
            botonCumpleanero.config(state="disable")
            
        else:
            valor.config(text = " Cumpleañero del día seleccionado: \n{} ".format(opcion.get()))
            botonCumpleanero.config(state="active")
            return cumpleanero
        
    def seleccionarUsuario():
        """
        Funcionalidad: Seleccionar el nombre y correo de la persona para así enviar un correo.
        Entradas: Ninguno.
        Salidas: El correo enviado.
        """
        cumpleanero=selec()
        for valores in lista:
            nombres=valores[0]
            nombre=nombres[0]
            apellido1=nombres[1]
            apellido2=nombres[2]
            correo=valores[2]
            cumpleanero2=str(cumpleanero)
            cumpleanero2=cumpleanero2.split(" ")
            if(str(cumpleanero2[0])==nombre and str(cumpleanero2[1])==apellido1 and str(cumpleanero2[2])==apellido2):
                mensaje=enviarCorreo(correo)
                valor2.config(text = "\n"+mensaje+"\n",bg="white")       

    def generarCumpleDia(matriz,opcion,ventana2):
        """
        Funcionalidad: Genera un radio button con la información de personas que cumplan el día de hoy.
        Entradas: La matriz (matriz), la opcion del radiobutton(opcion), la ventana(ventana2).
        Salidas: El contador de personas con el cumpleaños el día de hoy.
        """
        contador=0
        for valores in matriz:
            salida=retornarMesDia(valores)
            dia=salida[0]
            mes=salida[1]
            nombre=salida[2]
            if (dia==diaHoy.day and mes==diaHoy.month):
                contador+=1
                if(contador<=5):
                    Radiobutton(ventana2, text=nombre[0]+" "+nombre[1]+" "+nombre[2], variable=opcion,
                    value=nombre,command=selec, bg="white",selectcolor="white").pack(anchor=W)
        if(contador==0):
            labelNoCumple= Label(ventana2, text="¡No hay cumpleañeros el día de hoy!",bg="white")
            labelNoCumple.pack()
            return contador
        
    #Programa principal de la ventana cumpleañeros del día

    ventana2=tk.Toplevel(ventana)
    ventana2.title("Cumpleaños")
    ventana2.geometry("250x280")
    ventana2.configure(background="white")
    ventana2.resizable(False, False)
    window_height = 290
    window_width = 280
    screen_width = ventana2.winfo_screenwidth()
    screen_height = ventana2.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    ventana2.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    labelHoyCumple= Label(ventana2, text="Hoy Cumple",bg="white")
    labelHoyCumple.pack()
    valor = Label(ventana2,bg="white")
    valor.pack()
    opcion = StringVar()
    opcion.set(None)
    contador=generarCumpleDia(datosUsuario,opcion,ventana2)
    valor2 = Label(ventana2,bg="white")
    valor2.pack()
    botonCumpleanero=Button(ventana2, text="Enviar correo",command=seleccionarUsuario,bg="white",state="active")
    botonCumpleanero.pack()
    if(contador==0):
        botonCumpleanero.config(state="disable")
    blank= Label(ventana2,bg="white")
    blank.pack()
    mainloop()

##########################################################################################
    
def retornarMesDia(matrizPeq):
    """
    Funcionalidad: Retorna el mes y el día de la matriz.
    Entradas: La matriz (matrizPeq).
    Salidas: El día, mes, nombre y correo de la matriz. 
    """
    nombre=matrizPeq[0]
    fecha=matrizPeq[1]
    correo=matrizPeq[2]
    dia1=int(fecha[0]+fecha[1])
    mes1=int(fecha[3]+fecha[4])
    return dia1,mes1,nombre,correo

##########################################################################################

def evaluarNombres(nombre1,nombre2):
    """
    Funcionalidad: Evalúa si las personas tienen el mismo nombre y/o primer apellido. 
    Entradas: Dos nombres completos str(nombre1), str(nombre2).
    Salidas: Primer apellido en caso de repetir nombre, segundo apellido en caso de también repetir el nombre y el primer
    apellido.
    """
    nombreUsuario1=nombre1[0]
    nombreUsuario2=nombre2[0]
    if(nombreUsuario1==nombreUsuario2):
         nombreUsuario1=nombre1[1]
         nombreUsuario2=nombre2[1]
         if(nombreUsuario1==nombreUsuario2):
            nombreUsuario1=nombre1[2]
            nombreUsuario2=nombre2[2]
    return nombreUsuario1,nombreUsuario2

##########################################################################################

def ordenarNombres(matrizOrd):
    """
    Funcionalidad: Ordenar los nombres de forma alfabética en caso de cumplir el mismo día.
    Entradas: La matriz ordenada por días (matrizOrd).
    Salidas: La matriz ordenada por orden alfabético en caso de cumplir el mismo día.
    """
    for indice1,valores in enumerate(matrizOrd):
        salida1=retornarMesDia(valores)
        dia1=salida1[0]
        mes1=salida1[1]
        nombre1=salida1[2]
        for indice2,valores2 in enumerate(matrizOrd[:indice1]):
            salida2=retornarMesDia(valores2)
            dia2=salida2[0]
            mes2=salida2[1]
            nombre2=salida2[2]
            if(dia1==dia2 and mes1==mes2):
                nombresUsuarios=evaluarNombres(nombre1,nombre2)
                nombreUsuario1=nombresUsuarios[0]
                nombreUsuario2=nombresUsuarios[1]
                letra1=nombreUsuario1[0]
                letra2=nombreUsuario2[0]
                if(letra1<letra2):
                    temp = matrizOrd[indice1]
                    matrizOrd[indice1] = matrizOrd[indice2]
                    matrizOrd[indice2]= temp
                elif(letra1==letra2):
                    letra1=nombreUsuario1[1]
                    letra2=nombreUsuario2[1]
                    if(letra1<letra2):
                        temp = matrizOrd[indice1]
                        matrizOrd[indice1] = matrizOrd[indice2]
                        matrizOrd[indice2]= temp
    return matrizOrd

##########################################################################################

def ordenarDias(matriz1):
    """
    Funcionalidad: Ordenar los días de menor a mayor.
    Entradas: La matriz completa generada con los datos generados (matriz1).
    Salidas: La matriz ordenada por los días de menor a mayor (datosUsuario2).
    """
    datosUsuario=[]
    datosUsuario2=[]
    dias=range(32)
    dias=list(dias)
    for valores in matriz1:
        salida=retornarMesDia(valores)
        dia=salida[0]
        mes=salida[1]-1
        if dia in dias:
            index=dia-1
            while(dias[index]!=dia):
                index+=1
            dias.insert(index,valores)
    for valoresUsuario in dias:
        if(isinstance(valoresUsuario,int)==False):
            datosUsuario.append(valoresUsuario)
    datosUsuario2=ordenarNombres(datosUsuario)
    return datosUsuario2

##########################################################################################

def generarMatrizMes(datosUsuario):
    """
    Funcionalidad: Generar la matriz calendario.
    Entradas: Los matriz con los datos (datosUsuario).
    Salidas: El calendario generado (calendario).
    """
    calendario=[[["Enero"],],
            [["Febrero"],],
            [["Marzo"],],
            [["Abril"],],
            [["Mayo"],],
            [["Junio"],],
            [["Julio"],],
            [["Agosto"],],
            [["Setiembre"],],
            [["Octubre"],],
            [["Noviembre"],],
            [["Diciembre"],]]
    for valores in datosUsuario:
        salida=retornarMesDia(valores)
        dia=salida[0]
        mes=salida[1]-1
        for valores1 in calendario:
            if(calendario.index(valores1)==mes):
                 valores1.append(valores)
    return calendario

##########################################################################################

def actualizarTreeview():
    """
    Funcionalidad: Actualiza el treeview.
    Entradas: Ninguna.
    Salidas: Treeview actualizado según el ingreso de datos o eliminación de los mismos.
    """
    valor1=treeview.get_children(enero)
    valor2=treeview.get_children(febrero)
    valor3=treeview.get_children(marzo)
    valor4=treeview.get_children(abril)
    valor5=treeview.get_children(mayo)
    valor6=treeview.get_children(junio)
    valor7=treeview.get_children(julio)
    valor8=treeview.get_children(agosto)
    valor9=treeview.get_children(setiembre)
    valor10=treeview.get_children(octubre)
    valor11=treeview.get_children(noviembre)
    valor12=treeview.get_children(diciembre)
    listaValores=[valor1,valor2,valor3,valor4,valor5,valor6,valor7,valor8,valor9,valor10,valor11,valor12]
    for valores in listaValores:
        for datos in valores:
            treeview.delete(datos)

##########################################################################################

def generarTreeview(calendario):
    """
    Funcionalidad: Genera el treeview según la informacion de la matriz generada.
    Entradas: La matriz calendario (calendario)
    Salidas: El treeview con los datos ingresados.
    """
    actualizarTreeview()
    for valores in calendario:
            for datos in valores:
                if(valores.index(datos)!=0):
                    nombre=datos[0]
                    fecha=datos[1]
                    nombreUsuario=nombre[0]+" "+nombre[1]+" "+nombre[2]
                    mes=int(fecha[3]+fecha[4])
                    cumpleanos = treeview.insert(mes,tk.END,text=fecha[0]+fecha[1]+" "+nombreUsuario)
    return

##########################################################################################

def formarMatriz(datos):
    """
    Funcionalidad: Forma la matriz según los datos ingresados en el scrolledtext.
    Entradas: Los datos del scrolledtext str(datos).
    Salidas: La matriz generada con los datos ingresados (matriz).
    """
    personas=datos.split("|")
    for persona in personas:
        dato=persona.split("°")
        nombreApellidos=dato[0].split(",")
        dato[0]=nombreApellidos
        matriz.append(dato)
    return matriz

##########################################################################################

def obtenerInfo():
    """
    Funcionalidad: Obtiene la información del scrolledtext.
    Entradas: Ninguna.
    Salidas: La lista con esos datos del scrolledtext puros list(lista).
    """
    global lista
    info = editArea.get('1.0', tk.END)
    info=info.strip()
    if validarCantidad(info,lista):
        lista=formarMatriz(info)
        return lista,info
    else:
        return lista,""

##########################################################################################

def generarInformacion():
    """
    Funcionalidad: Genera los datos de cada matriz. 
    Entradas: Ninguna.
    Salidas: El calendario generado de acuerdo a las demás funciones llamadas (calendario).
    """
    global calendario
    global datosUsuario
    global lista
    global matriz
    salida=obtenerInfo()
    lista=salida[0]
    datosUsuario=ordenarDias(lista)
    calendario=generarMatrizMes(datosUsuario)
    generarTreeview(calendario)
    btnHTML.config(state="active")
    btnCorreo.config(state="active")
    try:
        registro = open("amigos.txt","r")
        amigos=registro.readlines()
        registro = open("amigos.txt","a")
        if amigos==[]:
            registro.write(salida[1])
        elif salida[1]=="":
            registro.write("")
        else:
            registro.write("|")
            registro.write(salida[1])
            registro.close()
    except:
        registro = open("amigos.txt","w")
        registro.write(salida[1])
        registro.close()
    return calendario

##########################################################################################

def borrarInfo():
    """
    Funcionalidad: Borra la información del archivo, scrolledtext, treeview, html y cumpleañeros del día.
    Entradas: Ninguna.
    Salidas: Datos de las matrices,listas y archivo borrados totalmente.
    """
    global calendario
    global datosUsuario
    global lista
    global matriz
    editArea.delete(1.0,END)
    btnCorreo.config(state="disable")
    btnHTML.config(state="disable")
    calendario=[[["Enero"],],
            [["Febrero"],],
            [["Marzo"],],
            [["Abril"],],
            [["Mayo"],],
            [["Junio"],],
            [["Julio"],],
            [["Agosto"],],
            [["Setiembre"],],
            [["Octubre"],],
            [["Noviembre"],],
            [["Diciembre"],]]
    datosUsuario=[]
    lista=[]
    matriz=[]
    actualizarTreeview()
    registro=open("amigos.txt","r")
    datos=registro.readline()
    datos=""
    registro=open("amigos.txt","w")
    registro.write(datos)
    registro.close()
    return 

##########################################################################################

def abrirArchivo():
    """
    Funcionalidad: Abre un archivo txt cualquiera mediante el OpenDialog y escribe todo lo que esté en
    ese archivo de texto en el scrolledtext.
    Entradas: Ninguna.
    Salidas: Los datos del archivo en el scrolledtext.
    """
    try:
        file_path = filedialog.askopenfilename()
        f = open(file_path,"r")
        info=""
        for linea in f.readlines():
            info+=linea
        editArea.insert(tk.INSERT,info)
        f.close()
        btnTV.config(state="active")
    except:
        messagebox.showinfo(message="Error al leer el archivo.", title="Atención")

##########################################################################################
        
def generarInformacionInicial(info):
    """
    Funcionalidad: Genera los datos de cada matriz. 
    Entradas: Ninguna.
    Salidas: El calendario generado de acuerdo a las demás funciones llamadas (calendario).
    """
    global calendario
    global datosUsuario
    global lista
    global matriz
    lista=formarMatriz(info[0])
    datosUsuario=ordenarDias(lista)
    calendario=generarMatrizMes(datosUsuario)
    generarTreeview(calendario)
    btnHTML.config(state="active")
    btnCorreo.config(state="active")
    return calendario

##########################################################################################

#Programa Principal

#Especificaciones de la ventana

ventana=tk.Tk()
ventana.title("Mis Amigos")
ventana.resizable(0,0)
ventana.config(bg="lightblue")
window_height = 600
window_width = 1200
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
ventana.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

#Etiquetas

mensaje=Label(ventana,text="Agenda de cumpleaños de amigos", font=("Arial Bold",18), bg="lightblue")
mensaje.place(x=400,y=1)
pregunta=Label(ventana,text="Datos:", bg="lightblue", font=("Arial Bold",14))
pregunta.place(x=10, y=40)
pregunta2=Label(ventana,text="Agenda", bg="lightblue", font=("Arial Bold",14))
pregunta2.place(x=720, y=40)
correo=Label(ventana,text="Cumpleañeros del día", bg="lightblue", font=("Arial Bold",14))
correo.place(x=950, y=150)
generar=Label(ventana,text="Generar HTML", bg="lightblue", font=("Arial Bold",14))
generar.place(x=950, y=250)

#Botones

btnCorreo = Button(ventana, text="       Hoy       ",command=abrirHoy)
btnCorreo.place(x=1000,y=200)
btnHTML = Button(ventana, text="Crear Archivo",command=crearHTML)
btnHTML.place(x=1000,y=300)
btnTV = Button(ventana, text="Agendar",command=generarInformacion)
btnTV.place(x=865,y=480)
btn = Button(ventana, text="Abrir archivo...",command=abrirArchivo)
btn.place(x=590,y=480)
btn1 = Button(ventana, text="Limpiar",command=borrarInfo)
btn1.place(x=530,y=480)
btnCorreo.config(state="disable")
btnHTML.config(state="disable")

#ScrolledText

frame1=Frame()
frame1.pack(padx=1,pady=65,anchor='w') 
frame1.config(bg="lightblue")
editArea = tkst.ScrolledText(master = frame1)
editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

#Treeview

treeview = ttk.Treeview(ventana,height=18)
treeview.place(x=720,y=76)
calendario2 = treeview.insert("", tk.END, iid=0, text="Calendario")
treeview.item(calendario2, open=True)
enero = treeview.insert(calendario2, tk.END, iid=1, text="Enero")
febrero = treeview.insert(calendario2, tk.END, iid=2, text="Febrero")
marzo = treeview.insert(calendario2, tk.END, iid=3, text="Marzo")
abril = treeview.insert(calendario2, tk.END, iid=4, text="Abril")
mayo = treeview.insert(calendario2, tk.END, iid=5, text="Mayo")
junio = treeview.insert(calendario2, tk.END, iid=6, text="Junio")
julio = treeview.insert(calendario2, tk.END, iid=7, text="Julio")
agosto = treeview.insert(calendario2, tk.END, iid=8, text="Agosto")
setiembre = treeview.insert(calendario2, tk.END, iid=9, text="Setiembre")
octubre = treeview.insert(calendario2, tk.END, iid=10, text="Octubre")
noviembre = treeview.insert(calendario2, tk.END, iid=11, text="Noviembre")
diciembre = treeview.insert(calendario2, tk.END, iid=12, text="Diciembre")

#Revisa si hay amigos registrados al iniciar el programa y los ordena en el treeview.

try:
    registro=open("amigos.txt","r")
    listaDeAmigos=registro.readlines()
    if listaDeAmigos==" ":
        ""
    else:
        generarInformacionInicial(listaDeAmigos)
        btnCorreo.config(state="active")
        btnHTML.config(state="active")
    registro.close()
except:
    ""
ventana.mainloop()        

