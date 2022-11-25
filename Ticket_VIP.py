from Ticket import Ticket

class TicketVIP(Ticket):
    def __init__(self, codigo_ticket, id_partido, asiento, asistencia):
        self.precio = 120
        super().__init__(codigo_ticket, "Ticket VIP", id_partido, asiento, asistencia)

def mostrar(self):
        print(f"""
        Código Ticket: {self.codigo_ticket}
        Tipo de Ticket: {self.tipo_ticket}
        ID del partido: {self.id_partido}
        Asiento: {self.asiento}
        Asistencia: {self.asistencia}""")