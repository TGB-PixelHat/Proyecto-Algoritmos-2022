from Factura import Factura
from Ticket_general import TicketGeneral
from Ticket_VIP import TicketVIP
import math
from collections import Counter

class Cliente():
    def __init__(self, nombre, cedula, edad):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
        self.facturas = []
        self.tickets = []
    
    def mostrar(self):
        print(f"""
        Nombre: {self.nombre}
        Cedula: {self.cedula}""")
        for ticket in self.tickets:
            ticket.mostrar()

    def es_permutacion(self, num1, num2):

        if len(num1) != len(num2):
            return False
        
        return Counter(num1) == Counter(num2)

    def is_vampire(self):
        cedula = self.cedula

        if len(str(cedula)) %2 !=0:
            vampiro = False
        else:
            colmillos = 0

            for x in range(0, int(math.pow(10, len(str(cedula))/2))):
                for y in range(0,int(math.pow(10, len(str(cedula))/2))):
                    if x*y == cedula:
                        if (self.es_permutacion(str(str(x)+""+str(y)), str(cedula))) == True:
                            colmillos += 1
        
            if colmillos >= 2:
                vampiro = True
            else:
                vampiro = False

        if vampiro == True:
            descuento = 0.50
            print("Su cédula es un número vampiro, obtiene un 50% de descuento en su entrada")
        elif vampiro == False:
            descuento = 0
        return descuento    

    def crear_factura(self):
        """
        Crea una factura
        """
        descuento = self.is_vampire()
        for ticket in self.tickets:
            factura = Factura(ticket.asiento, ticket.precio, descuento)
            factura.calc_total()
            factura.mostrar()