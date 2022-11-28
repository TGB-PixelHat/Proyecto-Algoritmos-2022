class Partido():
    def __init__(self, equipo_local, equipo_visitante, fecha_y_hora, estadio, id):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.fecha_y_hora = fecha_y_hora
        self.estadio = estadio
        self.id = id
        self.asientos_tomados = []
        self.asientos = []
        self.asistencia = []
        self.vip_comprados = 0
        self.general_comprados = 0

    def mostrar(self):
        """
        Muestra los atributos del partido
        """
        print(f"""
        ------------
        Equipo Local: {self.equipo_local.nombre_pais}
        Equipo Visitante: {self.equipo_visitante.nombre_pais}
        Fecha y Hora del partido: {self.fecha_y_hora}
        Estadio: {self.estadio.id}
        ID del partido: {self.id}
        ------------""")
    
    def mapa(self):
        """
        Imprime el mapa del estadio seleccionado con sus asientos
        Cuando se llega a la mitad de las filas a imprimir, se imprime el dibujo del estadio
        """
        print("")
        x = (self.estadio.capacidad[0] + self.estadio.capacidad[1]) // 10
        y = 10
        z = x // 2
        for a in range(x):
            fila = ["x" if f"{a}-{b}" in self.asientos_tomados else f"{a}-{b}" for b in range(y)]
            self.asientos.append(fila)
            print("|".join(fila))
            print()
            if len(self.asientos) == z:
                print("""
+-------------------------------------+---------------------------------------+
|/                                    |                                      \\|
|                                     |                                       |
|                                     |                                       |
+----------+                          |                            +----------+
|          |                          |                            |          |
+---+      |                          |                            |      +---+
|   |      |                       ---+---                         |      |   |
|   |      |\\                     /   |   \\                       /|      |   |
|   |      | |                   |    |    |                     | |      |   |
|   |      |/                     \\   |   /                       \\|      |   |
|   |      |                       ---+---                         |      |   |
+---+      |                          |                            |      +---+
|          |                          |                            |          |
+----------+                          |                            +----------+
|                                     |                                       |
|                                     |                                       |
|\\                                    |                                      /|
+-------------------------------------+---------------------------------------+
""")