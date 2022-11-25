class Factura():
    def __init__(self, asiento, subtotal, descuento):
        self.asiento = asiento
        self.subtotal = subtotal
        self.descuento = descuento
        self.iva = 0
        self.total = 0
    
    def mostrar(self):
        print(f"""
        Asiento: {self.asiento}
        Subtotal: {self.subtotal}$
        Descuento: {self.descuento}$
        IVA: {self.iva}$
        Total: {self.total}$""")
    
    def calc_iva(self):
        self.iva = self.subtotal*0.16
    
    def calc_descuento(self):
        self.descuento = self.descuento*self.subtotal

    def calc_total(self):
        self.calc_iva()
        self.calc_descuento()
        self.total = self.subtotal + self.iva - self.descuento

    