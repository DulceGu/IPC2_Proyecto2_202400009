class Planta:
    def __init__(self, hilera, posicion, litros_agua, gramos_fertilizante, tipo):
        self.hilera = hilera
        self.posicion = posicion
        self.litros_agua = litros_agua
        self.gramos_fertilizante = gramos_fertilizante
        self.tipo = tipo

    def __str__(self):
        return f"Planta(H{self.hilera}-P{self.posicion}, {self.tipo})"