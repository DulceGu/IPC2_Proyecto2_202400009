# modelos/invernadero.py
from estructuras.lista_simple import ListaSimple
from .planta import Planta

class Invernadero:
    def __init__(self, nombre, numero_hileras, plantas_por_hilera):
        self.nombre = nombre
        self.numero_hileras = numero_hileras
        self.plantas_por_hilera = plantas_por_hilera
        self.plantas = ListaSimple()          # todas las plantas del invernadero
        self.drones_asignados = ListaSimple() # Lista de drones asignados (por hilera)
        self.planes_riego = ListaSimple()

    def agregar_planta(self, planta):
        if 1 <= planta.hilera <= self.numero_hileras and 1 <= planta.posicion <= self.plantas_por_hilera:
            self.plantas.insertar(planta)
        else:
            print(f"Error: Planta H{planta.hilera}-P{planta.posicion} fuera de rango en {self.nombre}")

    def asignar_dron_a_hilera(self, dron, numero_hilera):
        if 1 <= numero_hilera <= self.numero_hileras:
            dron.asignar_a_hilera(numero_hilera)
            self.drones_asignados.insertar(dron)
        else:
            print(f"Error: Hilera {numero_hilera} no existe en {self.nombre}")

    def obtener_planta(self, hilera, posicion):
        return self.plantas.buscar(lambda p: p.hilera == hilera and p.posicion == posicion)

    def obtener_dron_por_hilera(self, hilera):
        return self.drones_asignados.buscar(lambda d: d.hilera_asignada == hilera)

    def agregar_plan_riego(self, plan):
        self.planes_riego.insertar(plan)

    def buscar_plan_por_nombre(self, nombre_plan):
        return self.planes_riego.buscar(lambda p: p.nombre == nombre_plan)

    def __str__(self):
        return f"Invernadero: {self.nombre} ({self.numero_hileras} hileras, {self.plantas_por_hilera} plantas/hilera)"