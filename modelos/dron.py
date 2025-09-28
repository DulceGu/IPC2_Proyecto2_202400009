from estructuras.lista_simple import ListaSimple

class Dron:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.hilera_asignada = None
        self.posicion_actual = 0
        self.total_agua = 0
        self.total_fertilizante = 0
        self.instrucciones = ListaSimple()  # instrucciones por segundo

    def asignar_a_hilera(self, numero_hilera):
        self.hilera_asignada = numero_hilera
        self.posicion_actual = 0

    def agregar_instruccion(self, instruccion):
        self.instrucciones.insertar(instruccion)

    def __str__(self):
        return f"{self.nombre} (H{self.hilera_asignada})"

