from sortedcollections import SortedList
lec1 = ["metal",[220.71533203125, 1428.857421875, 1578.857421875, 904.39453125, 1628.857421875, 2901.59912109375],88888,5555]
lec2 = ["metal",[300.54,1560.32324,200.785,400.7438,1600.455,600.458]]
#ref = ["metal",[1445.345,1679.324,1523.675]]
lec3 =["plastico 2",[1367.3583984375, 1372.74169921875, 1388.8916015625, 1458.87451171875, 1458.87451171875, 1383.50830078125]]
ref = [["metal",[1450.00,1500.00,1600.00]],["plastico",[1200.00,1300.00,1350.00]],["aire",[200,300,100]]]
purga = []
list1 =[]
list2=[]
filtrado = []
ruido = 500
for a in range(len(lec1[1])):
    if lec1[1][a] >= 300:
        # se considera que no es ruido ambiente
        purga.append(lec1[1][a])
print(purga)
purga = SortedList(purga)
sinpurga2 = SortedList(lec2[1])
#####################################################################################
nom = input("material a comparar: ")
for a in range(len(ref)):
    if ref[a][0] == nom:
        print("coincidencia: ",ref[a][0])
        espref = ref[a][1]
        print("Ahora espref vale: ",ref[a][1])
for c in range(len(sinpurga2)):
    prueba3 = list(sinpurga2.irange(0.65 * int(espref[1]), 1.55 * int(espref[1])))
    filtrado.append(prueba3)
    prueba3 = [*set(prueba3)]
    print("filtrado : ",filtrado)
set(prueba3)
print("filtrado terminado: ",prueba3)





######################################################################################3
#print("lista1 vale: ",list1)
#print("lista2 vale: ",list2)
for c,d in enumerate(list1):
    pass
# freqpredom = []
# tolerancia = 0.05
# for a in range(len(lec1[1])):
#     if lec1[1][a] >= 300:
#         purga.append(int(lec1[1][a]))
# for b in range(len(purga)):
#     up = purga[b]+tolerancia
#     dwn = purga[b]-tolerancia
# any_found = any(item*dwn >= purga[b] <= item * up for item in purga)
# print(any_found)
# print ("yes" if any_found else "no")