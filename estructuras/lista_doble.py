import os
from .nodo import Nodo

class ListaDoble:
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
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self.tamanio += 1

    def imprimir_adelante(self): # desde primero hasta último
        actual = self.primero
        while actual is not None:
            print(actual.valor)
            actual = actual.siguiente

    def imprimir_atras(self): # desde último hasta primero
        actual = self.ultimo
        while actual is not None:
            print(actual.valor)
            actual = actual.anterior

    def buscar(self, condicion): # condición es una función que recibe valor y devuelve bool
        actual = self.primero
        while actual is not None:
            if condicion(actual.valor):
                return actual.valor
            actual = actual.siguiente
        return None

    def graficar(self, nombre_archivo="lista_doble"): # similar a lista_simple pero con doble enlace
        codigo_dot = '''digraph G {
    rankdir=LR;
    node [shape=record, height=0.1];
    '''
        actual = self.primero
        contador = 1

        # generamos los nodos
        while actual is not None:
            etiqueta = str(actual.valor).replace('"', '\\"')
            codigo_dot += f'    nodo{contador} [label="{{<f1>|{etiqueta}|<f2>}}"];\n'
            contador += 1
            actual = actual.siguiente

        # reseteamos para los enlaces
        actual = self.primero
        contador = 1

        while actual is not None and actual.siguiente is not None: # aseguramos que haya siguiente
            codigo_dot += f'    nodo{contador}:f2 -> nodo{contador + 1}:f1;\n'
            codigo_dot += f'    nodo{contador + 1}:f1 -> nodo{contador}:f2;\n'
            contador += 1
            actual = actual.siguiente

        codigo_dot += '}'

        import os # aseguramos que la carpeta exista
        ruta_dot = f"reportes/dot/{nombre_archivo}.dot"
        os.makedirs("reportes/dot", exist_ok=True)
        with open(ruta_dot, "w", encoding="utf-8") as archivo:
            archivo.write(codigo_dot)

        ruta_svg = f"reportes/html/{nombre_archivo}.svg" # aseguramos que la carpeta exista
        os.makedirs("reportes/html", exist_ok=True)
        comando = f'dot -Tsvg "{ruta_dot}" -o "{ruta_svg}"'
        os.system(comando)

        print(f"Gráfico generado: {ruta_svg}") # mostramos mensaje
        return ruta_svg