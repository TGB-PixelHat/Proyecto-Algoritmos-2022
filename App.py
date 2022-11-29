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
import pickle
import os

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
            self.equipos.clear()
            self.estadios.clear()
            self.partidos.clear()
            self.clientes.clear()
            self.codigos_usados.clear()
            self.codigos_ticket.clear()
            #Descarga los datos de los equipos
            var = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json")
            equipos = var.json()
            for team in equipos:
                team = Equipo(team['name'], team["fifa_code"], team['group'], team['flag'], team['id'])
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
                            producto = Alimento(product["name"], product["quantity"], product["price"], product["type"], product["adicional"])
                        elif product["type"] == 'beverages':
                            producto = Bebida(product["name"], product["quantity"], product["price"], product["type"], product["adicional"])
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
            print()
    
    def show_stadiums(self):
        """
        Muestra los datos de todos los estadios de la base de datos
        """
        for estadio in self.estadios:
            print()
            estadio.mostrar()
            print()
    
    def show_matches(self):
        """
        Muestra todos los datos de los partidos de la base de datos
        """
        for partido in self.partidos:
            print()
            partido.mostrar()
            print()

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
                    partido.mostrar()
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
                    partido.mostrar()
                  
        else:            
            while True:
                try:
                    fecha = input("""Introduzca la fecha de la cual quiere buscar los partidos
                    (Formato MM/DD/YYYY si un día tiene 1 solo dígito copie sólo ese dígito sin un 0 en frente): """)
                    if len(fecha) > 10:
                        raise Exception
                    if fecha.count("/") != 2:
                        raise Exception                    
                    for caracter in fecha:
                        if not caracter.isnumeric() and not "/":
                            raise Exception
                    if fecha[2] != '/' and fecha[5] != '/':
                        raise Exception
                    break
                except:
                    print("Error!")
            
            comprobante = False
            for partido in self.partidos:
                if fecha in partido.fecha_y_hora:
                    partido.mostrar()
                    comprobante = True
            
            if comprobante == False:
                print("No hay ningún partido en la fecha que usted marcó, por favor intente de nuevo")

    def create_code(self):
        """
        Genera un código al azar para el ticket, si el código del Ticket ya existe lo hace de nuevo
        Retorna: Código generado
        """
        codigo_ticket = random.randint(1000000, 9999999)
        while codigo_ticket in self.codigos_ticket:            
            codigo_ticket = random.randint(1000000, 9999999)
        return codigo_ticket

    def buy_tickets(self):
        """
        Registra al cliente y hace que seleccione el ID del partido que quiere comprarle un ticket
        Después se selecciona el tipo de Ticket que quiere comprar junto con el asiento que va a ocupar
        Se calcula la factura y se enseña, preguntando por confirmación del pago
        Si el pago se confirma, se le añade la factura al cliente, si se cancela no se le añade y se cancela todo lo hecho anteriormente
        """
        
        while True:
            try:
                cedula = int(input("Ingrese su cédula: "))
                if cedula <= 0:
                    raise Exception
                break
            except:
                print("Error!")
        
        comprobante_cliente = False
        for client in self.clientes:
            if cedula == client.cedula:
                comprobante_cliente = True
                cliente = client

        if comprobante_cliente == False:
            while True:
                try:
                    name = input("Introduzca su nombre: ").title()
                    if not name.isalpha() or name.isspace():
                        raise Exception
                    edad = int(input("Introduzca su edad: "))
                    if edad <= 5 or edad >= 118:
                        raise Exception
                    break
                except:
                    print("Error! Intente de nuevo")
        
        self.show_matches()
        while True:
            try:
                option = int(input("Seleccione el Id del partido al que desea comprarle la entrada: "))
                if option not in range(1, len(self.partidos) + 1):
                    print("Ingreso Inválido")
                    raise Exception
                
                for match in self.partidos:
                    if str(option) == match.id:
                        partido = match

                tipo_ticket = input("Introduzca el tipo de ticket que desea comprar (1-General   2-VIP): ")
                if tipo_ticket != '1' and tipo_ticket != '2':
                    print("Ingreso Inválido")
                    raise Exception
                
                if partido.general_comprados == partido.estadio.capacidad[0] and tipo_ticket == '1':
                    print("Ya se alcanzó el límite de Tickets generales para este partido, intente en otro partido u otro tipo de ticket")
                    raise Exception
                if partido.vip_comprados == partido.estadio.capacidad[1] and tipo_ticket == '2':
                    print("Ya se alcanzó el límite de Ticket VIP para este partido, intente en otro partido u otro tipo de ticket")
                    raise Exception
                break
            except:
                print("")
                       
        
        partido.mapa()

        while True:
            try:
                asiento = input("Introduzca el número de asiento en el que quiere sentarse (Formato: N-N): ")
                comprobante = False
                for caracter in asiento:
                    if not caracter.isnumeric() and not "-":
                        raise Exception
                for fila in partido.asientos:
                    if asiento in fila:
                        comprobante = True
                if asiento in partido.asientos_tomados:
                    raise Exception
                if comprobante == False:
                    raise Exception
                break
            except:
                print("Error! Intente de nuevo")
        
        partido.asientos.clear()

        codigo_ticket = self.create_code()
        if tipo_ticket == '1':
            ticket = TicketGeneral(codigo_ticket, option, asiento, False)
        elif tipo_ticket == '2':
            ticket = TicketVIP(codigo_ticket, option, asiento, False)
        
        if comprobante_cliente == True:
            cliente.tickets.append(ticket)
            factura = cliente.crear_factura(ticket)
        
        if comprobante_cliente == False:
            cliente = Cliente(name, cedula, edad)
            cliente.tickets.append(ticket)
            factura = cliente.crear_factura(ticket)

        continuar = input("Desea continuar con el pago? 1.Si  2.No: ")
        while continuar != '1' and continuar != '2':
            continuar = input("Ingreso Inválido, desea continuar con el pago? 1.Si  2.No: ")

        if continuar == '1':
            if comprobante_cliente == False:
                self.clientes.append(cliente)
            partido.asientos_tomados.append(asiento)
            self.codigos_ticket.append(codigo_ticket)
            cliente.facturas.append(factura)
            cliente.mostrar()
            print("\Pago realizado exitosamente!")
            if tipo_ticket == '1':
                partido.general_comprados += 1
            elif tipo_ticket == '2':
                partido.vip_comprados += 1
        
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
        if len(self.clientes) == 0:
            print("No hay clientes registrados para realizar esta acción")
        else:
            for i, cliente in enumerate(self.clientes):
                print(f"\t{i + 1}")
                print(f"""
                Nombre: {cliente.nombre}
                Cédula: {cliente.cedula}""")
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
                        if int(ticket.id_partido) == int(partido.id):
                            partido.asistencia.append(cliente)
                            self.codigos_usados.append(ticket.codigo_ticket)
                            print("Asistencia Registrada exitosamente!")
                else:
                    print("Este Ticket ya ha sido registrado previamente, intente con otro ticket")
            else:
                print("El código de este ticket no se encuentra en nuestra base de datos")

    def busqueda_producto_nombre(self, restaurante):
        """
        Busca los productos del restaurante y los muestra a partir del Nombre (Cliente debe saber el nombre del producto antes)

        Recibe: El objeto de restaurante al que se le va a realizar la acción
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

        Recibe: El objeto Restaurante al que se le quiere realizar la acción
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
        
        Recibe: El objeto del restaurante al que se quiere realizar la acción
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

        comprobante = False
        for producto in restaurante.productos:
            if producto.precio in range(x, y+1):
                producto.mostrar()
                comprobante = True

        if comprobante == False:
            print("\t No existen productos en el rango de precio indicado")
    
    def restaurant_management(self):
        """
        Revisa si el cliente que entró existe, si posee algún ticket VIP y que de ese ticket VIP a cuál restaurante quiere verle la estadística
        """
        if len(self.clientes) == 0:
            print("No hay clientes registrados para realizar esta acción")
        else:
            es_vip = False
            cliente_existe = False
            while True:
                try:                
                    option = int(input("Introduzca su número de cédula: "))
                    for user in self.clientes:
                        if user.cedula == option:
                            cliente_existe = True
                            cliente = user
                    
                    if cliente_existe == False:
                        raise Exception                
                    break
                except:
                    print("Error! Introdujo un número inválido o la cédula que introdujo no se encuentra en nuestra base de datos")

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
                        print()

                while True:
                    try:
                        seleccion_ticket = int(input("Seleccione el número del Ticket VIP al cual desea ver el restaurante de su estadio: "))
                        if seleccion_ticket not in range(1, len(cliente.tickets) + 1):
                            raise Exception
                        if cliente.tickets[seleccion_ticket -1].tipo_ticket != "Ticket VIP":
                            raise Exception
                        ticket = cliente.tickets[seleccion_ticket - 1]
                        break
                    except:
                        print("Error!")
                        
                for partido in self.partidos:
                    if ticket.id_partido == int(partido.id):
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
        """
        Revisa si el cliente que entró existe, si posee algún ticket VIP y que de ese ticket VIP de cuál restaurante quiere comprar
        Va comprando los productos y cantidades de dicho restándole al stock del producto, después se confirma si quiere realizar el pago
        Si dice que no se revierten los cambios, si dice que si se crea la factura
        """
        es_vip = False
        cliente_existe = False
        if len(self.clientes) == 0:
            print("No hay clientes registrados que puedan comprar")
        else:
            while True:
                try:                
                    option = int(input("Introduzca su número de cédula: "))
                    for user in self.clientes:
                        if user.cedula == option:
                            cliente_existe = True
                            cliente = user
                    
                    if cliente_existe == False:
                        raise Exception                
                    break
                except:
                    print("Error! Introdujo un número inválido o la cédula que introdujo no se encuentra en nuestra base de datos")

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
                        print()

                while True:
                    try:
                        seleccion_ticket = int(input("Seleccione el número del Ticket VIP al cual desea ver el restaurante de su estadio: "))
                        if seleccion_ticket not in range(1, len(cliente.tickets) + 1):
                            raise Exception
                        if cliente.tickets[seleccion_ticket -1].tipo_ticket != "Ticket VIP":
                            raise Exception
                        ticket = cliente.tickets[seleccion_ticket - 1]
                        break
                    except:
                        print("Error!")
                        
                for partido in self.partidos:
                    if ticket.id_partido == int(partido.id):
                        estadio = partido.estadio
                
                for i, restaurante in enumerate(estadio.restaurantes):
                    print(f"\t{i+1}")
                    print(f"\t{restaurante.nombre}")
                    print()
                
                while True:
                    try:
                        seleccion_restaurante = int(input("Seleccione el Restaurante en el que quiere comprar: "))
                        if seleccion_restaurante not in range(1, len(estadio.restaurantes) +1):
                            raise Exception
                        restaurante = estadio.restaurantes[seleccion_restaurante -1]                            
                        break
                    except:
                        print("Error!")
                
                for i, producto in enumerate(restaurante.productos):
                    print(f"\t {i+1}")
                    producto.mostrar()
                    print("")
                
                productos_comprados = []

                while True:
                    while True:
                        try:
                            id = int(input("Introduzca el número del producto que desea comprar: "))
                            if id not in range(1, len(restaurante.productos) +1):
                                print("Error!")
                                raise Exception
                            if cliente.edad < 18 and restaurante.productos[id-1].adicional == 'alcoholic':
                                print("Eres menor de edad, por lo tanto no puedes pedir bebidas alcohólicas")
                                raise Exception
                            producto = restaurante.productos[id -1]

                            cantidad = int(input("Introduzca la cantidad que quiere comprar de este producto: "))
                            if cantidad <= 0 or producto.cantidad < cantidad:
                                print("Error!")
                                raise Exception
                            break
                        except:
                            print("")

                    comprobante_producto = False
                    for item in productos_comprados:
                        if producto.nombre == item["producto"].nombre:
                            item["cantidad"] += cantidad
                            producto.cantidad -= cantidad
                            producto.vendido += cantidad
                            comprobante_producto = True

                    if comprobante_producto == False:
                        productos_comprados.append({
                            "producto": producto,
                            "cantidad": cantidad
                        })
                        producto.cantidad -= cantidad
                        producto.vendido += cantidad
                    
                    detener = input("Desea comprar otro producto? (1.Si  2.No): ")
                    while detener != '1' and detener != '2':
                        detener = input("Ingreso Inválido, desea comprar otro producto? (1.Si  2.No): ")

                    if detener == '2':
                        break
                
                factura = cliente.crear_factura_restaurante(ticket, productos_comprados)
                
                confirmar = input("Desea confirmar su compra? (1.Si  2.No): ")
                while confirmar != '1' and confirmar != '2':
                    confirmar = input("Ingreso Inválido. Desea confirmar su compra? (1.Si  2.No): ")
                
                if confirmar == '1':
                    cliente.facturas.append(factura)
                    print("Pago realizado exitosamente!")
                else:
                    for item in productos_comprados:
                        for producto in restaurante.productos:
                            if item["producto"].nombre == producto.nombre:
                                producto.cantidad += item["cantidad"]
                                producto.vendido -= item["cantidad"]
                    print("Pago cancelado exitosamente")

    def gasto_promedio(self):
        """
        Determina primero cual es el cliente al que se le quiere realizar la estadística y si el cliente es vip
        Una vez determinado calcula el promedio gastado en un partido en específico mediante el uso del ticket
        """
        es_vip = False
        cliente_existe = False
        while True:
            try:                
                option = int(input("Introduzca el número de cédula del Cliente VIP del que quiere ver el gasto promedio: "))
                for user in self.clientes:
                    if user.cedula == option:
                        cliente_existe = True
                        cliente = user
                
                if cliente_existe == False:
                    raise Exception                
                break
            except:
                print("Error! Introdujo un número inválido o la cédula que introdujo no se encuentra en nuestra base de datos")

        for ticket in cliente.tickets:
            if ticket.tipo_ticket == "Ticket VIP":
                es_vip = True
        if es_vip == False:
            print("El cliente que seleccionó no es cliente VIP en ninguno de los partidos del mundial.")
        
        for i, ticket in enumerate(cliente.tickets):
                if ticket.tipo_ticket == "Ticket VIP":
                    print(f"\t{i+1}")
                    ticket.mostrar()
                    print()

        while True:
            try:
                seleccion_ticket = int(input("Seleccione el número del Ticket VIP al cual desea ver el gasto promedio: "))
                if seleccion_ticket not in range(1, len(cliente.tickets) + 1):
                    raise Exception
                if cliente.tickets[seleccion_ticket -1].tipo_ticket != "Ticket VIP":
                    raise Exception
                ticket = cliente.tickets[seleccion_ticket - 1]
                break
            except:
                print("Error!")
        
        contador = 0
        sumatoria_total = 0
        promedio_gastado = 0
        for factura in cliente.facturas:
            if factura.id_partido == ticket.id_partido:
                sumatoria_total += factura.total
                contador += 1
        
        promedio_gastado = sumatoria_total / contador

        print(f"""
        El cliente de nombre: {cliente.nombre}
        Tuvo un gasto promedio de: {promedio_gastado}$
        En el partido de Id: {ticket.id_partido}""")

    def ordenar_asistencia(self, partido):
        """
        Ordena los partidos según su asistencia
        
        Recibe: El objeto partido

        Retorna: La longitud de la lista de asistencia del objeto partido
            
        """
        return len(partido.asistencia)

    def tabla_asistencia(self):
        """
        Muestra por orden de mayor a menor los datos de los partidos con mayor y menor asistencia
        """
        partidos = []
        for partido in self.partidos:
            partidos.append(partido)

        partidos.sort(reverse = True, key=self.ordenar_asistencia)

        for partido in partidos:
            partido.mostrar()
            print(f"\tCantida de tickets comprados: {len(partido.asientos_tomados)}")
            print(f"\tPersonas que Asistieron: ")
            if len(partido.asistencia) != 0:
                for persona in partido.asistencia:
                    print(f"""
                        Nombre: {persona.nombre}
                        Cédula:{persona.cedula}""")
            else:
                print("""
                        Ninguna""")
            print()
            print(f"\tRelación asistencia/venta: ")
            if len(partido.asientos_tomados) > 0:
                print(f"""
                        {partido.asistencia//len(partido.asientos_tomados)}""")
            else:
                print("""
                        Ninguna""")
        partidos.clear()

    def partido_mayor_asistencia(self):
        """
        Itera sobre la lista de self.partidos para determinar cuál fue el partido con mayor asistencia
        Al finalizar muestra los datos del partido que obtuvo mayor asistencia
        """
        mayor_asistencia = self.partidos[0]
        for partido in self.partidos:
            if len(partido.asistencia) > len(mayor_asistencia.asistencia):
                mayor_asistencia = partido
        
        if len(mayor_asistencia.asistencia) != 0:
            print("\tEl partido que tuvo la mayor asistencia fue: ")
            mayor_asistencia.mostrar()
        else:
            print("\tNo ha habido asistencia en ninguno de los partidos para poder realizar esta estadística")

    def partido_boletos_vendidos(self):
        """
        Itera sobre la lista de self.partidos para determinar cuál tuvo la mayor cantidad de boletos vendidos
        Al finalizar muestra los datos del partido que vendió más boletos
        """
        mayor_boletos = self.partidos[0]
        for partido in self.partidos:
            if len(partido.asientos_tomados) > len(mayor_boletos.asientos_tomados):
                mayor_boletos = partido
        
        if len(mayor_boletos.asientos_tomados) != 0:
            print("\tEl partido que vendió la mayor cantidad de boletos fue: ")
            mayor_boletos.mostrar()
        else:
            print("\tNo se han vendido boletos en los partidos todavía para hacer esta estadística")

    def top_productos(self):
        """
        Calcula y enseña los 3 productos que fueron más vendidos en el restaurante que el cliente quiera escoger
        """
        top = []
        self.show_stadiums()

        while True:
            try:
                option = int(input("Seleccione el Id del estadio al que quiere acceder para la estadística: "))
                if option not in range(1, len(self.estadios) + 1 ):
                    raise Exception    
                for stadium in self.estadios:
                    if option == stadium.id:
                        estadio = stadium
                break
            except:
                print("Error!")
        
        for i, restaurante in enumerate(estadio.restaurantes):
            print(f"\t {i+1}")
            print(f"\t {restaurante.nombre}")

        while True:
            try:
                option = int(input("Seleccione el número correspondiente al Restaurante al que quiere acceder: "))
                if option not in range(1, len(estadio.restaurantes) +1):
                    raise Exception
                restaurante = estadio.restaurantes[option -1]
                break
            except:
                print("Error!")
        
        for producto in restaurante.productos:
            if len(top) < 3 and producto.vendido > 0:
                top.append(producto)
            elif len(top) == 3:
                for item in top:
                    if producto.vendido > item.vendido:
                        item = producto
        
        if len(top) != 0:            
            print("\tEstos son el top de productos vendidos: ")
            for i, producto in enumerate(top):
                print(f"\t{i+1}")
                print(f"""
                Nombre del producto: {producto.nombre}
                Cantidad vendida: {producto.vendido}""")
        else:
            print("No hay productos vendidos con los cuales hacer esta estadística")
        top.clear()

    def top_clientes(self):
        """
        Calcula y muestra los 3 clientes que compraron más tickets de la base de datos
        En caso de haber menos de 3 clientes sólo muestra los clientes que hay (1 o 2 clientes)
        """
        top = []

        for cliente in self.clientes:
            if len(top) < 3 and len(cliente.tickets) > 0:
                top.append(cliente)
            elif len(top) == 3:
                for customer in top:
                    if len(cliente.tickets) > len(customer.tickets):
                        customer = cliente
        
        if len(top) != 0:
            for i, cliente in enumerate(top):
                print("\tEstos son el top de clientes que compraron más boletos: ")
                print(f"\t{i+1}")
                print(f"""
            Nombre: {cliente.nombre}
            Cedula: {cliente.cedula}""")
        else:
            print("No hay clientes con los cuales hacer esta estadística")

    def stats(self):
        """
        Menú de estadísticas
        """
        option = input("""
        Bienvenido al menú de estadísticas, selecciona el número correspondiente a la estadística que deseas ver:
        1-Gasto promedio de un cliente VIP en un partido
        2-Tabla de asistencia de los partidos
        3-Partido con mayor asistencia
        4-Partido con mayor boletos vendidos
        5-Top 3 productos vendidos en el restaurante
        6-Top 3 clientes
        > """)
        while option != '1' and option != '2' and option != '3' and option != '4' and option != '5' and option != '6':
            option = input("Ingreso inválido, selecciona el número correspondiente a la estadística que deseas ver: ")
        if option == '1':
            self.gasto_promedio()
        elif option == '2':
            self.tabla_asistencia()
        elif option == '3':
            self.partido_mayor_asistencia()
        elif option == '4':
            self.partido_boletos_vendidos()
        elif option == '5':
            self.top_productos()
        elif option == '6':
            self.top_clientes()

    def read(self):
        """
        Primero revisa si el archivo a leer existe, si el archivo no existe, lo crea
        Si el archivo existe revisa si está o no está vacío, si está vacío no lee el archivo
        Si el archivo no está vacio, hace pickle.load para leer el archvio y se iguala a la variable a sobreescribir
        """
        if os.path.exists('clientes.txt'):
            if os.path.getsize('clientes.txt') != 0:
                with open('clientes.txt', 'rb') as a:
                    self.clientes = pickle.load(a)
        else:
            with open('clientes.txt', 'x'):
                pass
        
        if os.path.exists('equipos.txt'):
            if os.path.getsize('equipos.txt') != 0:
                with open('equipos.txt', 'rb') as a:
                    self.equipos = pickle.load(a)
        else:
            with open('equipos.txt', 'x'):
                pass
        
        if os.path.exists('estadios.txt'):
            if os.path.getsize('estadios.txt') != 0:
                with open('estadios.txt', 'rb') as a:
                    self.estadios = pickle.load(a)
        else:
            with open('estadios.txt', 'x'):
                pass

        if os.path.exists('partidos.txt'):
            if os.path.getsize('partidos.txt') != 0:
                with open('partidos.txt', 'rb') as a:
                    self.partidos = pickle.load(a)
        else:
            with open('partidos.txt', 'x'):
                pass
        
        if os.path.exists('codigos_usados.txt'):
            if os.path.getsize('codigos_usados.txt') != 0:
                with open('codigos_usados.txt', 'rb') as a:
                    self.codigos_usados = pickle.load(a)
        else:
            with open('codigos_usados.txt', 'x'):
                pass

        if os.path.exists('codigos_ticket.txt'):
            if os.path.getsize('codigos_ticket.txt') != 0:
                with open('codigos_ticket.txt', 'rb') as a:
                    self.codigos_ticket = pickle.load(a)
        else:
            with open('codigos_ticket.txt', 'x'):
                pass

    def write(self):
        """
        Guarda todos los datos hechas en las listas principales del programa en sus respectivos archivos txt
        No se valida que el archivo exista porque eso sucede al inicio del programa
        """
        with open('clientes.txt', 'wb') as a:
            pickle.dump(self.clientes, a)
        with open('equipos.txt', 'wb') as a:
            pickle.dump(self.equipos, a)
        with open('estadios.txt', 'wb') as a:
            pickle.dump(self.estadios, a)
        with open('partidos.txt', 'wb') as a:
            pickle.dump(self.partidos, a)
        with open('codigos_usados.txt', 'wb') as a:
            pickle.dump(self.codigos_usados, a)
        with open('codigos_ticket.txt', 'wb') as a:
            pickle.dump(self.codigos_ticket, a)

    def start(self):       
        self.read()
        
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
                self.write()
                break