from ..estructuras.lista_simple import ListaSimple

class PlanRiego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.orden_riego = ListaSimple()  
        self.tiempo_optimo = 0
        self.agua_total = 0
        self.fertilizante_total = 0
        # usaremos ListaSimple de tuplas (nombre, agua, fert)
        self.eficiencia_drones = ListaSimple() 
        # para instrucciones_por_tiempo cada "tiempo" será un objeto o diccionario simulado
        self.instrucciones_por_tiempo = ListaSimple()

    def agregar_paso(self, paso):
        self.orden_riego.insertar(paso)

    def agregar_eficiencia(self, nombre_dron, agua, fertilizante):
        # creamos una tupla como objeto simple
        eficiencia = {
            "nombre": nombre_dron,
            "agua": agua,
            "fertilizante": fertilizante
        }
        self.eficiencia_drones.insertar(eficiencia)

    def agregar_tiempo_instrucciones(self, instrucciones_en_tiempo):
        self.instrucciones_por_tiempo.insertar(instrucciones_en_tiempo)

    def __str__(self):
        return f"Plan: {self.nombre}"