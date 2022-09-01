# Esta version esta incompleta y es una demo
# El display oled de servicio tiene que mostrar una representacion visual
#   del analisis de espectro previo a los calculos de iden de materiales
#   para que en el caso de un error, sea mas facil identificar el origen 

# Este codigo es APB, Asi que por favor, antes de preguntar... 
#               Lean los comentarios :)

#       Fede

########################################################################


from #machine import Pin, I2C, ADC # Importa las librerias nesesarias para usar los pines gipo(general purpuose input output.. se explica solo), I2c para el oled, y Adc para convertir la entrada analogica del micro en digital
from time import sleep # importa algo parecido a un "delay" de arduino
import #ssd1306 #libreria que controla las direcciones de i2c para el oled
import time

#led = Pin(16, Pin.OUT) #declara una salida gpio como output, no se usa actualmente
uno = 0
dos = 0
tiempo = 0

# using default address 0x3C     #Cosas nesesarias del oled, declara pines, resolucion y protocolo de com
#i2c = I2C(sda=Pin(4), scl=Pin(5))
#display = ssd1306.SSD1306_I2C(128, 64, i2c)

# config del adc del micro
#mic = ADC(0) 
#declara la variable mic como la entrada de adc en el pin 0

while True: #Loop que grafica
    tiempo = tiempo + 1 #una variable contador que va aumentando su valor periodicamente
    if tiempo >= 120: #reseteo la variable para que no tenga un valor mayor a la resolucion del oled
        tiempo = 0 
        #display.fill(0) #pongo el oled en negro
    #algo = int(mic.read()/10)#lee la entrada de adc, la divide por 10, y lo conviente en un int
 #Mas adelante uso "algo" como una coordenada a graficar, por eso no puede tener coma y es un int

    #print(algo) #comprobacion por computadora de que funciona
    #display.text("Entrada de Mic",0,0,1)
    #display.fill_rect(1,16,1,48,7) # dibuja las lineas del grafico, son coordenadas cartesianas
    #display.fill_rect(2,62,120,2,2)
    #display.fill_rect(tiempo,algo,1,1,1) # Usa "tiempo" como x y "algo" como y
    # Como "tiempo" va incrementando, el grafico se mueve y "algo" oscila en y
    sleep(.01)
    #display.show() # Muestra todos los comandos de arriba en el oled, sin eso no muestra nada


    ######################################################################
    #               Codigo Basura pero "Util"
    ######################################################################
    
    #display.fill(0)
#display.fill_rect(0, 0, 32, 32, 1)
#display.fill_rect(2, 2, 28, 28, 0)
#display.vline(9, 8, 22, 1)
#display.vline(16, 2, 22, 1)
#display.vline(23, 8, 22, 1)
#display.fill_rect(26, 24, 2, 4, 1)
#display.text('me pica', 40, 0, 1)
#display.text('el rinion', 40, 12, 1)
#display.text("ADC: {}".format(mic.read()), 10, 24, 1)
#display.text(' ',40,36,1)
#display.text(' ',40,48,1)
#display.show()
#while True:

    #display.fill(0)
    #display.text("Entrada = {}".format(mic.read()),10,24,1)
    #display.show()
    #sleep(.1)
    #print("Bucle")

# while True:
#     uno = uno +1
#     dos = dos +1
#     if dos >=60:
#         dos = 0
#         print("some",dos)
#     display.fill_rect(1,16,1,48,7)
#     display.fill_rect(2,62,120,2,2)
#     display.fill_rect(mic.read(),20,20,20,20)
#     display.text("Espectro de freq",0,0,1)
#     display.fill_rect((uno),(micro),20,20,1)
#     sleep(.0001)
#     display.show()