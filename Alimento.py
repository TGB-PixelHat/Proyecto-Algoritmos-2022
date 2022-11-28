from Producto import Producto

class Alimento(Producto):
    def __init__(self, nombre, cantidad, precio, type, adicional):
        self.adicional = adicional
        self.vendido = 0
        super().__init__(nombre, cantidad, precio, type)

    
    def mostrar(self):
        """
        Muestra los atributos del producto alimento
        """
        print(f"""
        Nombre del producto: {self.nombre}
        Precio del producto: {self.precio + (self.precio * 0.16)}$
        Cantidad del producto: {self.cantidad}
        Tipo de producto: {self.type}
        Servir: {self.adicional}""")