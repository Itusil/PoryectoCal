#!/usr/bin/env python3

import socket
import random

PORT = 50001

s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

s.bind( ('', PORT) )

class Radiador:
  def __init__(self, id_, nombre, tempeFuera , tempeRadia,estado):
    self.id_ = id_
    self.nombre=nombre
    self.tempeFuera = tempeFuera
    self.tempeRadia = tempeRadia
    self.estado=estado

#Creamos una lista de radiadores donde guardaremos los radiadores
radiadores= list()
r1= Radiador("1", "Habitación1","234","200", "1")
r2= Radiador("2", "Habitación2","278", "250","1")
r3= Radiador("3", "Cuarto de baño", "237", "237", "0")
radiadores.append(r1)
radiadores.append(r2)
radiadores.append(r3)



def sendOK( s, dir_cli, params="" ):
	s.sendto( ("OK{}".format( params )).encode( "UTF-8" ), dir_cli)

def sendER( s, dir_cli, code=1):
	s.sendto( ("ER{}".format( code )).encode( "ascii" ), dir_cli)


def radiadorExiste(id_): #Devulve la posicion del radiador en el array de radiadores y, si no existe, devuelve -1
    for ww in range(0, len(radiadores)):
        if(radiadores[ww].id_ == id_):
            return ww
    return -1

def comandoONN():
    if(longitud == 4):
        if(mensaje[3] == "0"):
            for z in range(0, len(radiadores)):
                radiadores[z].estado="0"
            sendOK(s, dir_cli, "")
        elif(mensaje[3] == "1"):
            for z in range(0, len(radiadores)):
                radiadores[z].estado="1"
            sendOK(s, dir_cli, "")
        else:
            sendER(s, dir_cli, 4) #No puede ser un numero distinto a 0 o a 1

    elif(longitud >4 and mensaje[4] == ":"): #Comprobamos que el separador de parametros sea correcto
        id_ = mensaje[5:longitud]
        try:
            intid = int(id_) #Comprobar que el id es un numero (no contiene letras)
            if(intid <0): #Numero Id negativo
                sendER(s, dir_cli, 4)
            else:
                di= radiadorExiste(id_)
                if(di >= 0):
                    if(mensaje[3] == "0"):
                        radiadores[di].estado="0"
                        sendOK(s, dir_cli, "")
                    elif(mensaje[3] == "1"):
                        radiadores[di].estado="1"
                        sendOK(s, dir_cli, "")
                    else:
                        sendER(s, dir_cli, 4)  #No puede ser un numero distinto a 0 o a 1
                else:
                    sendER(s, dir_cli,11) #Radiador introducido no existe
        except ValueError:
            sendER(s, dir_cli,4) #El radiador no es un numero entero
    else:
        if(longitud <4):
            sendER(s, dir_cli,3) #Falta parametro de encender (1) o apagar (0)
        else:
            sendER(s, dir_cli,4) #Separador incorrecto

def comandoNAM():
    if(longitud>3):
        sendER(s, dir_cli,2) #Nam no puede tener parametros
    else:
        mensajeMandar = ""
        #Si el mensaje es vacio error 12
        #Hablado en tutoria: Hacer que de manera aleatoria no pueda cargar el nombre de radiadores y devuelva el codigo 12
        aleatorio = random.random()
        if aleatorio>0.20: #Un 80% de los casos cargará el mensaje y en un 20% dará error y devolverá error 12
            for z in range(0, len(radiadores)):
                mensajeMandar= mensajeMandar+radiadores[z].id_+","+radiadores[z].nombre 
                if(z != (len(radiadores)-1)):
                    mensajeMandar=mensajeMandar+":"
        if mensajeMandar!= "":
            sendOK(s, dir_cli, mensajeMandar)
        else:
            sendER(s, dir_cli, 12) #No ha podido cargar los radiadores

def comandoNOW():
    if(longitud == 3):
        mensajeMandar = ""
        for z in range(0, len(radiadores)):
            mensajeMandar= mensajeMandar+radiadores[z].tempeFuera
            ult =len(radiadores)-1
            if(z != ult):
                mensajeMandar=mensajeMandar+":"
        sendOK(s, dir_cli, mensajeMandar)
    else:
        id_ = mensaje[3:longitud]
        try:
            intid = int(id_)
            if(intid <0): 
                sendER(s, dir_cli, 4) #Numero Id negativo
            else:
                pos= radiadorExiste(id_)
                if (pos>=0):
                    mensajeMandar=radiadores[pos].tempeFuera
                    sendOK(s, dir_cli, mensajeMandar)
                else:
                    sendER(s, dir_cli,13) #El radiador no existe
        except ValueError:
            sendER(s, dir_cli,4) #El id introducido no es un entero (Ejemplo: contiene letras)

def comandoGET():
    if(longitud==3):
        mensajeMandar=""
        for z in range(0, len(radiadores)):
            mensajeMandar=mensajeMandar+radiadores[z].tempeRadia
            ult =len(radiadores)-1
            if(z != ult):
                mensajeMandar=mensajeMandar+":"
        sendOK(s, dir_cli, mensajeMandar)
    else:
        id_ = mensaje[3:longitud]
        try:
            intid = int(id_)
            if(intid <0): #Numero Id negativo
                sendER(s, dir_cli, 4)
            else:
                pos= radiadorExiste(id_)
                if (pos>=0):
                    mensajeMandar=radiadores[pos].tempeRadia
                    sendOK(s, dir_cli, mensajeMandar)
                else:
                    sendER(s, dir_cli,14) #El radiador no existe
        except ValueError:
            sendER(s,dir_cli,4) #El id introducido no es un entero (Ejemplo: contiene letras)

def comandoSET():
    if(longitud == 3):
        sendER(s, dir_cli, 3) #El comando set tiene que tener por obligacion el parametro de la temperatura
    elif(longitud<6):
        sendER(s, dir_cli, 4) #El parametron de la temperatura es incorrecto porque no tiene la longitud suficiente de 3 digitos
    else:
        temp=mensaje[3:6]
        try:
            inttemp = int(temp) 
            if(inttemp<0): #Error porque la temperatura es negativa
                sendER(s, dir_cli, 4)                
            elif(longitud == 6):
                for xx in range (0, len(radiadores)):
                    radiadores[xx].tempeRadia=temp
                sendOK(s, dir_cli, "")
            elif(longitud >6 and mensaje[6]==":"):
                id_ = mensaje[7:longitud]
                try:
                    intid = int(id_)
                    if(intid <0): 
                        sendER(s, dir_cli, 4) #Error porque el numero Id es negativo
                    else:
                        pos = radiadorExiste(str(id_)) 
                        if(pos>=0):
                            radiadores[pos].tempeRadia=temp
                            sendOK(s, dir_cli,"")
                        else:
                            sendER(s, dir_cli, 15) #Error porque el radiador introducido no existe
                except ValueError:
                    sendER(s, dir_cli,4) #Error porque el id introducido no es un entero (Ejemplo: contiene letras) 
            else:
                sendER(s, dir_cli, 4) #Error separador
        except ValueError:
            sendER(s, dir_cli,4) #Error porque la temperatura no es un entero (Ejemplo: contiene letras) 

while True:
    buf, dir_cli = s.recvfrom( 1024 )
    mensaje = buf.decode()
    longitud=len(mensaje)
    comand=mensaje[0:3]
    if(comand == "ONN"):
        comandoONN()
    elif(comand == "NAM"):
        comandoNAM()
    elif(comand == "NOW"):
        comandoNOW()
    elif(comand == "GET"):
        comandoGET()
    elif(comand == "SET"):
        comandoSET()
    else:
        sendER(s, dir_cli, 1) #Comando desconocido
s.close()

