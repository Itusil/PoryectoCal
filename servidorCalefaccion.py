#!/usr/bin/env python3

import socket

PORT = 50001

s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

s.bind( ('', PORT) )

class Radiador:
  def __init__(self, ida, tempe ,estado):
    self.ida = ida
    self.tempe = tempe
    self.estado=estado
  def setTemp(tempp):
    self.tempe=tempp

  def getEstado():
    return self.estado 
  def setEstado(est__):
    self.estado=est__

radiadores= list()
r1= Radiador("1234","234","1")
r2= Radiador("20", "200","1")
radiadores.append(r1)
radiadores.append(r2)





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
       s.sendto( "Comando ONN".encode(), dir_cli)
    elif(comand == "NAM"):
        s.sendto( "Comando NAM".encode(), dir_cli)
    elif(comand == "NOW"):
        s.sendto( "Comando NOW".encode(), dir_cli)
    elif(comand == "GET"):
        #s.sendto( "Comando GET".encode(), dir_cli)
        if(longitud>3):
            esp=1
            ida=list()
            for x in range(3,len(lista)):
                ida.append(lista[x])
        else:
            esp=0
        if(esp==0):
            #Hay que canbiar el string de respuesta por un OK
            res="Temperatura en todos los radiadores ????"
            s.sendto( res.encode(), dir_cli)
        else:
            idas=''.join(ida)
            pos = radiadorExiste(str(idas))
            if(pos==-1):
                s.sendto( "ERROR RADIADOR".encode(), dir_cli)
                #exit(15)
            #hacer obtener radiadior y cambiarla la temperatura con radiadores[pos].setTemp()...
            r=radiadores[pos]
            res="Temperatura del radiador id: "+r.ida+" es "+r.tempe
            s.sendto( res.encode(), dir_cli)

    elif(comand == "SET"):
        #s.sendto( "Comando SET".encode(), dir_cli)
        temp=lista[3]+lista[4]+lista[5]
        if(longitud>6):
            esp=1
            ida=list()
            for x in range(6,len(lista)):
                ida.append(lista[x])
        else:
            esp=0
        if(esp==0):
            #Hay que canbiar el string de respuesta por un OK
            res="Temperatura en todos los radiadores cambiada a "+str(temp)
            s.sendto( res.encode(), dir_cli)
        else:
            idas=''.join(ida)
            pos = radiadorExiste(str(idas))
            if(pos==-1):
                s.sendto( "ERROR RADIADOR".encode(), dir_cli)
                #exit(15)
            #hacer obtener radiadior y cambiarla la temperatura con radiadores[pos].setTemp()...
            radiadores[pos].tempe=str(temp)
            r=radiadores[pos]
            res="Temperatura en el radiador id: "+r.ida+" cambiada a "+r.tempe
            s.sendto( res.encode(), dir_cli)
    else:
	        s.sendto( "MAL COMANDO".encode(), dir_cli)


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

