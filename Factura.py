class Factura():
    def __init__(self, asiento, id_partido, subtotal, descuento):
        self.asiento = asiento
        self.id_partido = id_partido
        self.subtotal = subtotal
        self.descuento = descuento
        self.iva = 0
        self.total = 0
    
    def mostrar(self):
        """
        Muestra los atributos de la factura
        """
        print(f"""
        Asiento: {self.asiento}
        Subtotal: {self.subtotal}$
        Descuento: {self.descuento}$
        IVA: {self.iva}$
        Total: {self.total}$""")
    
    def calc_iva(self):
        """
        Calcula el iva
        """
        self.iva = self.subtotal*0.16
    
    def calc_descuento(self):
        """
        Calcula el descuento
        """
        self.descuento = self.descuento*self.subtotal

    def calc_total(self):
        """
        Calcula el total, primero calculando el iva y el descuento para conseguir el monto final
        """
        self.calc_iva()
        self.calc_descuento()
        self.total = self.subtotal + self.iva - self.descuento

    