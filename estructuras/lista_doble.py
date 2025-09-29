# estructuras/lista_doble.py
from .nodo_doble import NodoDoble

class ListaDoble:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio

    def insertar(self, valor):
        nuevo = NodoDoble(valor)
        if self.primero is None:
            self.primero = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self.tamanio += 1

    def buscar(self, condicion):
        actual = self.primero
        while actual is not None:
            if condicion(actual.valor):
                return actual.valor
            actual = actual.siguiente
        return None

    def obtener_en(self, indice):
        if indice < 0 or indice >= self.tamanio:
            return None
        
        if indice < self.tamanio // 2:
            actual = self.primero
            for _ in range(indice):
                actual = actual.siguiente
        else:
            actual = self.ultimo
            for _ in range(self.tamanio - 1 - indice):
                actual = actual.anterior
        return actual.valor

    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente