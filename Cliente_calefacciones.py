import socket, sys, os, select

PORT = 50001
TIMER = 0.1

Menu = """ 
#########################################################
#    1. Encender/Apagar                                 #
#    2. Listar radiadores                               #
#    3. Temperatura actual                              #
#    4. Mostrar temperatura deseada establecida         #
#    5. Establecer temperatura deseada                  #
#    6. Salir                                           #
#########################################################
"""

MenuONN = """
#################################
#    1. Encender                #
#    2. Apagar                  #
#################################
"""

errores = {
    0: "Error desconocido",
    1: "Comando desconocido.",
    2: "Parámetro inesperado. Se ha recibido un parámetro donde no se esperaba.",
    3: "Falta parámetro. Falta un parámetro que no es opcional.",
    4: "Parámetro con formato incorrecto.",
    11: "Error del servidor: No se ha podido encender/apagar el/los radiador(es)",
    12: "Error del servidor: No se ha podido obtener la lista de radiadores",
    13: "Error del servidor: No se ha podido obtener la temperatura del (los) radiador(es)",
    14: "Error del servidor: No se ha podido obtener la temperatura deseada",
    15: "Error del servidor: No se ha podido establecer la temperatura deseada"

}

if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

ipAddress = socket.gethostbyname(sys.argv[1])
dir_serv = (ipAddress, PORT)
s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
s.connect(dir_serv)

def printearError(err):
    #Usamos try por si el servidor manda un error que no conocemos
    #Si el indice no coincide con ningun error nos fallaría el programa
    #De esta forma nos aseguramos de que siga funcionando
    try:
        if len(err) == 3:
            er = int(err[2])
            print(errores[er])
        elif len(err) == 4:
            er = int(err[2:4])
            print(errores[er])
        else:
            print(errores[0])
    except:
        print(errores[0])
    

def listarRadiadores():
    mensaje = 'NAM'.encode()
    s.send(mensaje)
    buf = b''
    respuesta = b''
    while True:
        lista, _, _ = select.select([s],[],[],TIMER)
        if not lista:
            break
        buf = s.recv( 1024 )
        respuesta = respuesta + buf
    respuesta = respuesta.decode()
    if respuesta[0:2] == "ER":
        printearError(respuesta)
    else:
        respuesta = respuesta[2:].split(":")
        for i in respuesta:
            aux = i.split(",")
            print(aux[0], " ", aux[1])
    input("Pulsa enter para continuar...")


def encenderApagar():
    print(MenuONN)
    res = int(input())
    if res == 1:
        res = "0"
    elif res == 2:
        res = "1"
    else:
        print("incorrecto")
        return
    idRadiador = input("Id radiador: ")
    mensaje = 'ONN' + res 
    if idRadiador != "":
        mensaje = mensaje + ":" + idRadiador
    s.send(mensaje.encode())
    respuesta = s.recv( 1024 )
    if respuesta[0:2] == "ER":
        printearError(respuesta)
    else:
        print("Operacion realizada correctamente")
    input("Pulsa enter para continuar...")

def temperaturaAct():
    
    usr = input("Id radiador: ")
    mensaje = 'NOW' + usr
    s.send(mensaje.encode())
    buf = b''
    recibido = b''
    while True:
        lista, _, _ = select.select([s],[],[],TIMER)
        if not lista:
            break
        buf = s.recv( 1024 )
        recibido = recibido + buf
    recibido = recibido.decode()
    if recibido[0:2] == "ER":
        printearError(recibido)
    else:
        recibido = recibido[2:].split(":")
        for i in recibido:
            print(i[0:2] + "," + i[2])
    input("Pulsa enter para continuar...")


def getTempEstab():
    usr = input("Id radiador: ")
    mensaje = 'GET' + usr
    s.send(mensaje.encode())
    buf = b''
    recibido = b''
    while True:
        lista, _, _ = select.select([s],[],[],TIMER)
        if not lista:
            break
        buf = s.recv( 1024 )
        recibido = recibido + buf
    recibido = recibido.decode()

    if recibido[0:2] == "ER":
        printearError(recibido)
    else:
        recibido = recibido[2:].split(":")
        for i in recibido:
            print(i[0:2] + "," + i[2])
    input("Pulsa enter para continuar...")

def setTempEstab():
    usr = input("Id radiador: ")
    temp = input("Temperatura: ")
    mensaje = 'SET' + temp
    if usr != "":
        mensaje = mensaje + ":" + usr
    s.send(mensaje.encode())
    respuesta = s.recv( 1024 )
    print(respuesta[0:2])
    if respuesta[0:2] == "ER":
        printearError(respuesta)
    else:
        print("Operacion realizada correctamente")
    input("Pulsa enter para continuar...")

while True:
    print(Menu)
    inP = input()
    if inP == "":
        exit(0)
    inP = int(inP)
    if inP == 1:
        encenderApagar()
    elif inP == 2:
        listarRadiadores()
    elif inP == 3:
        temperaturaAct()
    elif inP == 4:
        getTempEstab()
    elif inP == 5:
        setTempEstab()
    elif inP == 6:
        exit(0)
    else:
        print("Opcion incorrecta")

s.close()
