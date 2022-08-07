import csv
print("inicio de programa")
materiales = {}
def newmat ():
    new0 = len(materiales)+1
    new1 = str(input("Nombre del material: "))
    new2 = float(input("freq del material: "))
    new3 = {"tipo":new1,"freq":new2}
    materiales[new0] = new3
    return "nuevo material creado"
for a in range(10):
    if a == 0:
        a = 1
    newmat()
    print(materiales)
    preg = str(input("pregunta : "))
    for a,b in enumerate(materiales):
        if preg in materiales[b]["tipo"]:
            print("esta en materiales")
            ask = str(input("agregar nueva informacion de frecuencia? Y/N  "))
            while True:
                if ask == "y":
                    newfreq = float(input("nueva freq : "))
                    materiales[b]["freq"] = (materiales[b]["freq"] + newfreq)/2
                    print("frecuencias promediadas")
                    print("freq de metal : ",materiales[b]["freq"])
                    break
                if ask == "n":
                    print("operacion rechazada")
                    break
                else :
                    print("entrada no es correcta")
        if preg not in materiales[b]["tipo"]:
            print("no esta en materiales")