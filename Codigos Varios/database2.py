import csv
database =[]
indices = ["tipo","freqmic","freqcap","valamp"] ### asigana los nombres de cada dato
csv_file = "database.csv"
entradapostFourier = 99999 ### Valores temporales, falta la incorporacion al resto del programa (datos de los sensores)
capacitivo = 88888
amplitud = 5555
####### Definicion de funciones ###########

##### Funcion asignadora: guarda los datos en el diccionario de forma ordenada ####
def asignadora():#2
    global database
    database = {"tipo":nombre, "freqmic":freqmic, "freqcap":freqcap, "valamp":valamp}
    return (database)
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
def almacenadora(goto):#3
    cont = 0
    try:
        with open(csv_file,"w") as file:
            writer = csv.DictWriter(file, fieldnames = indices)
            #writer.writeheader() deberia arreglar esto pero ya es muy tarde, asi funciona y punto
            print("          ")
            for data in goto:
                cont = cont +1
                print("data a cargar ",goto[str(cont+1)])
                if goto[str(cont+1)] != ['tipo', 'freqmic', 'freqcap', 'valamp']:
                    writer.writerow(goto[str(cont+1)])
                    print("data guardada")
                else:
                    print("excepcion de header")
    except IOError:
        print("I/O error")
def sup_lectora(goto_database):
    cont = 0
    upto_database = {}
    with open(csv_file, newline="") as File:
        print("inicio de lectura")
        lectura = csv.reader(File)
        for row in lectura:
            cont = cont+1
            row = {'tipo': row[0], 'freqmic': row[1], 'freqcap': row[2], 'valamp': row[3]}
            upto_database[str(cont+1)] = row
        upto_database[str(cont+2)] = goto_database
        return(upto_database)
z = sup_lectora(123)
creadora()
z1 = asignadora()
z2 = sup_lectora(z1)
almacenadora(z2)

