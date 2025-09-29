
from estructuras.lista_simple import ListaSimple

class SistemaRiego:
    def __init__(self):
        self.lista_drones = ListaSimple()
        self.lista_invernaderos = ListaSimple()

    def agregar_dron(self, dron):
        print(f"[Sistema.agregar_dron] Agregando dron: {dron.nombre} (ID: {dron.id})")
        self.lista_drones.insertar(dron)

    def buscar_dron_por_nombre(self, nombre):
        return self.lista_drones.buscar(lambda d: d.nombre == nombre)

    def buscar_dron_por_id(self, id):
        print(f"[Sistema.buscar_dron_por_id] Buscando dron con ID: {id}")
        dron_encontrado = self.lista_drones.buscar(lambda d: d.id == id)
        if dron_encontrado:
            print(f"[Sistema.buscar_dron_por_id] ✓ Encontrado: {dron_encontrado.nombre}")
        else:
            print(f"[Sistema.buscar_dron_por_id] ❌ No encontrado dron con ID: {id}")
        return dron_encontrado

    def agregar_invernadero(self, invernadero):
        self.lista_invernaderos.insertar(invernadero)

    def buscar_invernadero_por_nombre(self, nombre):
        return self.lista_invernaderos.buscar(lambda i: i.nombre == nombre)

    def limpiar_configuracion(self):
        """Elimina toda la configuración actual (como pide el enunciado al cargar nuevo XML)"""
        print("[Sistema.limpiar_configuracion] Limpiando configuración previa")
        self.lista_drones = ListaSimple()
        self.lista_invernaderos = ListaSimple()