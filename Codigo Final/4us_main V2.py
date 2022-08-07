import numpy as np
import scipy.fftpack as fourier
import matplotlib.pyplot as plt
import matplotlib
import pyaudio as pa 
import struct
matplotlib.use('TkAgg')

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
    Posm = np.where(M_gk == np.max(M_gk))[0][0]           # Encontramos la posición para la cual la Magnitud de FFT es máxim
    F_fund = F[Posm]
    print(F_fund)
