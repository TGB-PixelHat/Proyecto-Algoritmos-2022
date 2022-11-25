class Ticket():
    def __init__(self, codigo_ticket, tipo_ticket, id_partido, asiento, asistencia):
        self.codigo_ticket = codigo_ticket
        self.tipo_ticket = tipo_ticket
        self.id_partido = id_partido
        self.asiento = asiento
        self.asistencia = asistencia
    
    def mostrar(self):
        print(f"""
        Código Ticket: {self.codigo_ticket}
        Tipo de Ticket: {self.tipo_ticket}
        ID del partido: {self.id_partido}
        Asiento: {self.asiento}
        Asistencia: {self.asistencia}""")