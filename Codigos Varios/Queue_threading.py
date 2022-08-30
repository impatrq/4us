# import numpy as np
# import scipy.fftpack as fourier
# import matplotlib.pyplot as plt
# import matplotlib
# import pyaudio as pa 
# import struct
# import threading
# import queue

#### La forma de abajo una menos espacio visual y hace lo mismo que las 8 lineas de arrbia
import numpy as np,scipy.fftpack as fourier,matplotlib.pyplot as plt,matplotlib,pyaudio as pa,struct,threading,queue
from time import sleep

matplotlib.use('TkAgg')

delay = 5

FRAMES = 1024*8                                   # Tamaño del paquete a procesar
FORMAT = pa.paInt16                               # Formato de lectura INT 16 bits
CHANNELS = 1
Fs = 44100                                        # Frecuencia de muestreo típica para audio

cola = queue.Queue()

p = pa.PyAudio()


def calculadorafft():
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
        print(F_fund)
        return(F_fund)

#### Aplicar threading para que continue el calculo de fundamentales al mismo tiempor que se asignan dentro de la lista
def freqasign(delay,F_fund):    
    newfreq = [F_fund]
    for a in range(delay):
        print ("...")
        newfreq = newfreq+[F_fund]
        sleep(1)
    print("freq asignadas, calculando datos importantes....")
    pass
    print(newfreq)
    print("accion completada con exito")
delayint=int(input("Delay__?:  "))
fft_c = threading.Thread(target=calculadorafft)
asignar = threading.Thread(target=freqasign, args=(delay,F_fund))








    #freqasign(int(input("delay? : ")))
    # if ent == "asignar":
    #     newfreq = [F_fund]
    #     newfreq = newfreq + [F_fund]
    #     sleep(5)
    #     print ("nueva asignacion,    :",newfreq)