import requests
from Estadio import Estadio
from Partido import Partido
from Equipo import Equipo
from Cliente import Cliente
from Restaurante import Restaurante
from Producto import Producto
from Bebida import Bebida
from Alimento import Alimento
from Ticket_general import TicketGeneral
from Ticket_VIP import TicketVIP
import random

class App():
    def __init__(self):
        self.equipos = []
        self.estadios = []
        self.partidos = []
        self.clientes = []
        self.codigos_usados = []
        self.codigos_ticket = []

    def download(self):
        """
        Descarga los datos de la API sobreescribiendo los datos existentes en los archivos .txt
        """

        opcion = input("""
        Esta acción sobreescribirá todos los datos almacenados en iteraciones previas del programa, desea continuar?
        1.Si
        2.No
        > """)
        while opcion != '1' and opcion !='2':
            opcion = input("""
            Ingreso Inválido, ingrese si desea continuar con esta acción
            1.Si
            2.No
            > """)
        if opcion == '1':
            #Descarga los datos de los equipos
            var = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json")
            equipos = var.json()
            for team in equipos:
                team = Equipo(team['name'], team["fifa_code"], team['group'] )
                self.equipos.append(team)

            #Descarga los estadios, restaurantes y productos del restaurante
            var = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json")
            estadios_mundial = var.json()
            
            for info in estadios_mundial:
                estadio = Estadio(info["name"], info["location"], info["id"], info["capacity"])
                self.estadios.append(estadio)
                for edificio in info["restaurants"]:
                    restaurante = Restaurante(edificio["name"], info["id"])
                    estadio.restaurantes.append(restaurante)
                    for product in edificio["products"]:
                        if product["type"] == 'food':
                            producto = Alimento(product["name"], product["price"], product["type"], product["adicional"])
                        elif product["type"] == 'beverages':
                            producto = Bebida(product["name"], product["price"], product["type"], product["adicional"])
                        restaurante.productos.append(producto)

            #Descarga los partidos
            var = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json")
            partidos = var.json()
            for info in partidos:
                for equi in self.equipos:
                    if info["home_team"] == equi.nombre_pais:
                        equipo_local = equi
                    
                    elif info["away_team"] == equi.nombre_pais:
                        equipo_visitante = equi

                for esta in self.estadios:
                    if info["stadium_id"] == esta.id:
                        estadio_jugar = esta

                partido = Partido(equipo_local, equipo_visitante, info["date"], estadio_jugar, info["id"])
                self.partidos.append(partido)
 
    def show_teams(self):
        """
        Muestra los datos de todos los equipos de la base de datos
        """
        for i, equipo in enumerate(self.equipos):
            print(str(i+1) + "-")
            equipo.mostrar()
    
    def show_stadiums(self):
        """
        Muestra los datos de todos los estadios de la base de datos
        """
        for estadio in self.estadios:
            print()
            estadio.mostrar()
    
    def show_matches(self):
        """
        Muestra todos los datos de los partidos de la base de datos
        """
        for partido in self.partidos:
            print()
            partido.mostrar()

    def search_match(self):
        """
        Muestra los partidos dependiendo de lo que indique el usuario
        """        
        opcion = input("""
        Elija el cómo desea Buscar los partidos:
        1.Buscar los Partidos por País
        2.Buscar todos los partidos que se mostrarán en un estadio específico
        3.Buscar todos los partidos que se jugarán en una fecha específica
        > """)

        while opcion != '1' and opcion != '2' and opcion != '3':
            opcion = input("""
            Ingreso inválido, introduzca el número de la acción que desea realizar:
            1.Buscar los Partidos por País
            2.Buscar todos los partidos que se mostrarán en un estadio específico
            3.Buscar todos los partidos que se jugarán en una fecha específica
            > """)
        
        if opcion == '1':
            self.show_teams()
            pais = input("Escriba el código FIFA del país al que quiere buscarle los partidos: ")
            while not pais.isalpha() or pais.isspace():
                pais = input("Ingreso Inválido. Escriba el código FIFA del país al que quiere buscarle los partidos: ")
            pais = pais.upper()
            comprobante = False
            
        
            for partido in self.partidos:
                if partido.equipo_local.fifa_code == pais or partido.equipo_visitante.fifa_code == pais:
                    comprobante = True
                    print("     ------")
                    partido.mostrar()
                    print("     ------")
            if comprobante == False:
                print("El código que introdujo no está en la lista de partidos, intente de nuevo")

        elif opcion == '2':
            self.show_stadiums()
            while True:
                try:
                    estadio = int(input("Escriba el Id del Estadio al que desea buscarle los partidos: "))
                    if estadio not in range(0, len(self.estadios) +1):
                        raise Exception
                    break
                except:
                    print("Error!")

            for partido in self.partidos:
                if partido.estadio.id == estadio:
                    print("     -----")
                    partido.mostrar()
                    print("     -----")
                  
        else:
            fecha = input("Introduzca la fecha de la cual quiere buscar los partidos (Formato MM/DD/YYYY): ")
            while True:
                try:
                    if len(fecha) > 10:
                        raise Exception
                    if fecha.count("/") != 2:
                        raise Exception                    
                    for caracter in fecha:
                        if not caracter.isnumeric() and not "/":
                            raise Exception
                    break
                except:
                    print("Error!")
            
            comprobante = False
            for partido in self.partidos:
                if fecha in partido.fecha_y_hora:
                    print("     -----")
                    partido.mostrar()
                    print("     -----")
                    comprobante = True
            
            if comprobante == False:
                print("No hay ningún partido en la fecha que suted marcó, por favor intente de nuevo")

    def create_code(self):
        """
        Genera un código al azar para el ticket, si el código del Ticket ya existe lo hace de nuevo, retorna el código generado
        """
        codigo_ticket = random.randint(1000000, 9999999)
        while codigo_ticket in self.codigos_ticket:            
            codigo_ticket = random.randint(1000000, 9999999)
        return codigo_ticket

    def buy_tickets(self):
        """
        Registra al cliente y hace que seleccione el ID del partido que quiere comprarle un ticket, hace que seleccione el asiento, y le imprime la factura
        """
        while True:
            try:
                name = input("Introduzca su nombre: ")
                if not name.isalpha() or name.isspace():
                    raise Exception
                cedula = int(input("Ingrese su cédula: "))
                if cedula <= 0:
                    raise Exception
                edad = int(input("Introduzca su edad: "))
                if edad <= 0 or edad >= 118:
                    raise Exception
                tipo_ticket = input("Introduzca el tipo de ticket que desea comprar (1-General   2-VIP): ")
                if tipo_ticket != '1' and tipo_ticket != '2':
                    raise Exception
                break
            except:
                print("Error! Intente de nuevo")
        

        self.show_matches()
        option = input("Seleccione el Id del partido al que desea comprarle la entrada: ")
        while not option.isnumeric() and option not in range(1, len(self.partidos) + 1):
            option = input("Ingreso Inválido, seleccione el ID del partido al que desea comprarle el boleto: ")
        
        for partido in self.partidos:
            if option == partido.id:
                estadio = partido
                estadio.mapa()
        while True:
            try:
                asiento = input("Introduzca el número de asiento en el que quiere sentarse (Formato: NN-NN): ")
                comprobante = False
                for caracter in asiento:
                    if not caracter.isnumeric() and not "-":
                        raise Exception
                for fila in estadio.asientos:
                    if asiento in fila:
                        comprobante = True
                if asiento in estadio.asientos_tomados:
                    raise Exception
                if comprobante == False:
                    raise Exception
                break
            except:
                print("Error! Intente de nuevo")
        
        estadio.asientos.clear()

        codigo_ticket = self.create_code()
        if tipo_ticket == '1':
            ticket = TicketGeneral(codigo_ticket, option, asiento, False)
        elif tipo_ticket == '2':
            ticket = TicketVIP(codigo_ticket, option, asiento, False)
        
        comprobante_cliente = False
        for cliente in self.clientes:
            if cedula == cliente.cedula:
                comprobante_cliente = True
                cliente.tickets.append(ticket)
                cliente.crear_factura()
        
        if comprobante_cliente == False:
            cliente = Cliente(name, cedula, edad)
            cliente.tickets.append(ticket)
            cliente.crear_factura()

        continuar = input("Desea continuar con el pago? 1.Si  2.No: ")
        while continuar != '1' and continuar != '2':
            continuar = input("Ingreso Inválido, desea continuar con el pago? 1.Si  2.No: ")

        if continuar == '1':
            if comprobante_cliente == False:
                self.clientes.append(cliente)
            estadio.asientos_tomados.append(asiento)
            self.codigos_ticket.append(codigo_ticket)
            cliente.mostrar()
        
        else:
            if comprobante_cliente == True:
                for cliente in self.clientes:
                    if cedula == cliente.cedula:
                        index = cliente.tickets.index(ticket)
                        del cliente.tickets[index]
            
            if comprobante_cliente == False:
                index = cliente.tickets.index(ticket)
                del cliente.tickets[index]
            print("Pago cancelado exitosamente, regresará al menú principal")
        
    def use_tickets(self):
        """
        Registra la asistencia de un ticket a un partido
        """
        for i, cliente in enumerate(self.clientes):
            print(f"\t{i + 1}")
            cliente.mostrar()
        while True:
            try:                
                option = int(input("Introduzca el número del cliente que desea confirmar la asistencia: "))
                if option not in range(1, len(self.clientes) +1):
                    raise Exception
                cliente = self.clientes[option -1]
                break
            except:
                print("Error!")
        for i, ticket in enumerate(cliente.tickets):
            print(f"\t{i +1}")
            ticket.mostrar()
        while True:
            try:
                asistencia = int(input("Ingrese el número del ticket al que desea confirmar la asistencia: "))
                if asistencia not in range(1, len(cliente.tickets) +1):
                    raise Exception
                ticket = cliente.tickets[asistencia -1]
                break
            except:
                print("Error!")
        
        if ticket.codigo_ticket in self.codigos_usados:
            print("Este Ticket ya ha sido registrado previamente, intente con otro ticket")
        elif ticket.codigo_ticket in self.codigos_ticket:
            if ticket.asistencia == False:
                ticket.asistencia = True
                for partido in self.partidos:
                    if ticket.id_partido == partido.id:
                        partido.asistencia.append(ticket)
                        self.codigos_usados.append(ticket.codigo_ticket)
                        print("Asistencia Registrada exitosamente!")
        else:
            print("El código de este ticket no se encuentra en nuestra base de datos")

    def busqueda_producto_nombre(self, restaurante):
        """
        Busca los productos del restaurante y los muestra a partir del Nombre (Cliente debe saber el nombre del producto antes)
        """
        lista_productos = []
        for producto in restaurante.productos:
            print(f"\t{producto.nombre}")
            lista_productos.append(producto.nombre)

        while True:
            try:
                nombre_mostrar = input("Introduzca el nombre del alimento al que desea ver su información: ")
                if nombre_mostrar not in lista_productos:
                    raise Exception
                for producto in restaurante.productos:
                    if nombre_mostrar == producto.nombre:
                        producto.mostrar()
                break
            except:
                print("El nombre que introdujo no se encuentra en la base de datos")
            
    def busqueda_producto_tipo(self, restaurante):
        """
        Busca los productos del restaurante y los muestra dependiendo de su tipo (Bebida o Alimento)
        """
        tipo_mostrar = input("""
        Ingrese el número correspondiente al tipo de producto que desea buscar:
        1.Alimento
        2.Bebida
        > """)
        while tipo_mostrar != '1' and tipo_mostrar != '2':
            tipo_mostrar = input("Ingreso inválido, introduzca el número correspondiente al tipo de producto que desea buscar: ")
        
        if tipo_mostrar == '1':
            for producto in restaurante.productos:
                if producto.type == "food":
                    producto.mostrar()
        elif tipo_mostrar == '2':
            for producto in restaurante.productos:
                if producto.type == 'beverages':
                    producto.mostrar()

    def busqueda_producto_rango_precio(self,restaurante):
        """
        Busca los productos del restaurante y los muestra dependiendo de un rango de precio 
        """
        while True:
            try:
                x = int(input("Ingrese el valor mínimo del rango de precio: "))
                if x < 0:
                    raise Exception
                y = int(input("Ingrese el valor máximo del rango de precio (Debe ser mayor que el anterior): "))
                if y < 0 or y <= x:
                    raise Exception
                break
            except:
                print("Error!")
        for producto in restaurante.productos:
            if producto.precio in range(x, y+1):
                producto.mostrar()
    
    def restaurant_management(self):
        es_vip = False
        for i, cliente in enumerate(self.clientes):
            print(f"\t{i + 1}")
            cliente.mostrar()
        while True:
            try:                
                option = int(input("Introduzca el número del cliente que está ingresando actualmente a la base de datos: "))
                if option not in range(1, len(self.clientes) +1):
                    raise Exception
                cliente = self.clientes[option -1]
                break
            except:
                print("Error!")

        for ticket in cliente.tickets:
            if ticket.tipo_ticket == "Ticket VIP":
                es_vip = True
        if es_vip == False:
            print("No es usuario VIP de ninguno de los Tickets que ha comprado, por lo que no puede ver los productos de los restaurantes.")
        
        elif es_vip == True:
            for i, ticket in enumerate(cliente.tickets):
                if ticket.tipo_ticket == "Ticket VIP":
                    print(f"\t{i+1}")
                    ticket.mostrar()

                    while True:
                        try:
                            seleccion_ticket = int(input("Seleccione el número del Ticket VIP al cual desea ver el restaurante de su estadio: "))
                            if seleccion_ticket not in range(1, len(cliente.tickets) + 1):
                                raise Exception
                            ticket = cliente.tickets[seleccion_ticket - 1]
                            break
                        except:
                            print("Error!")
                    
            for partido in self.partidos:
                if ticket.id_partido == partido.id:
                    estadio = partido.estadio
            
            for i, restaurante in enumerate(estadio.restaurantes):
                print(f"\t{i+1}")
                print(f"\t{restaurante.nombre}")
            
            while True:
                try:
                    seleccion_restaurante = int(input("Seleccione el Restaurante al que quiere ver los productos: "))
                    if seleccion_restaurante not in range(1, len(estadio.restaurantes) +1):
                        raise Exception
                    restaurante = estadio.restaurantes[seleccion_restaurante -1]                            
                    break
                except:
                    print("Error!")
            
            tipo_busqueda = input("""
                    Ingrese el número correspondiente al tipo de búsqueda de productos que desea realizar en este restaurante:
                    1.Búsqueda por Nombre
                    2.Búsqueda por tipo
                    3.Búsqueda por rango de precio
                    > """)
            
            while tipo_busqueda != '1' and tipo_busqueda != '2' and tipo_busqueda != '3':
                tipo_busqueda = input("Ingreso Inválido, ingrese el número correspondiente al tipo de búsqueda que desea realizar: ")
            
            if tipo_busqueda == '1':
                self.busqueda_producto_nombre(restaurante)
            elif tipo_busqueda == '2':
                self.busqueda_producto_tipo(restaurante)
            else:
                self.busqueda_producto_rango_precio(restaurante)
            
    def buy_restaurant(self):
        es_vip = False
        for i, cliente in enumerate(self.clientes):
            print(f"\t{i + 1}")
            cliente.mostrar()
        while True:
            try:                
                option = int(input("Introduzca el número del cliente que está ingresando actualmente a la base de datos: "))
                if option not in range(1, len(self.clientes) +1):
                    raise Exception
                cliente = self.clientes[option -1]
                break
            except:
                print("Error!")

        for ticket in cliente.tickets:
            if ticket.tipo_ticket == "Ticket VIP":
                es_vip = True
        if es_vip == False:
            print("No es usuario VIP de ninguno de los Tickets que ha comprado, por lo que no puede ver los productos de los restaurantes.")
        
        elif es_vip == True:
            for i, ticket in enumerate(cliente.tickets):
                if ticket.tipo_ticket == "Ticket VIP":
                    print(f"\t{i+1}")
                    ticket.mostrar()

                    while True:
                        try:
                            seleccion_ticket = int(input("Seleccione el número del Ticket VIP al cual desea ver el restaurante de su estadio: "))
                            if seleccion_ticket not in range(1, len(cliente.tickets) + 1):
                                raise Exception
                            ticket = cliente.tickets[seleccion_ticket - 1]
                            break
                        except:
                            print("Error!")
                    
            for partido in self.partidos:
                if ticket.id_partido == partido.id:
                    estadio = partido.estadio
            
            for i, restaurante in enumerate(estadio.restaurantes):
                print(f"\t{i+1}")
                print(f"\t{restaurante.nombre}")
            
            while True:
                try:
                    seleccion_restaurante = int(input("Seleccione el Restaurante en el que quiere comprar: "))
                    if seleccion_restaurante not in range(1, len(estadio.restaurantes) +1):
                        raise Exception
                    restaurante = estadio.restaurantes[seleccion_restaurante -1]                            
                    break
                except:
                    print("Error!")
            
            

    def start(self):
        print("""
    --------------------------------------------------------------------------------------------------------------    
    [....          [.       [... [......      [.       [.......                                                   
  [..    [..      [. ..          [..         [. ..     [..    [..        [. [..       [..      [. [..    [. [..   
[..       [..    [.  [..         [..        [.  [..    [..    [..       [.     [..  [..  [..  [.     [..[.     [..
[..       [..   [..   [..        [..       [..   [..   [. [..                [..  [..     [..      [..       [..  
[..       [..  [...... [..       [..      [...... [..  [..  [..            [..    [..      [..   [..       [..    
  [.. [. [..  [..       [..      [..     [..       [.. [..    [..        [..       [..    [..  [..       [..      
    [.. ..   [..         [..     [..    [..         [..[..      [..     [........    [...     [........ [........ 
         [.                                                                                                       
    --------------------------------------------------------------------------------------------------------------""")
        while True:
            opcion = input("""
            Selecciona el número de la acción que deseas realizar:
            1-Buscar partidos 
            2-Comprar Entrada
            3-Utilizar Boletos
            4-Búsqueda Productos en Restaurantes (Sólo para usuarios VIP)
            5-Compra en Restaurante (Sólo para usuarios VIP)
            6-Estadísticas
            7-Descargar datos de la API (Sobreescribir)
            8-Salir del programa
            > """)
            while opcion != '1' and opcion != '2' and opcion != '3' and opcion != '4' and opcion != '5' and opcion != '6' and opcion != '7' and opcion != '8':
                opcion = input("Ingreso inválido, introduzca el número de la acción que deseas realizar: ")
            
            if opcion == '1':
                self.search_match()
            elif opcion == '2':
                self.buy_tickets()
            elif opcion == '3':
                self.use_tickets()
            elif opcion == '4':
                self.restaurant_management()
            elif opcion == '5':
                self.buy_restaurant()
            elif opcion == '6':
                self.stats()
            elif opcion == '7':
                self.download()
            else:
                print("Hasta Luego!")
                break