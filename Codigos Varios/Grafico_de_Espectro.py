#################################################################################################################

#                   Clon del main V2 //[ WIP ]// Solucion del problema del grafico y valores de amplitud

##############################################################################################################
import numpy as np
import scipy.fftpack as fourier
import matplotlib.pyplot as plt
import matplotlib
import pyaudio as pa 
import struct
from time import sleep
matplotlib.use('TkAgg')

delay = 5

FRAMES = 1024*8                                   # Tamaño del paquete a procesar
FORMAT = pa.paInt16                               # Formato de lectura INT 16 bits
CHANNELS = 1
Fs = 44100                                        # Frecuencia de muestreo típica para audio

p = pa.PyAudio()

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
    gk = fourier.fft(dataInt)
    Ma_gk = abs(gk)
    Fua = Fs+np.arange(0,len(dataInt))/len(dataInt)
    Posm = np.where(M_gk == np.max(M_gk))[0][0]           # Encontramos la posición para la cual la Magnitud de FFT es máxim
    F_fund = F[Posm]

    plt.plot(Fua, Ma_gk)
    plt.xlabel('Frecuencia (Hz)', fontsize='14')
    plt.ylabel('Amplitud FFT', fontsize='14')
    plt.show()
    print(F_fund)
    def freqasign(delay):    
        newfreq = [F_fund]
        for a in range(delay):
            print ("...")
            newfreq = newfreq+[F_fund]
            sleep(1)
        print("freq asignadas, calculando datos importantes....")
        pass
        print(newfreq)
        print("accion completada con exito")
