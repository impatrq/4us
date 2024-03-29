#################################################################################################################

#                   Version a terminar // deteccion de materiales en base a una referencia
#                   Falta implementar base de datos csv y refinar la tolerancia del algoritmo

##############################################################################################################
#                    Todos los parametros para las funciones se pasan en el siguiente formato
#                               (nombre,freq_mic,val_ind,freq_cap)
################################################################################################################
from turtle import delay
from sortedcollections import SortedList
import numpy as np,scipy.fftpack as fourier,matplotlib.pyplot as plt,matplotlib,pyaudio as pa,struct,threading,queue,csv
from time import sleep
#import RPi.GPIO as gpio    Descomentar para la version de raspberry
import serial

ref = [["metal",[1450.00,1500.00,1600.00,2000.00,3000.00]],["plastico",[1200.00,1300.00,1350.00]],["aire",[200,300,100]]]

matplotlib.use('TkAgg')

FRAMES = 1024*8                                   # Tamaño del paquete a procesar
FORMAT = pa.paInt16                               # Formato de lectura INT 16 bits
CHANNELS = 1
Fs = 44100                                        # Frecuencia de muestreo típica para audio

##### Asignaciones de la base de datos csv #####
database =[]
indices = ["tipo","freqmic","freqcap","valamp"]   # asigana los nombres de cada dato
csv_file = "dartabase.csv"
capacitivo = 88888 # Valor temporal (a reemplazar)
amplitud = 5555    # Valor temporal (a reemplazar)

# creo una queue de tipo last in first out
cola = queue.LifoQueue()

p = pa.PyAudio()

ser = serial.Serial("/dev/serial0", 9600)

##### Funcion que limpia la entrada de datos y detecta el tipo de material
def limpiadora_general(a_limpiar,ref):
    filtrado =[]
    finales = []
    limpio=[]
    a_limpiar = SortedList(a_limpiar)
    ref = SortedList(ref)
    for b in range(len(ref)):
        nom = ref[b][0]
        espref = ref[b][1]
        for c in range(len(a_limpiar)):
            limpio = list(a_limpiar.irange(0.65 * int(espref[1]), 1.55 * int(espref[1])))
            filtrado.append(limpio)
            limpio = [*set(limpio)]
        if len(limpio):
            #print("vale algo :",limpio," y es un ",nom)
            finales.append([limpio,nom])
            if nom != "aire":
                print("el material es un: ",nom," y vale :",limpio)
                if mdo_asign == True:
                    print("asignando datos....")
                    asignadora(nom,limpio,0,0)
                    return(0)
            else:
                print("no hay un material con freq importante")
    #print("filtrado terminado: ",finales)
#### Funcion Limpiadora: obtiene unicamente la informacion importante de todo el ruido ambiente
def limpiadora(a_limpiar,ref):
    filtrado =[]
    a_limpiar = SortedList(a_limpiar)
    ref = SortedList(ref)
    nom = input("material a comparar: ")
    for a in range(len(ref)):
        if ref[a][0] == nom:
            print("coincidencia: ",ref[a][0])
            espref = ref[a][1]
            print("Ahora espref vale: ",ref[a][1])
    for c in range(len(a_limpiar)):
        limpio = list(a_limpiar.irange(0.65 * int(espref[1]), 1.55 * int(espref[1])))
        ### Falta ajustar la tolerancia para ponerlo a punto
        filtrado.append(limpio)
        limpio = [*set(limpio)]
    set(limpio)
    print("filtrado terminado: ",limpio)

##### Funcion creadora: Pide la entrada de datos para la clase asignadora ####
def creadora(): #1
    nombre=str(input("Nombre del material a cargar? :  "))
    freq_mic = newfreq
    freq_cap = 1234 #agarrar el valor de diferencia de capacitancia directo de la pico
    val_ind = 1 #agarrar el valor del sensor inductivo directo de la pico
    print("Valores asignados, clase creada ")
    return(nombre,freq_mic,val_ind,freq_cap)
##### Funcion asignadora: guarda los datos en el diccionario de forma ordenada ####
def asignadora(nombre,freq_mic,val_ind,freq_cap):#2
    formated = [{"tipo":nombre, "freq_mic":freq_mic, "val_ind":freq_cap, "val_ind":val_ind}]
    almacenadora(formated)
    return
##### Funcion almacenadora: Guarda los datos del diccionario en el csv para formar la base de datos ####
def almacenadora(formated):#3
    try:
        with open(csv_file,"w") as file:
            writer = csv.DictWriter(file, fieldnames = indices)
            writer.writeheader()
            for data in formated:
                writer.writerow(data)
                print("data guardada")
    except IOError:
        print("I/O error")
###### Funcion lectora: Lee los datos directo de la base de datos
def lectora():
    with open(csv_file, newline="") as File:
        print("inicio de lectura")
        lectura = csv.reader(File)
        for row in lectura:
            print(row)

#funcion de calculos fft (magnitud de frecuencia y amplitud)
def calculadorafft(cola):
    stream = p.open(                                  # Abrimos el canal de audio con los parámeteros de configuración
    format = FORMAT,
    channels = CHANNELS,
    rate = Fs,
    input=True,
    output=True,
    frames_per_buffer=FRAMES
    )
    while True:
        F = (Fs/FRAMES)*np.arange(0,FRAMES//2)                 # Creamos el vector de frecuencia para encontrar la frecuencia dominante
        data = stream.read(FRAMES)
        dataInt = struct.unpack(str(FRAMES) + 'h', data)
        M_gk = abs(fourier.fft(dataInt)/FRAMES)
        Posm = np.where(M_gk == np.max(M_gk))[0][0]           # Encontramos la posición para la cual la Magnitud de FFT es máxim
        F_fund = F[Posm]
        #agrego data a la cola
        cola.put(F_fund)
# funcion de recoleccion de informacion de frecuencias de sonido
def freqasign(delayint,cola):
    global newfreq
    # Funcion que se encarga de eliminar la informacion erronea del mic al inciar
    basura = [cola.get()]
    for a in range(5):
        basura = basura + [cola.get()]
    ##############################################################################
    newfreq = [cola.get()]
    while True:
        newfreq = []
        for a in range(delayint):
            #retira inf. de la cola (pero la ultima inf. que se agrego porque es una cola de tipo lifo)
            data = cola.get()
            print("data de la cola: ",data)
            print("...")
            newfreq = newfreq + [data]
        z = limpiadora_general(newfreq,ref)
def escucha():
    while 1 :
        sleep(10)
        message ='''
        {
        "type" : "metal",
        "frequency" : [283,345,234,465],
        "is_metal" : 0,
        "capacitivo" : 93485793580
        }
        '''
    print(message)
    ser.write(message.encode(encoding='UTF-8'))

    print("accion completada con exito")
delayint=int(input("Cantidad de mustras por toma?:  "))
mdo_asign = str(input("Desea hacer una asignacion? (S/N): "))
if mdo_asign.lower() == "s":
    mdo_asign = True
    print("Esperando asignacion.....")
else:
    mdo_asign = False
    print("Asignacion cancelada ")
print("Inicializando escaneo con",delayint,"muestras por segundo.......")
# Designa los diferentes threads
fft_c = threading.Thread(target=calculadorafft, args=(cola,))
asignar = threading.Thread(target=freqasign, args=(delayint,cola,))
# inicia los threads
fft_c.start()
asignar.start()