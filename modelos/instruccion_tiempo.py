# modelos/instruccion_tiempo.py
class InstruccionTiempo:
    def __init__(self, nombre_dron, accion):
        self.nombre_dron = nombre_dron
        self.accion = accion

    def __str__(self):
        return f"{self.nombre_dron}: {self.accion}"