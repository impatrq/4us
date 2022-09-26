####################################################################################

#               Esta es la primera version del "main" del esp 8266
#               Falta intergrar el protocolo de comunicacion UART junto
#               con el de la raspberry, mejorar la interfaz grafica 
#               y agregar funcionalidades extra

#                                                               Fede Aranda

#####################################################################################
from machine import Pin,I2C,ADC, UART
### Serial no sirve aca, va a tener que ser por uart
from time import sleep
import ssd1306
up = Pin(02,Pin.IN,Pin.PULL_UP)
dw = Pin(14,Pin.IN,Pin.PULL_UP)
ok = Pin(00,Pin.IN,Pin.PULL_UP)
ind = Pin(12,Pin.IN,Pin.PULL_UP)
sensamp = ADC(0)

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
def start_up():
    display.fill(0)
    display.text("4us",50,20,1)
    display.text("Proyect",35,30,1)
    display.text("Running - v1",0,50,1)
    display.show()
def detect_metales():
    while True:
        display.fill(0)
        display.text("Metales",50,20,1)
        if up.value() == False:
            return
        if ind():
            display.text("no",40,30,1)
        else:
            display.text("si",40,30,1)
        display.show()
def sens_amp():
    while True:
        display.fill(0)
        display.text("Amplitud",50,20,1)
        if up.value() == False:
            return
        amp = str(sensamp.read()/10)
        display.text(amp,40,30,1)
        display.show()
def cayo_algo():
    amp = int(sensamp.read()/10)
    normal = amp
    calculado = normal*1.0050
    cant = 0
    while True:
        amp = int(sensamp.read()/10)
        display.fill(0)
        if amp >= calculado:
            display.text("cayo algo",0,20,1)
            cant = cant+1
        else:
            amp = str(amp)
            display.text("nada",0,20,1)
            display.text(amp,40,20,1)
        if cant > 0:
            strant = str(cant)
            display.text("cayeron    cosas",0,40,1)
            display.text(strant,67,40,1)
        display.show()
        if up.value() == False:
            return
def cayo_metal():
    amp = int(sensamp.read()/10)
    normal = amp
    calculado = normal*1.0050
    cant = 0
    while True:
        amp = int(sensamp.read()/10)
        display.fill(0)
        if amp >= calculado and ind.value() == False:
            display.text("cayo algo",0,20,1)
            cant = cant+1
        else:
            amp = str(amp)
            display.text("nada",0,20,1)
            display.text(amp,40,20,1)
        if cant > 0:
            strant = str(cant)
            display.text("cayeron    metales",0,40,1)
            display.text(strant,67,40,1)
        display.show()
        if up.value() == False:
            return
def comunicar():
    # esta es la funcion sobre la que hay que implementar la com.
    display.fill(0)
    display.text("Enviando...",0,20,1)
    display.show()
    sleep(2)
    return
def main_menu():
    cont = 0
    while True:
        if up.value() == True:
            cont = cont+10
        if dw.value() == True:
            cont = cont-10
        if ok.value() == False:
            if cont == 0:
                detect_metales()
            if cont == 10:
                sens_amp()
            if cont == 20:
                cayo_algo()
            if cont == 30:
                cayo_metal()
            if cont == 40:
                comunicar()
        display.fill(0)
        display.text(">",0,cont,3)
        display.text("_ Sens. Ind.",12,0,1)
        display.text("_ Sens. Amp.",12,10,1)
        display.text("_ Cayo algo?",12,20,1)
        display.text("_ Cayo metal?",12,30,1)
        display.text("_ Comunicar",12,40,1)
        display.show()
start_up()
sleep(2)
main_menu()

