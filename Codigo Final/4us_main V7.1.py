#################################################################################################################################################

#                   Pequeña demo e implementacion del sistema mqtt para la publicacion de datos y estadistacas del sistema 4us

#####################################################################################################################################################3
from sortedcollections import SortedList
import numpy as np
import scipy.fftpack as fourier
import pyaudio as pa
import struct
import threading
import queue
import csv
import random
from time import sleep
from keyboard import is_pressed
from paho.mqtt import client as mqtt_client
#import RPi.GPIO as GPIO

notref = [["metal", [1450.00, 1500.00, 1600.00, 2000.00, 3000.00, 3500,
                     800, 700], True], ["plastico", [0, 0], False], ["aire", []]]#200, 300, 100]]]

FRAMES = 1024*8                                   # Tamaño del paquete a procesar
FORMAT = pa.paInt16                               # Formato de lectura INT 16 bits
CHANNELS = 1
# Frecuencia de muestreo típica para audio
Fs = 44100

##### Asignaciones de la base de datos csv #####
database = []
# asigana los nombres de cada dato
indices = ["tipo", "freq_mic", "freq_cap", "val_ind"]
csv_file = "database.csv"
capacitivo = 88888  # Valor temporal (a reemplazar)
amplitud = 5555    # Valor temporal (a reemplazar)

# creo una queue de tipo last in first out
cola = queue.LifoQueue()

p = pa.PyAudio()

tolerancia = 50
estado = False

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = '4us_client'
password = 'recicle'

######### Mensaje de ejemplo::
msg = {"msttrown":["plastico",3452],
        "lsstrown":["metal",184],
        "cnttrown":[52987,9098]}


sensor_2 = 21
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(sensor_2,GPIO.IN)

# Funcion que limpia la entrada de datos y detecta el tipo de material


def limpiadora_general(a_limpiar,noise_flr):
    print("Data recivida por limpiadora general: ",a_limpiar)
    a_limpmic = []
    a_limpamp = []
    for a in range(len(a_limpiar)):
        print("Noise flr vale: ",noise_flr)
        if a_limpiar[a][1] >= noise_flr*0.75:
            a_limpmic.append(a_limpiar[a][1])
            print("Data agregada: ",a_limpiar[a][1],"                  data si guardada",a_limpiar[a][0])
        else:
            print("Data no guardada: ",a_limpiar[a][1],"Con frecuencia: ",a_limpiar[a][0])
    ref = fst_lectora()
    filtrado = []
    finales = []
    limpio = []
    espref = []
    nom = ""
    a_limpmic = SortedList(a_limpmic)
    #print("data recivida para limpiar: ",a_limpiar)
    if len(ref) != 0 and len(ref) >= 6:
        for b in range(len(ref)):
            try:
                nom = ref[str(b+1)]["tipo"]
                print("nom asignada ", nom)
            except:
                print("ERROR_ ASIGNACION NOMBRE")
            try:
                espref = [str(b+1)]["freq_mic"]
                print("espref asignada ", espref)
            except:
                print("ERROR_ ASIGNACION PARAMETROS")
            for c in range(len(a_limpmic)):
                for z in range(len(espref)):
                    #print("espref vale: ",espref)
                    limpio = list(a_limpmic.irange(
                        0.65 * int(espref[z]), 1.55 * int(espref[z])))
                    filtrado.append(limpio)
                    filtrado = [*set(filtrado)]
    else:
        print("WARN __ Ref nula o insuficiente, usando ref nativa....")
        for nrf in range(len(notref)):
            espref = notref[nrf][1]
            nom = notref[nrf][0]
            #ferrintrs = notref[nrf][2]
            for c in range(len(a_limpmic)):
                for z2 in range(len(espref)):
                    #print("espref vale: ",espref)
                    limpio = list(a_limpmic.irange(
                        0.65 * int(espref[z2]), 1.55 * int(espref[z2])))
                    if limpio != []:
                        filtrado = filtrado + limpio
                        filtrado = [*set(filtrado)]
                        print("fil trado vale: ",filtrado,"con nombre ",nom)
    finales.append([limpio, nom])
    if filtrado != []:
        if is_pressed("m"):
            nom = "metal"
            print("simulando sens.ind...")
            print("El material es un: ",nom," y vale :", filtrado)
        else:
            print("el material es un: ", nom," y vale :", filtrado)
        if is_pressed("a"):
            print("asignando datos....")
            intnom = input("Ingrese el nombre del material a cargar: ")
            asignadora(intnom, limpio, 0,0)
            return (0)
    else:
        print("no hay un material con freq importante")
        print("limpio vale : ", limpio)
    return(nom)

def noise_floor(cicles):
    noise_lvl = []
    print("cantidad de ciclos a realizar: ",cicles)
    for one in range(cicles):
        crntnoise = cola.get()
        crntnoise = crntnoise[1]
        if crntnoise <= 200:
            noise_lvl.append(crntnoise)
    print("Valores de ruido: ",noise_lvl)
    noise_flr = sum(noise_lvl)/len(noise_lvl)
    print("Valor promedio de ruido: ",noise_flr)
    return(noise_flr)
def fst_lectora():
    cont = 0
    upto_database = {}
    with open(csv_file, newline="") as File:
        print("inicio de fst lectura")
        lectura = csv.reader(File)
        for row in lectura:
            cont = cont+1
            #print("row a leer por fst lectora: ",row)
            if row != []:
                row = {'tipo': row[0], 'freq_mic': row[1], 'val_ind': row[2]}
                upto_database[str(cont+1)] = row
            else:
                print("espacio vacio")
                cont = cont - 1
        #print("Saliendo de fst lectora, lista final: ",upto_database)
        return (upto_database)

##### Funcion creadora: Pide la entrada de datos para la clase asignadora ####


def creadora():  # 1
    nombre = str(input("Nombre del material a cargar? :  "))
    freq_mic = newfreq
    freq_cap = 1234  # agarrar el valor de diferencia de capacitancia directo de la pico
    val_ind = 1  # agarrar el valor del sensor inductivo directo de la pico
    print("Valores asignados, clase creada ")
    return (nombre, freq_mic, val_ind, freq_cap)
##### Funcion asignadora: guarda los datos en el diccionario de forma ordenada ####


def asignadora(nombre, freq_mic, val_ind, freq_cap):  # 2
    formated = {"tipo": nombre, "freq_mic": freq_mic,
                "freq_cap": freq_cap, "val_ind": val_ind}
    print("entro en almacenadora ", formated)
    upto_database = sup_lectora(formated)
    almacenadora(upto_database)
    return
##### Funcion almacenadora: Guarda los datos del diccionario en el csv para formar la base de datos ####


def almacenadora(goto):  # 3
    cont = 0
    try:
        with open(csv_file, "w") as file:
            writer = csv.DictWriter(file, fieldnames=indices)
            # writer.writeheader() deberia arreglar esto pero ya es muy tarde, asi funciona y punto
            print("          ")
            for data in goto:
                cont = cont + 1
                print("data a cargar ", goto[str(cont+1)])
                if goto[str(cont+1)] != ['tipo', 'freq_mic', 'freqcap', 'valamp']:
                    writer.writerow(goto[str(cont+1)])
                    print("data guardada")
                else:
                    print("excepcion de header")
    except IOError:
        print("I/O error")


def sup_lectora(goto_database):
    cont = 0
    upto_database = {}
    with open(csv_file, newline="") as File:
        print("inicio de lectura")
        lectura = csv.reader(File)
        for row in lectura:
            cont = cont+1
            print("row vale : ", row)
            if row != []:
                row = {'tipo': row[0], 'freq_mic': row[1], 'val_ind': row[2]}
                upto_database[str(cont+1)] = row
            else:
                cont = cont-1
        upto_database[str(cont+2)] = goto_database
        return (upto_database)


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,msg):
    msttrown = msg["msttrown"]
    lsstrown = msg["lsstrown"]
    cnttrown = msg["cnttrown"]
    topics = ["Depositado mas veces","Depositado menos veces","cantidad de residuos depositados"]
    for a in range(len(topics)):
        sleep(1)
        if a == 0:
            topic = topics[a]
            msg = "Se recomienda reducir la cantidad de "+str(msttrown[0])+" porque se tiro "+str(msttrown[1])+" veces"
            result = client.publish(topic,msg)
        if a == 1:
            topic = topics[a]
            msg = "El material que menos veces se deposito fue: "+str(lsstrown[0])+" Y se deposito "+str(lsstrown[1])+" veces"
            result = client.publish(topic,msg)
        if a == 2:
            topic = topics[a]
            msg = "Se depositaron "+str(cnttrown[0])+" materiales reciclables, y se devolvieron "+str(cnttrown[1])+" materiales"
            result = client.publish(topic,msg)
        else:
            pass
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

def runmqtt():
    client = connect_mqtt()
    client.loop_start()
    publish(client,msg)
# funcion de calculos fft (magnitud de frecuencia y amplitud)


def calculadorafft(cola):
    cont = 0
    stream = p.open(                                  # Abrimos el canal de audio con los parámeteros de configuración
        format=FORMAT,
        channels=CHANNELS,
        rate=Fs,
        input=True,
        output=True,
        frames_per_buffer=FRAMES
    )
    while True:
        if cont >= 60:
            print("calculadora sigue corriendo", cont)
            cont = 0
        # Creamos el vector de frecuencia para encontrar la frecuencia dominante
        F = (Fs/FRAMES)*np.arange(0, FRAMES//2)
        data = stream.read(FRAMES)
        dataInt = struct.unpack(str(FRAMES) + 'h', data)
        M_gk = abs(fourier.fft(dataInt)/FRAMES)
        # Encontramos la posición para la cual la Magnitud de FFT es máxim
        Posm = np.where(M_gk == np.max(M_gk))[0][0]
        F_fund = F[Posm]
        # agrego data a la cola
        if F_fund >= tolerancia:
            #print("Señal : ",F_fund, "amp : ",max(M_gk))
            cola.put([F_fund,max(M_gk)])
        cont = cont + 1
# funcion de recoleccion de informacion de frecuencias de sonido


def freqasign(delayint, cola):
    global newfreq, estado
    matpress = "nada"
    # Funcion que se encarga de eliminar la informacion erronea del mic al inciar
    basura = [cola.get()]
    for a in range(10):
        basura = basura + [cola.get()]
    noise_flr = noise_floor(50)
    ##############################################################################
    newfreq = [cola.get()]
    while True:
        if is_pressed("p"):
            matpress = "plastico"
        if is_pressed("m"):
            matpress = "metal"
        if is_pressed("e"):
            matpress = "envoltorio"
        if is_pressed("c"):
            matpress = "carton"
        newfreq = []
        ampfreq = []
        # if GPIO.input(sensor_2) == 0:
        if is_pressed("d"):
            print("objeto detectado por alguno de los dos sensores")
            sleep(.5)
            for a in range(delayint):
                # retira inf. de la cola (pero la ultima inf. que se agrego porque es una cola de tipo lifo)
                data = cola.get()
                print("data de la cola: ", data)
                print("...")
                newfreq.append(data)
                print("entonces: freq: ",newfreq,)
                if a >= (delayint - 1):
                    print("entrando a limpiadora general ", newfreq)
                    matnom = limpiadora_general(newfreq,noise_flr)
                    if matpress == "nada":
                        print("__Por Favor Presione un Boton__")
                    else:
                        if matnom == matpress:
                            print("!!__CORRECTO__!!")
                            print("__Concidencia de material__")
                            print("__El material Ingresado si es un",matnom,"__")
                        else:
                            print("!!__ERRONEO__!!")
                            print("__No hay concidencia de material__")
                            print("__El Material Ingresado es un",matnom,"no un",matpress,"__")
            runmqtt()
        sleep(1)

#delayint=int(input("Cantidad de mustras por toma?:  "))
delayint = 5
mdo_asign = False
print("Inicializando escaneo con", delayint, "muestras por segundo.......")
# Designa los diferentes threads
fft_c = threading.Thread(target=calculadorafft, args=(cola,))
asignar = threading.Thread(target=freqasign, args=(delayint, cola,))
# inicia los threads
fft_c.start()
asignar.start()