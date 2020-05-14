f = open('datos.txt','r')
valores = f.read()
valores = valores.split()
for i in range(0, len(valores)):
    valores[i] = int(valores[i])

tt=0
cc=0
K = 8            # Tamano del bloque
k = 4            # Lineas por conjunto
cachesize = 64   # en bytes
m = int(cachesize / K)
conjuntos = int(m / k)
it=0
ia=0
ib=0
ic=0
id=0

def asocestaen(ed):
    for i in range(m):
        if valida[i]:
            if etiqueta[i]==ed:
                return i
    return -1

def asocnovalida():
    for i in range(m):
        if valida[i]==False:
            return i
    return -1


def asoccestaen(cd,ed):
    for i in range(cd*k,cd*k+k):
      if valida[i]:
          if etiqueta[i]==ed:
              return i
    return -1

def asoccnovalida(cd):
    for i in range(cd*k,cd*k+k):
        if valida[i]==False:
            return i
    return -1



def leere(i,tipo):
    global tt, cc
    global valida
    global modificada,nextlinea,it,ia,ib,ic,id

    #print("work:", work)
    if tipo==0:
        tt=tt+0.1
        cc=cc+1
        return work[i]
    if tipo==1:
        bd=i / K
        ld=int(bd % m)
        ed=bd / m
        if valida[ld]:
            if etiqueta[ld]==ed:
                tt=tt+0.01
                cc=cc+1
                return work[i]
            if modificada[ld]:
                tt=tt+0.22
                cc=cc+1
                etiqueta[ld]=ed
                modificada[ld]=False
                return work[i]
            tt=tt+0.11
            cc=cc+1
            etiqueta[ld]=ed
            modificada[ld]=False
            return work[i]
        tt=tt+0.11
        cc=cc+1
        etiqueta[ld]=ed
        modificada[ld]=False
        valida[ld]=True;
        return work[i]
    if tipo==2:
        bd=i/K
        ed=bd
        estaen=asocestaen(ed);
        if estaen>=0:
            tt=tt+0.01
            return work[i]
        nv=asocnovalida()
        if nv>=0:
            valida[nv]=True
            modificada[nv]=False
            etiqueta[nv]=ed
            tt=tt+0.11
            return work[i]
        if modificada[nextlinea]:
            tt=tt+0.22
            modificada[nextlinea]=False
            etiqueta[nextlinea]=ed;
            nextlinea=nextlinea+1;
            if nextlinea==m:
                nextlinea=0;
            return work[i]
        tt=tt+0.11
        modificada[nextlinea]=False
        etiqueta[nextlinea]=ed;
        nextlinea=nextlinea+1;
        if nextlinea==m:
            nextlinea=0;
        return work[i]
    if tipo==3:
        it=it+1
        bd=i / K
        cd=int(bd % conjuntos)
        ed=bd / conjuntos
        estaen=asoccestaen(cd,ed)
        if estaen>=0:
            ia=ia+1
            tt=tt+0.01
            return work[i];
        nv=asoccnovalida(cd)
        #if i==40:
        #    print "40=",nv,cd
        if nv>=0:
            ib=ib+1
            tt=tt+0.11
            modificada[nv]=False;
            valida[nv]=True
            etiqueta[nv]=ed
            return work[i];
        if modificada[nl[cd]]:
            ic=ic+1
            tt=tt+0.22
            modificada[nl[cd]]=False
            etiqueta[nl[cd]]=ed;
            nl[cd]=nl[cd]+1
            if nl[cd]%k==0:
                nl[cd]=k*cd;
            return work[i]
        id=id+1
        tt=tt+0.11
        modificada[nl[cd]]=False
        etiqueta[nl[cd]]=ed;
        nl[cd]=nl[cd]+1
        if nl[cd]%k==0:
            nl[cd]=k*cd;
        return work[i]

def leer(i,tipo):
    #if it<=100:
    #    print
    #    print i,it,ia,ib,ic,id
    return leere(i,tipo)
    #if it<100:
    #    print i,it,ia,ib,ic,id
    #    print





def escribir(i,tipo,valor):
    global tt, cc
    global valida
    global modificada,nextlinea
    if tipo==0:
        tt=tt+0.1;
        cc=cc+1
        work[i]=valor
        return
    if tipo==1:
        bd=i / K
        ld=int(bd % m)
        ed=bd / m
        if valida[ld]:
            if etiqueta[ld]==ed:
                tt=tt+0.01
                cc=cc+1
                modificada[ld]=True
                work[i]=valor
                return
            if modificada[ld]:
                tt=tt+0.22
                cc=cc+1
                etiqueta[ld]=ed
                modificada[ld]=True
                work[i]=valor
                return
            tt=tt+0.11
            cc=cc+1
            etiqueta[ld]=ed
            modificada[ld]=True
            work[i]=valor
            return
        tt=tt+0.11
        cc=cc+1
        etiqueta[ld]=ed
        modificada[ld]=True
        valida[ld]=True;
        work[i]=valor
        return
    if tipo==2:
        bd=i/K
        ed=bd
        estaen=asocestaen(ed);
        if estaen>=0:
            tt=tt+0.01
            modificada[estaen]=True;
            work[i]=valor
            return
        nv=asocnovalida()
        if nv>=0:
            valida[nv]=True
            modificada[nv]=True
            etiqueta[nv]=ed
            tt=tt+0.11
            work[i]=valor
            return
        if modificada[nextlinea]:
            tt=tt+0.22
            modificada[nextlinea]=True
            etiqueta[nextlinea]=ed;
            nextlinea=nextlinea+1;
            if nextlinea==m:
                nextlinea=0;
            work[i]=valor
            return
        tt=tt+0.11
        modificada[nextlinea]=True
        etiqueta[nextlinea]=ed;
        nextlinea=nextlinea+1;
        if nextlinea==m:
            nextlinea=0;
        work[i]=valor
        return
    if tipo==3:
        bd=i / K
        cd=int(bd % conjuntos)
        ed=bd / conjuntos
        estaen=asoccestaen(cd,ed)
        if estaen>=0:
            modificada[estaen]=True
            tt=tt+0.01
            work[i]=valor
            return
        nv=asoccnovalida(cd)
        if nv>=0:
            tt=tt+0.11
            modificada[nv]=True;
            valida[nv]=True
            etiqueta[nv]=ed
            work[i]=valor;
            return
        if modificada[nl[cd]]:
            tt=tt+0.22
            modificada[nl[cd]]=True
            etiqueta[nl[cd]]=ed;
            nl[cd]=nl[cd]+1
            if nl[cd]%k==0:
                nl[cd]=k*cd;
            work[i]=valor;
            return
        tt=tt+0.11
        modificada[nl[cd]]=True
        etiqueta[nl[cd]]=ed;
        nl[cd]=nl[cd]+1
        if nl[cd]%k==0:
            nl[cd]=k*cd;
        work[i]=valor;
        return



nl=[k*i for i in range(0,conjuntos)]
n=4096;
puntos=True #puntos es que va imprimiendo ... es mas resumido, si puntos es False es mas detallado
#for tipo in [1]:
for tipo in range(0,4):
    work=list(valores)
    nextlinea=0
    tt=0
    cc=0
    valida=[False for l in range(m)]
    modificada=[False for l in range(m)]
    etiqueta=[0 for l in range(m)]
    for i in range(0,n-1):
        #print("(", tt,"-",cc, ")", end = "")
        if puntos and i%100==0:
            #print("i: ", tt)
            print(".", end = "")
        for j in range(i+1,n):
            if leer(i,tipo)>leer(j,tipo):
                   temp=leer(i,tipo)
                   escribir(i, tipo,leer(j,tipo))
                   escribir(j,tipo,temp)
        if not puntos:
            print(tipo,i,tt)

    if puntos:
        print(tipo,tt)

