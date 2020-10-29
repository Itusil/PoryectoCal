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


radiadores= list()
r1= Radiador("1234", "Habitación1","234","200", "1")
r2= Radiador("20", "Habitación2","278", "250","1")
r3= Radiador("5", "Cuarto de baño", "237", "237", "0")
radiadores.append(r1)
radiadores.append(r2)
radiadores.append(r3)



def sendOK( s, dir_cli, params="" ):
	s.sendto( ("OK{}".format( params )).encode( "ascii" ), dir_cli)

def sendER( s, dir_cli, code=1):
	s.sendto( ("ER{}".format( code )).encode( "ascii" ), dir_cli)

def sendOKNombres( s, dir_cli, params="" ):
	s.sendto( ("OK{}".format( params )).encode( "UTF-8" ), dir_cli)

def radiadorExiste(id_):
    for ww in range(0, len(radiadores)):
        if(radiadores[ww].id_ == id_):
            return ww
    return -1


while True:
    buf, dir_cli = s.recvfrom( 1024 )
    mensaje = buf.decode()
    longitud=len(mensaje)
    #comand= mensaje[0]+mensaje[1]+mensaje[2]
    comand=mensaje[0:3]
    if(comand == "ONN"):
       #s.sendto( "Comando ONN".encode(), dir_cli)

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
                sendER(s, dir_cli, 4)
        elif(longitud >4 and mensaje[4] == ":"):
            id_ = mensaje[5:longitud]
            try:
                intid = int(id_)
                di= radiadorExiste(id_)
                if(di >= 0):
                    if(mensaje[3] == "0"):
                        radiadores[di].estado="0"
                        sendOK(s, dir_cli, "")
                    elif(mensaje[3] == "1"):
                        radiadores[di].estado="1"
                        sendOK(s, dir_cli, "")
                    else:
                        #OJO! PARAMETRO NO ES MAL FORMATO O SI?
                        sendER(s, dir_cli, 4)
                else:
                    sendER(s, dir_cli,11)
            except ValueError:
                sendER(s, dir_cli,4)
        else:
            if(longitud <4):
                sendER(s, dir_cli,3)
            else:
                sendER(s, dir_cli,4)
        
        
    elif(comand == "NAM"):
        if(longitud>3):
            sendER(s, dir_cli,2 )
        else:
            mensajeMandar = ""
            #mensaje vacio error 12
            #Hablado en tutoria: Hacer que de manera aleatoria no pueda cargar el nombre de radiadores y devuelva el codigo 12
            aleatorio = random.random()
            if aleatorio>0.20: #Un 80% de los casos cargará el mensaje y en un 20% dará error
                for z in range(0, len(radiadores)):
                    mensajeMandar= mensajeMandar+radiadores[z].id_+","+radiadores[z].nombre 
                    if(z != (len(radiadores)-1)):
                        mensajeMandar=mensajeMandar+":"
            if mensajeMandar!= "":
                #Preguntar (sobre UTF-8)
                sendOKNombres(s, dir_cli, mensajeMandar)
            else:
                sendER(s, dir_cli, 12)

    elif(comand == "NOW"):
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
                pos= radiadorExiste(id_)
                if (pos>=0):
                    mensajeMandar=radiadores[pos].tempeFuera
                    sendOK(s, dir_cli, mensajeMandar)
                else:
                    sendER(s, dir_cli,13)
            except ValueError:
                sendER(s, dir_cli,4)
            

    elif(comand == "GET"):
        if(longitud==3):
            mensajeMandar=""
            for z in range(0, len(radiadores)):
                mensajeMandar=mensajeMandar+radiadores[z].tempeRadia
                if(z != ult):
                    mensajeMandar=mensajeMandar+":"
            sendOK(s, dir_cli, mensajeMandar)
        else:
            id_ = mensaje[3:longitud]
            try:
                intid = int(id_)
                pos= radiadorExiste(id_)
                if (pos>=0):
                    mensajeMandar=radiadores[pos].tempeRadia
                    sendOK(s, dir_cli, mensajeMandar)
                else:
                    sendER(s, dir_cli,14)
            except ValueError:
                sendER(s,dir_cli,4)



    elif(comand == "SET"):
        if(longitud == 3):
            sendER(s, dir_cli, 3)
        elif(longitud<6):
            sendER(s, dir_cli, 4)
        else:
            temp=mensaje[3:6]
            try:
                inttemp = int(temp)
                if(longitud == 6):
                    for xx in range (0, len(radiadores)):
                        radiadores[xx].tempeRadia=temp
                    sendOK(s, dir_cli, "")
                elif(longitud >6 and mensaje[6]==":"):
                    id_ = mensaje[7:longitud]
                    try:
                        intid = int(id_)
                        pos = radiadorExiste(str(id_))
                        if(pos>=0):
                            radiadores[pos].tempeRadia=temp
                            sendOK(s, dir_cli,"")
                        else:
                            sendER(s, dir_cli, 15)
                    except ValueError:
                        sendER(s, dir_cli,4)
                else:
                    sendER(s, dir_cli, 4) #Error separador
            except ValueError:
                sendER(s, dir_cli,4)
    else:
            sendER(s, dir_cli, 1)


s.close()

