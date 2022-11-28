class Producto():
    def __init__(self, nombre, cantidad, precio, type):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.vendido = 0
        self.type = type
    
    def mostrar(self):
        """
        Muestra los atributos del producto
        """
        print(f"""
        Nombre del producto: {self.nombre}
        Precio del producto: {self.precio + (self.precio * 0.16)}$
        Cantidad del producto: {self.cantidad}
        Tipo de producto: {self.type}""")