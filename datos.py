f = open('datos.txt','r')
valores = f.read().split()
for i, v in enumerate(valores):
     valores[i] = int(v)
f.close()
