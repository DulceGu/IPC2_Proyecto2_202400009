# modelos/sistema.py
from ..estructuras.lista_simple import ListaSimple
from ..estructuras.cola import Cola

class SistemaRiego:
    def __init__(self):
        self.lista_drones = ListaSimple()
        self.lista_invernaderos = ListaSimple()
        self.dron_actual = None

    def agregar_dron(self, dron):
        self.lista_drones.insertar(dron)

    def buscar_dron_por_nombre(self, nombre):
        return self.lista_drones.buscar(lambda d: d.nombre == nombre)

    def buscar_dron_por_id(self, id):
        return self.lista_drones.buscar(lambda d: d.id == id)

    def agregar_invernadero(self, invernadero):
        self.lista_invernaderos.insertar(invernadero)

    def buscar_invernadero_por_nombre(self, nombre):
        return self.lista_invernaderos.buscar(lambda i: i.nombre == nombre)

    def graficar_td_as(self):
        # Graficar lista de drones
        self.lista_drones.graficar()  # Debo agregar método graficar a ListaSimple
        # Graficar otros TDAs aquí...