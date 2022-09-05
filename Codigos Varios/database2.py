import csv
database =[]
indices = ["tipo","freqmic","freqcap","valamp"] ### asigana los nombres de cada dato
csv_file = "dartabase.csv"
entradapostFourier = 99999 ### Valores temporales, falta la incorporacion al resto del programa (datos de los sensores)
capacitivo = 88888
amplitud = 5555
####### Definicion de funciones ###########

##### Funcion asignadora: guarda los datos en el diccionario de forma ordenada ####
def asignadora():#2
    global database
    database = database + [{"tipo":nombre, "freqmic":freqmic, "freqcap":freqcap, "valamp":valamp}]
##### Funcion creadora: Pide la entrada de datos para la clase asignadora ####
def creadora(): #1
    global freqmic,freqcap,valamp,nombre
    nombre=str(input("Nombre del material a cargar? :  "))
    freqmic=entradapostFourier
    freqcap=capacitivo
    valamp = amplitud
    print("Valores asignados, clase creada ")
    print(nombre,freqmic,freqcap,valamp)
    return(nombre,freqmic,freqcap,valamp)
##### Funcion almacenadora: Guarda los datos del diccionario en el csv para formar la base de datos ####
def almacenadora():#3
    try:
        with open(csv_file,"w") as file:
            writer = csv.DictWriter(file, fieldnames = indices)
            writer.writeheader()
            for data in database:
                writer.writerow(data)
                print("data guardada")
    except IOError:
        print("I/O error")
print("Base de datos hasta el momento :    ",database)
def lectora():
    with open(csv_file, newline="") as File:
        print("inicio de lectura")
        lectura = csv.reader(File)
        for row in lectura:
            print(row)
creadora()
asignadora()
almacenadora()

