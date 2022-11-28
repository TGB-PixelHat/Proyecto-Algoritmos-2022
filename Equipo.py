class Equipo():
    def __init__(self, nombre_pais, fifa_code, grupo, bandera, id):
        self.nombre_pais = nombre_pais
        self.fifa_code = fifa_code
        self.grupo = grupo
        self.bandera = bandera
        self.id = id
    
    def mostrar(self):
        """
        Muestra los atributos de los equipos
        """
        print(f"""
        Nombre del País: {self.nombre_pais}
        Código de FIFA: {self.fifa_code}
        Grupo: {self.grupo}""")