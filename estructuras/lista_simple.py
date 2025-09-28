from .nodo import Nodo
import os

class ListaSimple:
    def __init__(self):
        self.primero = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio

    def insertar(self, valor):
        nuevo = Nodo(valor)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1

    def buscar(self, condicion):
        actual = self.primero
        while actual is not None:
            if condicion(actual.valor):
                return actual.valor
            actual = actual.siguiente
        return None

    def buscar_todos(self, condicion):
        resultados = ListaSimple()
        actual = self.primero
        while actual is not None:
            if condicion(actual.valor):
                resultados.insertar(actual.valor)
            actual = actual.siguiente
        return resultados

    def obtener_en(self, indice):
        if indice < 0 or indice >= self.tamanio:
            return None
        actual = self.primero
        for _ in range(indice):
            actual = actual.siguiente
        return actual.valor

    def graficar(self, nombre_archivo="lista_simple"):
        codigo_dot = '''digraph G {
    rankdir=LR;
    node [shape=record, height=0.1];
'''
        actual = self.primero
        contador = 1
        while actual is not None:
            etiqueta = str(actual.valor).replace('"', '\\"')
            codigo_dot += f'    nodo{contador} [label="{{<f0> {etiqueta} | <f1> }}"];\n'
            contador += 1
            actual = actual.siguiente

        actual = self.primero
        contador = 1
        while actual is not None and actual.siguiente is not None:
            codigo_dot += f'    nodo{contador}:f1 -> nodo{contador + 1}:f0;\n'
            contador += 1
            actual = actual.siguiente

        codigo_dot += '}'

        os.makedirs("reportes/dot", exist_ok=True)
        ruta_dot = f"reportes/dot/{nombre_archivo}.dot"
        with open(ruta_dot, "w", encoding="utf-8") as f:
            f.write(codigo_dot)

        os.makedirs("reportes/html", exist_ok=True)
        ruta_svg = f"reportes/html/{nombre_archivo}.svg"
        os.system(f'dot -Tsvg "{ruta_dot}" -o "{ruta_svg}"')
        return ruta_svg
    
    def iter_nodos(self):
        actual = self.primero
        while actual is not None:
            yield actual
            actual = actual.siguiente

    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente
