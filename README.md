# Actividad: Forwarding Básico

Semana 10-11: Redes IP, Módulo 4: Redes y Ruteo, CC4303-1

## Ejecución

Para ejecutar es necesario correr cada router en una ventana de terminal distinta, y enviar mensajes al router deseado usando `netcat`.
Cada router necesita como argumentos la IP del router y su puerto, sumado al nombre del archivo en que se encuentran sus tablas de ruta.

Adicionalmente es posible probar el funcionamiento del sistema ejecutando el archivo `prueba_router.py` con los headers asociados al destino de los paquetes a enviar (los cuales deben ser de la forma `[IP_destino],[puerto_destino],[TTL]`), y la dirección del router de inicio. Con lo cual se envían todas las lineas en `test_file.txt` sumado a los headers, a la dirección de destino.

**Ejecución:

Para correr cada router se debe pasar la IP del router y su puerto, sumado al nombre del archivo en que se encuentran sus tablas de ruta.

Ejemplo:

```bash
python3 router.py 127.0.0.1 8881 rutas/v1/R1.txt
```
Para ejecutar la prueba de routers se deben incluir los header a agregar a cada linea de `test_file.txt`, sumado a la IP del router de inicio y su puerto.

Ejemplo:

```bash
python3 prueba_router.py 127.0.0.1,8885,10 127.0.0.1 8881
```

## Funcionamiento

La lógica de un router se encuentra dentro del script `router.py`, y todas las funcionalidades auxiliares dentro de `utilities.py`. Puesto que está todo documentado dentro de los respectivos archivos, se procede solo a explicar las decisiones de diseño asociadas a la implementación de round robin.

### Funcionamiento round robin:

Se implementa round robin via una clase `RoundRobinRoutingTable`, la cual es instanciada con el nombre que contiene la tabla de rutas de un router. Esta clase de manera subyacente contiene un diccionario con direcciones de destino mapeadas a arreglos circulares (instancia de la clase `CircularArrayWithPointer`), donde los arreglos circulares solo exponen un método que permite solicitar el siguiente elemento en el arreglo, y de no existir ningun elemento en el arreglo se retorna siempre `None` (esto es especialmente útil al momento de pedir el siguiente salto para una ruta que el router no posee en su tabla de rutas).

Veamos que la clase `RoundRobinRoutingTable` expone a su vez el método `next_hop()`, el cual toma la dirección de destino a la cual se pretende llegar, y retorna la siguiente dirección a la cual hacer forward dada por el arreglo circular (de no exitir una forma se retorna `None` aprovechando el comportamiento del arreglo circular). Ahora, si al invocar `next_hop()` no se tiene información en el diccionario respecto a la dirección de destino, se construye una nueva entrada asociada al arreglo circular de posibles formas de hacer forward.
