# estructuras/pila.py
from .nodo import Nodo

class Pila:
    def __init__(self):
        self.tope = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio

    def apilar(self, valor):
        nuevo = Nodo(valor)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self.tamanio += 1

    def desapilar(self):
        if self.tope is None:
            return None
        valor = self.tope.valor
        self.tope = self.tope.siguiente
        self.tamanio -= 1
        return valor

    def ver_tope(self):
        return self.tope.valor if self.tope else None

    def esta_vacia(self):
        return self.tope is None