from CacheCorresp import CacheCorresp

puntos=True
#for tipo in [1]:
for tipo in range(0,4):
    CC = CacheCorresp(tipo)
    for i in range(0, CC.n - 1):
        #print("(", CC.get_tt(), "-", CC.get_cc(), ")", end =" ")
        if puntos and i % 100 == 0:
            print(".", end ="")
        for j in range(i + 1, CC.n):
            if CC.leer(i) > CC.leer(j):
                temp = CC.leer(i)
                CC.escribir(i, CC.leer(j))
                CC.escribir(j, temp)
        if not puntos:
            print(tipo,i, CC.get_tt())
    if puntos:
        print(tipo, CC.get_tt())
