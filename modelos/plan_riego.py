
from estructuras.lista_simple import ListaSimple
from .eficiencia_dron import EficienciaDron

class PlanRiego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.orden_riego = ListaSimple()  # cada elemento es (hilera, posicion)
        self.tiempo_optimo = 0
        self.agua_total = 0
        self.fertilizante_total = 0
        self.eficiencia_drones = ListaSimple()  # Lista de EficienciaDron
        self.instrucciones_por_tiempo = ListaSimple()  # Lista de ListaSimple de InstruccionTiempo

    def agregar_paso(self, hilera, posicion):
        self.orden_riego.insertar((hilera, posicion))

    def agregar_eficiencia(self, nombre_dron, agua, fertilizante):
        eficiencia = EficienciaDron(nombre_dron, agua, fertilizante)
        self.eficiencia_drones.insertar(eficiencia)

    def agregar_tiempo_instrucciones(self, instrucciones_lista):
        self.instrucciones_por_tiempo.insertar(instrucciones_lista)

    def __str__(self):
        return f"Plan: {self.nombre} ({self.tiempo_optimo}s, {self.agua_total}L, {self.fertilizante_total}g)"