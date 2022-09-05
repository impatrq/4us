#################################################################################################################

#       Esta version implementa multithreading y soluciona el problema de la recoleccion de inf.
#       Tambien implementa el uso de queue para el traspaso seguro de inf. entre threads

##############################################################################################################

import numpy as np,scipy.fftpack as fourier,matplotlib.pyplot as plt,matplotlib,pyaudio as pa,struct,threading,queue
from time import sleep

matplotlib.use('TkAgg')

FRAMES = 1024*8                                   # Tamaño del paquete a procesar
FORMAT = pa.paInt16                               # Formato de lectura INT 16 bits
CHANNELS = 1
Fs = 44100                                        # Frecuencia de muestreo típica para audio
# creo una queue de tipo last in first out
cola = queue.LifoQueue()

p = pa.PyAudio()

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
        print(F_fund)
# funcion de recoleccion de informacion de frecuencias de sonido
def freqasign(delayint,cola):
    sleep(delayint)
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
        newfreq = newfreq + [data]    
    print("freq asignadas, calculando datos importantes....")
    pass
    print(newfreq)
    print("accion completada con exito")
delayint=int(input("Delay__?:  "))
print(delayint)
# Designa los diferentes threads
fft_c = threading.Thread(target=calculadorafft, args=(cola,))
asignar = threading.Thread(target=freqasign, args=(delayint,cola,))
# inicia los threads
fft_c.start()
asignar.start()