from dataclasses import dataclass
from datetime import datetime
import random
from logs import get_logger

logger = get_logger(__name__)

formas: set[str] = {"Cuadrado", "Triangulo", "Circulo", "Rectangulo", "Hexagono"}
colores: set[str] = {"Rojo", "Verde", "Azul", "Amarillo", "Naranja"}

orden_formas: list[str] = ["Cuadrado", "Triangulo", "Circulo", "Rectangulo", "Hexagono"]
orden_colores: list[str] = ["Rojo", "Verde", "Azul", "Amarillo", "Naranja"]


class ErrorJuego(Exception):
    pass

class CamaraNoEncontrada(ErrorJuego):
    pass

class DatosInvalidos(ErrorJuego):
    pass

class LeaderboardVacio(ErrorJuego):
    pass

@dataclass
class Jugador:
    nombre: str
    carrera: str

    def __post_init__(self) -> None:
        self.nombre = self.nombre.strip()
        self.carrera = self.carrera.strip()

        if not self.nombre or not self.carrera:
            logger.error("Datos inválidos al crear jugador")
            raise DatosInvalidos("El nombre y la carrera no pueden estar vacíos")

        logger.info(f"Jugador creado: {self.nombre} - {self.carrera}")

@dataclass
class Ronda:
    forma_el: str
    color_el: str
    f_check: bool
    c_check: bool
    t_check: bool
    tiempo: float

    @property
    def puntaje(self) -> int:
        return int(self.f_check) + int(self.c_check) + int(self.t_check)

class Partida:
    duracion = 20
    rondas = 3

    def __init__(self, jugador: Jugador) -> None:
        self.jugador = jugador
        self.rondas_jugadas: list[Ronda] = []
        self.puntaje_c: dict[str, int] = {color: 0 for color in orden_colores}
        self.puntaje_f: dict[str, int] = {forma: 0 for forma in orden_formas}
        self.fyc_usados: set[tuple[str, str]] = set()

        logger.info(f"Partida iniciada para {jugador.nombre}")

    def siguiente_fig(self) -> tuple[str, str]:
        disp = [
            (forma, color)
            for forma in formas
            for color in colores
            if (forma, color) not in self.fyc_usados
        ]

        if not disp:
            self.fyc_usados.clear()
            disp = [(f, c) for f in formas for c in colores]

        elec = random.choice(disp)
        self.fyc_usados.add(elec)

        logger.info(f"Nueva figura objetivo: {elec}")

        return elec

    def res_ronda(self, resultado: Ronda) -> None:
        self.rondas_jugadas.append(resultado)

        if resultado.c_check:
            self.puntaje_c[resultado.color_el] += 1
        if resultado.f_check:
            self.puntaje_f[resultado.forma_el] += 1

        logger.info(
            f"Ronda registrada: {resultado.forma_el} {resultado.color_el} "
            f"puntaje={resultado.puntaje}"
        )

    @property
    def puntaje_total(self) -> int:
        return sum(r.puntaje for r in self.rondas_jugadas)

    def terminado(self) -> bool:
        return len(self.rondas_jugadas) >= self.rondas

    def resultado(self) -> "Record":
        logger.info("Generando resultado final de la partida")

        return Record(
            jugador=self.jugador.nombre,
            carrera=self.jugador.carrera,
            puntaje=self.puntaje_total,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            puntaje_c=dict(self.puntaje_c),
            puntaje_f=dict(self.puntaje_f)
        )

@dataclass
class Record:
    jugador: str
    carrera: str
    puntaje: int
    fecha: str
    puntaje_c: dict
    puntaje_f: dict
