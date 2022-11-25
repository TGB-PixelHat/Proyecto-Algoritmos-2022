from Producto import Producto

class Alimento(Producto):
    def __init__(self, nombre, precio, type, adicional):
        self.adicional = adicional
        super().__init__(nombre, precio, type)

    
    def mostrar(self):
        print(f"""
        Nombre del producto: {self.nombre}
        Precio del producto: {self.precio}
        Tipo de producto: {self.type}
        Servir: {self.adicional}""")