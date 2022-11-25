class Restaurante():
    def __init__(self, nombre, id_estadio):
        self.nombre = nombre
        self.id_estadio = id_estadio
        self.productos = []

    def mostrar_todo(self):
        print(f"""
        Nombre del restaurante: {self.nombre}
        ID del estadio: {self.id_estadio}
        Productos: """)
        for producto in self.productos:
            producto.mostrar()
    