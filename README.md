# Proyecto: Topography report
## Descripción
Realiza un reporte de topología en formato PDF dado una lista de coordenadas.

Dado una lista de puntos [P1, P2, ..., PN] donde Pi es la coordenada (xi, yi) para _**i = 1..N**_ que representa puntos de un polígono en un plano 2D

[Polygon](screenshots/polygon.jpg)

_**Nota**: Para el cliente el eje X es vertical y el je Y horizontal tal como se muestra la imagen. Además los puntos se dá en sentido horario._

el programa calcula los valores de:
* Ángulos internos
* Azimuts
* Distancia de P1 a P2, de P2 a P3, ..., de PN a P1

Además de ingresar la lista de puntos, tiene la opción de llenar un formulario el cual consta de:
* Plano de...
* Propiedad
* Ubicación
* Perito _(el cual por defecto vene el nombre del cliente)_
* Propietario
* Fecha
