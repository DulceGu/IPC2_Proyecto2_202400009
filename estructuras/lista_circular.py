from .nodo import Nodo

class ListaCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio

    def insertar(self, valor): # inserción al final
        nuevo = Nodo(valor)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero # apunta al primero
        else: # lista no está vacía
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
        self.tamanio += 1