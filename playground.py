from utilities import *

ip_header = parse_ip_header('127.0.0.1,8881,255,hola')
print(ip_header)