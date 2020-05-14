from datos import valores
from datetime import datetime

class CacheCorresp:
    K = 8            # Tamano del bloque
    k = 4            # Lineas por conjunto
    cachesize = 64   # en bytes
    m = int(cachesize / K)
    conjuntos = int(m / k)

    tt = 0
    cc = 0
    n = 4096
    tipo = -1
    nextlinea = 0

    nl = []
    datos = []
    valida = []
    etiqueta = []
    modificada = []

    lectura = True
    escritura = True

    def __init__(self, tipo):
        self.fecha_hora_i = datetime.now()
        self.tipo = tipo
        self.datos = list(valores)
        self.valida = [False for l in range(self.m)]
        self.etiqueta = [0 for l in range(self.m)]
        self.modificada = [False for l in range(self.m)]
        self.nl = [self.k * i for i in range(0, self.conjuntos)]
        #print(self.tipo)
        #print(self.tt)
        #for i in range(10):
        #    print("(", self.datos[i], ")" , end =" ")

    def __del__(self): 
        self.fecha_hora_d = datetime.now()
        diferencia = self.fecha_hora_d - self.fecha_hora_i
        #print(diferencia.total_seconds())

    def sum_tt(self, n):
        self.tt = self.tt + n
        self.cc = self.cc + 1

    def get_tt(self):
        return self.tt

    def get_cc(self):
        return self.cc

    def asocestaen(self, ed):
        for i in range(self.m):
            if self.valida[i]:
                if self.etiqueta[i] == ed:
                    return i
        return -1

    def asocnovalida(self):
        for i in range(self.m):
            if self.valida[i] == False:
                return i
        return -1

    def asoccestaen(self, cd, ed):
        for i in range(cd * self.k, cd * self.k + self.k):
            if self.valida[i]:
                if self.etiqueta[i] == ed:
                   return i
        return -1

    def asoccnovalida(self, cd):
        for i in range(cd * self.k, cd * self.k + self.k):
            if self.valida[i] == False:
                return i
        return -1

    def leer(self, i):
        if self.lectura: 
            #print("L[", self.tipo, "](", self.cc, ")", end =" ")
            self.lectura = False
        if self.tipo == 0:
            self.sum_tt(0.1)
            return self.datos[i]
        if self.tipo == 1:
            bd = i / self.K
            ld = int(bd % self.m)
            ed = bd / self.m
            if self.valida[ld]:
                if self.etiqueta[ld] == ed:
                    self.sum_tt(0.01)
                    return self.datos[i]
                if self.modificada[ld]:
                    self.sum_tt(0.22)
                    self.etiqueta[ld] = ed
                    self.modificada[ld ]= False
                    return self.datos[i]
                self.sum_tt(0.11)
                self.etiqueta[ld] = ed
                self.modificada[ld] = False
                return self.datos[i]
            self.sum_tt(0.11)
            self.etiqueta[ld] = ed
            self.modificada[ld] = False
            self.valida[ld] = True
            return self.datos[i]
        if self.tipo == 2:
            bd = i / self.K
            ed = bd
            estaen = self.asocestaen(ed)
            if estaen >= 0:
                self.sum_tt(0.01)
                return self.datos[i]
            nv = self.asocnovalida()
            if nv >= 0:
                self.valida[nv] = True
                self.modificada[nv] = False
                self.etiqueta[nv] = ed
                self.sum_tt(0.11)
                return self.datos[i]
            if self.modificada[self.nextlinea]:
                self.sum_tt(0.22)
                self.modificada[self.nextlinea] = False
                self.etiqueta[self.nextlinea] = ed
                self.nextlinea = self.nextlinea + 1
                if self.nextlinea == self.m:
                    self.nextlinea = 0
                return self.datos[i]
            self.sum_tt(0.11)
            self.modificada[self.nextlinea] = False
            self.etiqueta[self.nextlinea] = ed
            self.nextlinea = self.nextlinea + 1
            if self.nextlinea == self.m:
                self.nextlinea = 0
            return self.datos[i]
        if self.tipo == 3:
            #it=it+1
            bd = i / self.K
            cd = int(bd % self.conjuntos)
            ed = bd / self.conjuntos
            estaen = self.asoccestaen(cd, ed)
            if estaen >= 0:
                #ia=ia+1
                self.sum_tt(0.01)
                return self.datos[i]
            nv = self.asoccnovalida(cd)
            if nv >= 0:
                #ib=ib+1
                self.sum_tt(0.11)
                self.modificada[nv] = False
                self.valida[nv] = True
                self.etiqueta[nv] = ed
                return self.datos[i]
            if self.modificada[self.nl[cd]]:
                #ic=ic+1
                self.sum_tt(0.22)
                self.modificada[self.nl[cd]] = False
                self.etiqueta[self.nl[cd]] = ed
                self.nl[cd] = self.nl[cd] + 1
                if self.nl[cd] % self.k == 0:
                    self.nl[cd] = self.k * cd
                return self.datos[i]
            #id=id+1
            self.sum_tt(0.11)
            self.modificada[self.nl[cd]] = False
            self.etiqueta[self.nl[cd]] = ed
            self.nl[cd] = self.nl[cd] + 1
            if self.nl[cd] % self.k == 0:
                self.nl[cd] = self.k * cd
            return self.datos[i]

    def escribir(self, i, valor):
        if self.escritura: 
            #print("E[", self.tipo, "](", self.cc, ")", end =" ")
            self.escritura = False
        if self.tipo == 0:
            self.sum_tt(0.1)
            self.datos[i] = valor
            return
        if self.tipo == 1:
            bd = i / self.K
            ld = int(bd % self.m)
            ed = bd / self.m
            if self.valida[ld]:
                if self.etiqueta[ld] == ed:
                    self.sum_tt(0.01)
                    self.modificada[ld] = True
                    self.datos[i] = valor
                    return
                if self.modificada[ld]:
                    self.sum_tt(0.22)
                    self.etiqueta[ld] = ed
                    self.modificada[ld] = True
                    self.datos[i] = valor
                    return
                self.sum_tt(0.11)
                self.etiqueta[ld] = ed
                self.modificada[ld] = True
                self.datos[i] = valor
                return
            self.sum_tt(0.11)
            self.etiqueta[ld] = ed
            self.modificada[ld] = True
            self.valida[ld] = True
            self.datos[i] = valor
            return
        if self.tipo == 2:
            bd = i / self.K
            ed = bd
            estaen = self.asocestaen(ed)
            if estaen>=0:
                self.sum_tt(0.01)
                self.modificada[estaen] = True
                self.datos[i] = valor
                return
            nv = self.asocnovalida()
            if nv >= 0:
                self.valida[nv] = True
                self.modificada[nv] = True
                self.etiqueta[nv] = ed
                self.sum_tt(0.11)
                self.datos[i] = valor
                return
            if self.modificada[self.nextlinea]:
                self.sum_tt(0.22)
                self.modificada[self.nextlinea] = True
                self.etiqueta[self.nextlinea] = ed
                self.nextlinea = self.nextlinea + 1
                if self.nextlinea == m:
                    self.nextlinea = 0
                self.datos[i] = valor
                return
            self.sum_tt(0.11)
            self.modificada[self.nextlinea] = True
            self.etiqueta[self.nextlinea] = ed
            self.nextlinea = self.nextlinea + 1
            if self.nextlinea == m:
                self.nextlinea = 0
            self.datos[i] = valor
            return
        if self.tipo == 3:
            bd=i / self.K
            cd = int(bd % self.conjuntos)
            ed=bd / self.conjuntos
            estaen = self.asoccestaen(cd, ed)
            if estaen >= 0:
                self.modificada[estaen] = True
                self.sum_tt(0.01)
                self.datos[i] = valor
                return
            nv = self.asoccnovalida(cd)
            if nv >= 0:
                self.sum_tt(0.11)
                self.modificada[nv] = True
                self.valida[nv] = True
                self.etiqueta[nv] = ed
                self.datos[i] = valor
                return
            if self.modificada[nl[cd]]:
                self.sum_tt(0.22)
                self.modificada[nl[cd]] = True
                self.etiqueta[nl[cd]] = ed
                self.nl[cd] = self.nl[cd] + 1
                if self.nl[cd] % self.k == 0:
                    self.nl[cd] = self.k * cd
                self.datos[i] = valor
                return
            self.sum_tt(0.11)
            self.modificada[nl[cd]] = True
            self.etiqueta[nl[cd]] = ed
            self.nl[cd] = self.nl[cd] + 1
            if self.nl[cd] % self.k == 0:
                self.nl[cd] = self.k * cd
            self.datos[i] = valor
            return
