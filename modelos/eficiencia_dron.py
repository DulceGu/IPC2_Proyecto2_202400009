class EficienciaDron:
    def __init__(self, nombre, agua, fertilizante):
        self.nombre = nombre
        self.agua = agua
        self.fertilizante = fertilizante

    def to_dict(self):
        # solo para facilitar la generación de XML, no se almacena como dict :)
        return {
            "nombre": self.nombre,
            "litrosAgua": str(self.agua),
            "gramosFertilizante": str(self.fertilizante)
        }
