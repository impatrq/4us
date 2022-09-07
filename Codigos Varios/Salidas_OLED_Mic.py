import numpy as np
import scipy.fftpack as fourier
import matplotlib.pyplot as plt
import matplotlib
import pyaudio as pa 
import struct
from time import sleep
from #machine import Pin, I2C, ADC # Importa las librerias nesesarias para usar los pines gipo(general purpuose input output.. se explica solo), I2c para el oled, y Adc para convertir la entrada analogica del micro en digital
from time import sleep # importa algo parecido a un "delay" de arduino
import #ssd1306 #libreria que controla las direcciones de i2c para el oled

# using default address 0x3C     #Cosas nesesarias del oled, declara pines, resolucion y protocolo de com
#i2c = I2C(sda=Pin(4), scl=Pin(5))
#display = ssd1306.SSD1306_I2C(128, 64, i2c)

#led = Pin(16, Pin.OUT) #declara una salida gpio como output, no se usa actualmente
tiempo = 0

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
    Posm = np.where(M_gk == np.max(M_gk))[0][0]           # Encontramos la posición para la cual la Magnitud de FFT es máxim
    F_fund = F[Posm]
    print(F_fund)

    tiempo = tiempo + 1 #una variable contador que va aumentando su valor periodicamente
    if tiempo >= 120: #reseteo la variable para que no tenga un valor mayor a la resolucion del oled
        tiempo = 0 
        #display.fill(0) #pongo el oled en negro

    #display.text("Entrada de Mic",0,0,1)
    #display.fill_rect(1,16,1,48,7) # dibuja las lineas del grafico, son coordenadas cartesianas
    #display.fill_rect(2,62,120,2,2)
    #display.fill_rect(tiempo,newfreq,1,1,1) # Usa "tiempo" como x y "newfreq" como y
    # Como "tiempo" va incrementando, el grafico se mueve y "algo" oscila en y
    sleep(.01)
    #display.show() # Muestra todos los comandos de arriba en el oled, sin eso no muestra nada

    #### Aplicar threading para que continue el calculo de fundamentales al mismo tiempor que se asignan dentro de la lista
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

#No garantizo que funcione, quiero probar como se comporta ya que es la fusion de dos codigos, del Mic_Grafico... y 4us_main V2