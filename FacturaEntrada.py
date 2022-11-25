from Factura import Factura

class FacturaEntrada(Factura):
    def __init__(self, subtotal, descuento, iva, total):
        super().__init__(subtotal, descuento, iva, total)