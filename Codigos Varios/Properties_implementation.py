#################################################################################################################

#                   Version a terminar // implementacion de base de datos csv // 

##############################################################################################################

import numpy as np,scipy.fftpack as fourier,matplotlib.pyplot as plt,matplotlib,pyaudio as pa,struct,threading,queue,csv
from time import sleep

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
##### Funcion creadora: Pide la entrada de datos para la clase asignadora ####
def lectora():
    with open(csv_file, newline="") as File:
        print("inicio de lectura")
        lectura = csv.reader(File)
        global tmateriales
        tmateriales = []
        try:
            for row in lectura:
                print(row[0])
                tmateriales.append(str(row[0]))
        except:
            print("final de lista")
            print("tipos de materiales: ",tmateriales)
        return tmateriales
def lectora_de_datos(nombre):
    with open(csv_file, newline="") as File:
        lectura=list(csv.reader(File))
        for row in lectura:
            print("...")
            if row[0] == nombre:
                print("esta :",row[0])
                return row
            else: pass

def recalculadora(row2):
    with open(csv_file, newline="") as File:
        lectura = csv.reader(File)
        csvdata = []
        for row in lectura:
            print("...")
            if row[0] == nombre:
                recalc = row
            else:
                print(row[0])
                csvdata.append(row)
        #### Pensar bien el algoritmo que elimina la basura
        finrecalc = newfreq + recalc
        len(recalc)
        for a in range(len(recalc[1])):
##### Funcion asignadora: guarda los datos en el diccionario de forma ordenada ####
def asignadora():#2
    global database
    database = database + [{"tipo":nombre, "freqmic":freqmic, "freqcap":freqcap, "valamp":valamp}]
##### Funcion almacenadora: Guarda los datos del diccionario en el csv para formar la base de datos ####
def almacenadora():#3
    try:
        with open(csv_file,"a") as file:
            writer = csv.DictWriter(file, fieldnames = indices)
            writer.writeheader()
            for data in database:
                writer.writerow(data)
                print("data guardada")
    except IOError:
        print("Error al abrir.... X ")
###### Funcion lectora: Lee los datos directo de la base de datos
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
        #print(F_fund)
# funcion de recoleccion de informacion de frecuencias de sonido
def freqasign(delayint,cola):
    sleep(delayint)
    global newfreq
    # Funcion que se encarga de eliminar la informacion erronea del mic al inciar
    basura = [cola.get()]
    for a in range(5):
        basura = basura + [cola.get()]
    ##############################################################################
    newfreq = [cola.get()]
    for a in range(delayint):
        #retira inf. de la cola (pero la ultima inf. que se agrego porque es una cola de tipo lifo)
        data = cola.get()
        print("...")
        global newfreq
        newfreq = newfreq + [data]    
    print("freq asignadas, calculando datos importantes....")
    pass
    print(newfreq)
    #creadora()
    #asignadora()
    #almacenadora()
    print("accion completada con exito")
delayint=int(input("Delay__?:  "))
print(delayint)

def creadora(tlista): #1
    print(tlista)
    global freqmic,freqcap,valamp,nombre
    nombre=str(input("Nombre del material a cargar? :  "))
    if nombre in tlista:
        while True:
            preg = input("El material ya existe, asignar nuevos valores? : (S/N)")
            preg.lower()
            if preg == "s":
                lecesp = lectora_de_datos(nombre)
                #freqmic2 = (lecesp[1] + newfreq)
                print(lecesp)
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                freqmic = newfreq
                freqcap = capacitivo
                valamp = amplitud
                break
            if preg == "n":
                print("Accion rechazada.. ")
                break
            else:
                print("Entrada no valida ")
    print("Valores asignados, clase creada ")

# Designa los diferentes threads
fft_c = threading.Thread(target=calculadorafft, args=(cola,))
asignar = threading.Thread(target=freqasign, args=(delayint,cola,))
# inicia los threads
fft_c.start()
asignar.start()
tlista = lectora()
print(tlista)
creadora(tlista)