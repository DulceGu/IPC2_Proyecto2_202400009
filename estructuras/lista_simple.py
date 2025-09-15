from .nodo import Nodo

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

    def buscar_por_indice(self, indice):
        if indice < 0 or indice >= self.tamanio:
            return None
        actual = self.primero
        for i in range(indice):
            actual = actual.siguiente
        return actual.valor

    def buscar(self, condicion):
        actual = self.primero
        while actual is not None:
            if condicion(actual.valor):
                return actual.valor
            actual = actual.siguiente
        return None

    def imprimir(self):
        actual = self.primero
        while actual is not None:
            print(actual.valor)
            actual = actual.siguiente

    def graficar(self, nombre_archivo="lista_simple"):
        codigo_dot = '''digraph G {
    rankdir=LR;
    node [shape=record, height=0.1];
    '''
        actual = self.primero
        contador = 1

        # generamos lo nodos
        while actual is not None:
            etiqueta = str(actual.valor).replace('"', '\\"')
            codigo_dot += f'    nodo{contador} [label="{{<f0> {etiqueta} | <f1> }}"];\n'
            contador += 1
            actual = actual.siguiente

        # reseteamos para los enlaces
        actual = self.primero
        contador = 1

        # generamos los enlaces
        while actual is not None and actual.siguiente is not None:
            codigo_dot += f'    nodo{contador}:f1 -> nodo{contador + 1}:f0;\n'
            contador += 1
            actual = actual.siguiente

        codigo_dot += '}'

        import os
        ruta_dot = f"reportes/dot/{nombre_archivo}.dot"
        os.makedirs("reportes/dot", exist_ok=True)
        with open(ruta_dot, "w", encoding="utf-8") as archivo:
            archivo.write(codigo_dot)

        ruta_svg = f"reportes/html/{nombre_archivo}.svg"
        os.makedirs("reportes/html", exist_ok=True)
        comando = f'dot -Tsvg "{ruta_dot}" -o "{ruta_svg}"'
        os.system(comando)

        print(f"Gráfico generado: {ruta_svg}")
        return ruta_svg