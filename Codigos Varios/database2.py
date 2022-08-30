import csv
database = [
{"tipo":"metal", "freqmic":0000, "freqcap":0000, "valamp":0000}
,{"tipo":"plastico", "freqmic":0000, "freqcap":0000, "valamp":0000}
,{"tipo":"carton", "freqmic":0000, "freqcap":0000, "valamp":0000}
,{"tipo":"papel", "freqmic":0000, "freqcap":0000, "valamp":0000}
]
indices = ["tipo","freqmic","freqcap","valamp"] ### asigana los nombres de cada dato
csv_file = "dartabase.csv"
entradapostFourier = 99999 ### Valores temporales, falta la incorporacion al resto del programa (datos de los sensores)
capacitivo = 88888
amplitud = 5555
####### Definicion de funciones ###########

##### Funcion asignadora: guarda los datos en el diccionario de forma ordenada ####
def asigandora(nombre,freqmic,freqcap,valamp):
    database = database + [{"tipo":nombre, "freqmic":freqmic, "freqcap":freqcap, "valamp":valamp}]
##### Funcion creadora: Pide la entrada de datos para la clase asignadora ####
def creadora():
    nombre=str(input("Nombre del material a cargar? :  "))
    freqmic=entradapostFourier
    freqcap=capacitivo
    valamp = amplitud
    print("Valores asignados, clase creada ")
    return(nombre,freqmic,freqcap,valamp)
##### Funcion almacenadora: Guarda los datos del diccionario en el csv para formar la base de datos ####
def almacenadora():
    try:
        with open(csv_file,"w") as file:
            writer = csv.DictWriter(file, fieldnames = indices)
            writer.writeheader()
            for data in database:
                writer.writerow(data)
    except IOError:
        print("I/O error")

print("Base de datos hasta el momento :    ",database)
# datos = [{"tipo":"sucutrulo", "freqmic":7777, "freqcap":7777, "valamp":7777}]
# database = database + datos
# print("2 : ",database)
def lectora():
    # terminar lectora (borrar pass por si alguien mas lo revisa, jajjaja que iluso)
    pass