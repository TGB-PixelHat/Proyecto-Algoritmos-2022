class Estadio():
    def __init__(self, nombre, ubicacion, id, capacidad):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.id = id
        self.capacidad = capacidad
        self.restaurantes = []
        

    
    def mostrar(self):
        """
        Muestra los atributos del estadio, junto con sus restaurantes
        """
        print(f"""
        Nombre del estadio: {self.nombre}
        Ubicación del estadio: {self.ubicacion}
        Id del estadio: {self.id}
        Capacidad del estadio: {self.capacidad[0] + self.capacidad[1]} Asientos""")
        print("""
        ------RESTAURANTES DEL ESTADIO------""")
        for restaurante in self.restaurantes:
            restaurante.mostrar()
     