from estructuras.lista_simple import ListaSimple

class SistemaRiego:
    def __init__(self):
        self.lista_drones = ListaSimple()
        self.lista_invernaderos = ListaSimple()

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

    def limpiar_configuracion(self):
        """Elimina toda la configuración actual (como pide el enunciado al cargar nuevo XML)"""
        self.lista_drones = ListaSimple()
        self.lista_invernaderos = ListaSimple()

