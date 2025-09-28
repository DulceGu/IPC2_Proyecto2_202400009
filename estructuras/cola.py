from .nodo import Nodo

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamanio = 0

    def esta_vacia(self): # si la cola está vacía
        return self.frente is None

    def encolar(self, valor): # agregar al final
        nuevo = Nodo(valor)
        if self.final is None:
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.tamanio += 1

    def desencolar(self): # eliminar del frente
        if self.frente is None:
            return None
        valor = self.frente.valor
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamanio -= 1
        return valor

    def ver_frente(self): # ver el valor del frente sin eliminar
        return self.frente.valor if self.frente else None

    def __len__(self):
        return self.tamanio
