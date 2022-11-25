from Factura import Factura

class FacturaRestaurante(Factura):
    def __init__(self, subtotal_comida, descuento_comida, total):
        self.subtotal_comida = subtotal_comida
        self.descuento_comida = descuento_comida
        self.total = total