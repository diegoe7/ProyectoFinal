import cv2
import numpy as np
from logs import get_logger
from DetecciónFiguras import clasificar

A_Contraste = 1500
Rangos_HSV = {
    "Rojo": [(np.array([0, 100, 80]), np.array([8, 255, 255])), (np.array([170, 100, 80]), np.array([180, 255, 255]))],
    "Naranja": [(np.array([10, 100, 100]), np.array([24, 255, 255]))],
    "Amarillo": [(np.array([25, 80, 100]), np.array([35, 255, 255]))],
    "Verde": [(np.array([36, 60, 60]), np.array([85, 255, 255]))],
    "Azul": [(np.array([86, 60, 60]), np.array([130, 255, 255]))],
}

def color_dominante(margen_hsv: np.ndarray, mask: np.ndarray) -> str | None:
    pixeles = int(np.count_nonzero(mask))

    if pixeles == 0:
        return None
    
    color = None
    pix = 0

    for nombre_color, rango in Rangos_HSV.items():
        mask_col = np.zeros_like(mask)
        for inferior, superior in rango:
            mask_col |= cv2.inRange(margen_hsv, inferior, superior)
        sobreposicion = cv2.bitwise_and(mask, mask_col)
        count = int(np.count_nonzero(sobreposicion))
        if count > pix:
            pix = count
            color = nombre_color

    if color is not None and pix / pixeles >=0.35:
        return color
    return None

class Detectar:
    def __init__(self, forma: str, color: str, contorno: np.ndarray, box: tuple[int, int, int, int], centro: tuple[int, int]):
        self.forma = forma
        self.color = color
        self.contorno = contorno
        self.box = box
        self.centro = centro

def detectar_figuras(margen: np.ndarray) -> list[Detectar]:
    items: list[Detectar] = []
    borroso = cv2.GaussianBlur(margen, (5, 5), 0)
    hsv = cv2.cvtColor(borroso, cv2.COLOR_BGR2HSV)
    gris = cv2.cvtColor(borroso, cv2.COLOR_BGR2GRAY)
    borde =cv2.Canny(gris, 50, 150)
    borde = cv2.dilate(borde, np.ones((3, 3), np.uint8), iterations=1)
    contornos, _ = cv2.findContours(borde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        if area < A_Contraste:
            continue
        perimetro = cv2.arcLength(contorno, True)

        if perimetro == 0:
            continue
        epsilon = 0.02 * perimetro
        aprox = cv2.approxPolyDP(contorno, epsilon, True)
        puntos = [(float(p[0][0]), float(p[0][1])) for p in aprox]

        if len(puntos) < 3:
            continue
        forma = clasificar(puntos)

        if forma == "Desconocido":
            continue
        mask = np.zeros(gris.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contorno], -1, 255, thickness=cv2.FILLED)
        color = color_dominante(hsv, mask)
        if color is None:
            continue
        x, y, w, h = cv2.boundingRect(contorno)
        M = cv2.moments(contorno)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = x + w // 2, y + h // 2
        items.append(Detectar(forma, color, contorno, (x, y, w, h), centro = (cx, cy)))
    return items
