from Producto import Producto

class Bebida(Producto):
    def __init__(self, nombre, cantidad, precio, type, adicional):
        self.adicional = adicional 
        self.vendido = 0
        super().__init__(nombre, cantidad, precio, type)
    
    def mostrar(self):
        """
        Muestra los atributos del producto bebida
        """
        print(f"""
        Nombre del producto: {self.nombre}
        Precio del producto: {self.precio + (self.precio * 0.16)}$
        Tipo de producto: {self.type}
        Tipo de Bebida: {self.adicional}""")
