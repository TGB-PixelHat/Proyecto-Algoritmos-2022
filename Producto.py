class Producto():
    def __init__(self, nombre, precio, type):
        self.nombre = nombre
        self.precio = precio
        self.type = type
    
    def mostrar(self):
        print(f"""
        Nombre del producto: {self.nombre}
        Precio del producto: {self.precio}
        Tipo de producto: {self.type}""")