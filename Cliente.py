from Factura import Factura
from FacturaRestaurante import FacturaRestaurante
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
        """
        Muestra los atributos del cliente, con sus facturas y sus tickets
        """
        print(f"""
        Nombre: {self.nombre}
        Cedula: {self.cedula
        }""")
        print("------TICKETS DEL CLIENTE------")
        for ticket in self.tickets:
            ticket.mostrar()
        print()
        print("------FACTURAS DEL CLIENTE------")
        for factura in self.facturas:
            factura.mostrar()
        

    def es_permutacion(self, a, b):
        if len(a) != len(b):
            return False
        return Counter(a) == Counter(b)

    def is_vampire(self):
        colmillos = 0
        if len(str(self.cedula)) %2 != 0:
            vampiro = False

        else:
            for x in range(0,int(math.pow(10, len(str(self.cedula))/2))):
                    for y in range(0,int(math.pow(10, len(str(self.cedula))/2))):
                        if (x*y == self.cedula):
                            #print('Fangs: %d %d' % (x, y))
                            if (self.es_permutacion(str(str(x)+''+str(y)), str(self.cedula)) ):
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

    def is_perfect(self, num, i, sum):
        """
        Determina si el número que recibe es un número perfecto o no
        Si es perfecto retornará una variable descuento que valdrá 0.5
        Si no es perfecto retornará esa misma variable pero con el valor de 0
        """
        if i < num:
            if num % i == 0:
                sum +=  i
            return self.is_perfect(num, i+1, sum)
    
        if i == num:
            if sum == num:
                print("Tu cédula es un número perfecto, por lo que te vamos a otorgar un 15% de descuento del monto a pagar")
                descuento = 0.15
            else:
                descuento = 0
        return descuento

    def crear_factura(self, ticket):
        """
        Crea una factura (Para la compra de asiento en un partido)
        """
        descuento = self.is_vampire()
        factura = Factura(ticket.asiento, ticket.id_partido, ticket.precio, descuento)
        factura.calc_total()
        factura.mostrar()
        return factura
    
    def crear_factura_restaurante(self, ticket, productos_comprados):
        """
        Crea una factura (Para la compra de productos en un restaurante)
        """
        subtotal = 0
        descuento = self.is_perfect(self.cedula, 1, 0)
        for item in productos_comprados:
            subtotal += (item["producto"].precio * item["cantidad"])

        factura = FacturaRestaurante(ticket.asiento, subtotal, descuento, self.cedula, ticket.id_partido, productos_comprados)
        factura.calc_total()
        factura.mostrar()
        return factura