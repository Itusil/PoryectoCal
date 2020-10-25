#!/usr/bin/env python3

import socket

PORT = 50001

s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

s.bind( ('', PORT) )

class Radiador:
  def __init__(self, ida, nombre, tempeFuera , tempeRadia,estado):
    self.ida = ida
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
	s.sendto( ("OK{}\r\n".format( params )).encode( "ascii" ), dir_cli)

def sendER( s, dir_cli, code=1):
	s.sendto( ("ER{}\r\n".format( code )).encode( "ascii" ), dir_cli)


def radiadorExiste(id_):
    for ww in range(0, len(radiadores)):
        if(radiadores[ww].ida == id_):
            return ww
    return -1


"""Esta identado"""
while True:
    buf, dir_cli = s.recvfrom( 1024 )
    lista = list(buf.decode())
    longitud=len(lista)
    comand= lista[0]+lista[1]+lista[2]

    if(comand == "ONN"):
       #s.sendto( "Comando ONN".encode(), dir_cli)

        if(longitud == 4):
            if(lista[3] == "0"):
                for onnn in range(0, len(radiadores)):
                    radiadores[onnn].estado="0"
                s.sendto( "0".encode(), dir_cli)
                #sendOK(s, dir_cli, "")
            elif(lista[3] == "1"):
                for onnn in range(0, len(radiadores)):
                    radiadores[onnn].estado="1"
                s.sendto( "1".encode(), dir_cli)
                #sendOK(s, dir_cli, "")
            else:
                print("ERROR")
                #sendER(s, dir_cli, 4)
                #exit()
        elif(longitud >4):
            i = 4
            idd = ""
            while(i < longitud):
                idd += lista[i]
                i += 1
            try:
                intid = int(idd)
                di= radiadorExiste(idd)
                if(di != 0):
                    if(lista[3] == "0"):
                        for onnn in range(0, len(radiadores)):
                            radiadores[onnn].estado="0"
                        s.sendto( "0".encode(), dir_cli)
                        #sendOK(s, dir_cli, "")
                    elif(lista[3] == "1"):
                        for onnn in range(0, len(radiadores)):
                            radiadores[onnn].estado="1"
                        s.sendto( "0".encode(), dir_cli)
                        #sendOK(s, dir_cli, "")
                else:
                    print("No existe el radiador")
                    #sendER(s, dir_cli,11)
            except ValueError:
                print("Id con formato incorrecto")
                #exit(4)
                #sendER(s, dir_cli,4)
        else:
            print("Falta parámetro")
            #sendER(s, dir_cli,3)
        
        
    elif(comand == "NAM"):
        #s.sendto( "Comando NAM".encode(), dir_cli)
        if(longitud>3):
            print("ERROR")
            #sendER(s, dir_cli,2 )
        else:
            mensaje = ""
            for www in range(0, len(radiadores)):
                mensaje= mensaje+radiadores[www].ida+","+radiadores[www].nombre 
                if(www != (len(radiadores)-1)):
                    mensaje=mensaje+":"
            s.sendto( mensaje.encode(), dir_cli)
            #sendOK(s, dir_cli, mensaje)

    elif(comand == "NOW"):
        #s.sendto( "Comando NOW".encode(), dir_cli)
        if(longitud == 3):
            mensaje = ""
            for www in range(0, len(radiadores)):
                mensaje= mensaje+radiadores[www].ida+","+radiadores[www].tempeFuera
                ult =len(radiadores)-1
                if(www != ult):
                    mensaje=mensaje+":"
            s.sendto( mensaje.encode(), dir_cli)
            #sendOK(s, dir_cli, mensaje)
        else:
            ida=""
            for x in range(3,len(lista)):
                ida=ida+lista[x]
            try:
                intid = int(ida)
                pos= radiadorExiste(ida)
                if (pos>=0):
                    mensaje=radiadores[pos].tempeFuera
                    s.sendto( mensaje.encode(), dir_cli)
                    #sendOK(s, dir_cli, mensaje)
                else:
                    mensaje="ERROR"
                    s.sendto( mensaje.encode(), dir_cli) 
                    #sendER(s, dir_cli,13)
            except ValueError:
                print("Id con formato incorrecto")
                #exit(4)
                #sendER(s, dir_cli,4)
            

    elif(comand == "GET"):
        #s.sendto( "Comando GET".encode(), dir_cli)
        if(longitud==3):
            mensaje=""
            for www in range(0, len(radiadores)):
                mensaje= mensaje+"Radiador id: "+ radiadores[www].ida+", temperatura: "+radiadores[www].tempeRadia+"\n"
            s.sendto( mensaje.encode(), dir_cli)
        else:
            ida=""
            for x in range(3,len(lista)):
                ida=ida+lista[x]
            pos = radiadorExiste(str(ida))
            try:
                intid = int(ida)
                pos= radiadorExiste(ida)
                if (pos>=0):
                    mensaje=radiadores[pos].tempeRadia
                    s.sendto( mensaje.encode(), dir_cli)
                    #sendOK(s, dir_cli, mensaje)
                else:
                    mensaje="ERROR"
                    s.sendto( mensaje.encode(), dir_cli) 
                    #sendER(s, dir_cli,14)
            except ValueError:
                print("Id con formato incorrecto")
                #exit(4)
                #sendER(s,dir_cli,4)



    elif(comand == "SET"):
        #s.sendto( "Comando SET".encode(), dir_cli)
        if(longitud == 3):
            print("ERROR")
            #sendER(s, dir_cli, 3)
        elif(longitud<6):
            print("ERROR")
            #sendER(s, dir_cli, 4)
        else:
            temp=lista[3]+lista[4]+lista[5]
            try:
                inttemp = int(temp)
                if(longitud == 6):
                    for xx in range (0, len(radiadores)):
                        radiadores[xx].tempeRadia=temp
                    res="Temperatura en todos los radiadores cambiada a "+str(temp)
                    s.sendto( res.encode(), dir_cli)
                    #sendOK(s, dir_cli, "")
                else:
                    ida=""
                    for x in range(6,len(lista)):
                        ida= ida +lista[x]
                    try:
                        intid = int(ida)
                        pos = radiadorExiste(str(ida))
                        if(pos>=0):
                            radiadores[pos].tempeRadia=temp
                            s.sendto( temp.encode(), dir_cli)
                            #sendOK(s, dir_cli,"")
                        else:
                            s.sendto( "ERROR RADIADOR".encode(), dir_cli)
                            #sendER(s, dir_cli, 15)
                    except ValueError:
                        print("Id con formato incorrecto")
                        #exit(4)
                        #sendER(s, dir_cli,4)
            except ValueError:
                print("Temperatura con formato incorrecto")
                #exit(4)
                #sendER(s, dir_cli,4)
    else:
	        s.sendto( "MAL COMANDO".encode(), dir_cli)
            #sendER(s, dir_cli, 1)


s.close()
"""
if __name__ == "__main__":
    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    s.bind( ('', PORT) )

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        buf, dir_cli = s.recvfrom( MAX_BUF )
        print( "Conexión aceptada del socket {0[0]}:{0[1]}.".format( address ) )
        if( os.fork() ):
            dialog.close()
        else:
            s.close()
            session( dialog )
            dialog.close()
            exit( 0 )"""

