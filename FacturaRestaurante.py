from Factura import Factura

class FacturaRestaurante(Factura):
    def __init__(self, asiento, subtotal, descuento, cedula,  id_partido, productos_comprados):
        self.cedula = cedula
        self.productos_comprados = productos_comprados
        self.total = 0
        super().__init__(asiento, id_partido, subtotal, descuento)
    
    def calc_iva(self):
        """
        Calcula el iva y se lo suma al subtotal
        """
        self.subtotal = self.subtotal + self.subtotal * 0.16

    def calc_descuento(self):
        """
        Calcula el descuento
        """
        self.descuento = self.subtotal * self.descuento
    
    def calc_total(self):
        """
        Calcula el total a pagar, primero calculando el iva y el descuento para realizar el cálculo
        """
        self.calc_iva()
        self.calc_descuento()
        self.total = self.subtotal - self.descuento

    def mostrar(self):
        """
        Muestra los atributos de la factura del restaurante, junto con los atributos de cada producto comprado
        """
        print(f"""
        Subtotal de la comida: {self.subtotal}$
        Descuento otorgado: {self.descuento}$
        Total a pagar por la comida: {self.total}
        Productos comprados: """)
        for producto in self.productos_comprados:
            print(f"""
            Nombre del producto: {producto["producto"].nombre}
            Precio del producto: {producto["producto"].precio + (producto["producto"].precio * 0.16)}
            Cantidad comprada: {producto["cantidad"]}""")
