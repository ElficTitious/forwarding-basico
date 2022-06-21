from dataclasses import dataclass
import ipaddress

@dataclass
class IPHeader:
  """Data class usada para representar un header IP.

  Attributes:
  -----------
  ip_address (str): Dirección IP donde se encuentra escuchando el router
                    de destino del paquete.
  port (int): Puerto en que se encuentra escuchando el router de destino
              del paquete en la IP ip_address.
  msg (str): Mensaje siendo enviado en el paquete.
  """

  ip_address: str
  port: int
  msg: str

@dataclass
class RoutingTableLine:
  """Data class usada para representar una línea de una tabla de ruteo.

  Attributes:
  -----------
  possible_ip_addresses (list[str]): Lista con todas las potenciales direcciones
                                     IP generadas a partir de una red (CIDR).
  initial_port (int): Inicio del rango de puertos.
  final_port (int): Fin del rango de puertos.
  landing_ip (str): Dirección IP donde redirigir dados los valores anteriores
  landing_port (int): Puerto donde redirigir dados los primeros dos valores y la IP 
                      anterior
  """

  possible_ip_addresses: list[str]
  initial_port: int
  final_port: int
  landing_ip: str
  landing_port: int

def parse_ip_header(ip_header: str) -> IPHeader:
  """Función encargada de, dado un header IP representado como
  un string de la forma [Dirección IP],[Puerto],[mensaje], retornar
  un objeto de la data class IPHeader.

  Parameters:
  -----------
  ip_header (str): Header IP representado como un string de la forma 
                   [Dirección IP],[Puerto],[mensaje]
  
  Returns:
  --------
  (IPHeader): Instancia de la data class representando el mismo header ip
              pasado como parámetro
  """

  # Extraemos el contenido del header
  packet_contents_list = ip_header.split(',')

  # Guardamos el contenido en variables ad-hoc
  ip_address = packet_contents_list[0]
  port = int(packet_contents_list[1])
  msg = packet_contents_list[2]

  # Retornamos el contenido empaquetado en una instancia de IPHeader
  return IPHeader(ip_address, port, msg)

def parse_routing_table_line(routing_table_line: str) -> RoutingTableLine:
  """Función que dada una linea de una tabla de ruteo, de la forma
  [Red (CIDR)] [Puerto_Inicial] [Puerto_final] [IP_Para_llegar] [Puerto_para_llegar],
  la parsea retornando una instancia de RoutingTableLine.

  Parameters:
  -----------
  routing_table_line (str): Linea de una tabla de ruteo, la cual debe ser de la forma
                            [Red (CIDR)] [Puerto_Inicial] [Puerto_final] [IP_Para_llegar] [Puerto_para_llegar].
  
  Returns:
  --------
  (RoutingTableLine): Linea de la tabla de ruteo pasada como parametro, pero parseada y empaquetada
                      en una instancia de la data class RoutingTableLine.
  """

  # Comenzamos por extraer el contenido de la línea en una lista
  routing_table_line_contents_list = routing_table_line.split(' ')

  # Guardamos el contenido en variables ad-hoc
  cidr_net = routing_table_line_contents_list[0]
  initial_port = int(routing_table_line_contents_list[1])
  final_port = int(routing_table_line_contents_list[2])
  landing_ip = routing_table_line_contents_list[3]
  landing_port = int(routing_table_line_contents_list[4])

  # Generamos la lista con todas las potenciales direcciones IP generadas 
  # a partir de la red (CIDR) presente en la linea.
  possible_ip_addresses = [str(ip) for ip in ipaddress.IPv4Network(cidr_net)]

  # Retornamos la instancia de RoutingTableLine
  return RoutingTableLine(possible_ip_addresses, initial_port, 
                          final_port, landing_ip, landing_port)

def traverse_routing_table(routing_table_file_name: str, 
                           destination_address: tuple[str, int]) -> tuple[str, int] | None:
  """Función que dado el npombre de un archivo conteniendo una tabla de ruteo, y un par
  (destination_ip, destination_port), revisa en orden, linea por linea, la tabla de ruteo,
  buscando hacia donde redirigir un paquete destinado a la dirección dada como segundo parámetro.
  De encontrar una dirección donde redirigir se retorna dicho par, de lo contrario se retorna None.

  Parameters:
  -----------
  routing_table_file_name (str): Nombre de un archivo conteniendo la tabla de ruteo a recorrer.
  destination_address (tuple[str, int]): Par (destination_ip, destination_port) a buscar en la
                                         tabla de ruteo.
  
  Returns:
  --------
  (tuple[str, int] | None): De encontrar una dirección donde redirigir se retorna dicho par en la forma
                            (next_hop_IP, next_hop_port), pero de recorrer la tabla completa y no encontrar
                            una ruta apropiada, se retorna None.
  """

  # Desempaquetamos la dirección de destino por facilidad de uso
  destination_ip, destination_port = destination_address

  # Abrimos el archivo que contiene la tabla de ruteo y leemos sus lineas
  routing_table_file = open(routing_table_file_name, 'r')
  routing_table_lines = routing_table_file.readlines()

  # Iteramos sobre las lineas
  for line in routing_table_lines:

    # Parseamos la línea
    routing_table_line = parse_routing_table_line(line.strip('\n'))

    # Revisamos si en la linea actual se indica como hacer forward para la dirección de destino
    if (destination_ip in routing_table_line.possible_ip_addresses and 
        destination_port in range(routing_table_line.initial_port, routing_table_line.final_port + 1)):
      
      # De ser el caso retornamos la dirección a la cual hacer forward
      next_hop_ip, next_hop_port = (routing_table_line.landing_ip, routing_table_line.landing_port)
      return (next_hop_ip, next_hop_port)

  # De no encontrar ninguna ruta apropiada, retornamos None
  return None
  
