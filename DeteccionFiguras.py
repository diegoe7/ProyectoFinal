import math
import numpy as np
from logs import get_logger

logger = get_logger(__name__)

def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])

def angulo(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    x1, x2 = a[0] - b[0], a[1] - b[1]
    y1, y2 = c[0] - b[0], c[1] - b[1]
    val1 = math.hypot(x1, y1)
    val2 = math.hypot(x2, y2)
    if val1 < 1e-9 or val2 < 1e-9:
        return 0.0
    cos_ang = max(-1.0, min(1.0,(x1 * x2 + y1 * y2) / (val1 * val2)))
    return math.degrees(math.acos(cos_ang))

def p_poligono(puntos: list[tuple[float, float]]) -> float:
    n = len(puntos)
    if n < 2:
        return 0.0
    return sum(dist(puntos[i], puntos[(i + 1) % n]) for i in range(n))

def a_poligono(puntos: list[tuple[float, float]]) -> float:
     arr = np.array(puntos)
     x, y = arr[:, 0], arr[:, 1]
     x_sig, y_sig = np.roll(x, -1), np.roll(y, -1)
     return float(abs(np.sum(x * y_sig - x_sig * y)) / 2.0)

def circularidad(puntos: list[tuple[float, float]]) -> float:
    perimetro = p_poligono(puntos)
    if perimetro < 1e-9:
        return 0.0
    area = a_poligono(puntos)
    return (4 * math.pi * area) / (perimetro ** 2)

def clasificar(puntos: list[tuple[float, float]]) -> str:
    n = len(puntos)
    if n < 3:
        return "Desconocido"
    if n >= 6:
        if circularidad(puntos) > 0.92:
            return "Circulo"
    if n == 3:
        return "Triangulo"
    if n == 4:
        angulos = [angulo(puntos[i - 1], puntos[i], puntos[(i + 1) % n]) for i in range(n)]
        if all(80 <= a <= 100 for a in angulos):
            return "Cuadrado"
        else:
            return "Rectangulo"
    if n in (5, 6):
        angulos = []
        for i in range(n):
            punto_ant = puntos[(i - 1) % n]
            punto_act = puntos[i]
            punto_sig = puntos[(i + 1) % n]
            angulos.append(angulo(punto_ant, punto_act, punto_sig))
        angulo_prom = sum(angulos) / n
        angulo_var = sum((a - angulo_prom) ** 2 for a in angulos) / n
        if angulo_var < 400.0:
            return "Hexagono"
        return "Desconocido"
    return "Desconocido"
