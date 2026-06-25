import time
from Bases import Ronda
from detector_de_colores import Detectar

class Controlador:
    
    def __init__(self, figura_el: str, color_el: str, duracion: int = 20):
        self.figura_el = figura_el
        self.color_el = color_el
        self.duracion = duracion
        self.tiempo_inicio = time.monotonic()
        self.f_check = False
        self.c_check = False
        self.t_check = False
        self.ronda_finalizada = False
        self.tiempo_finalizado: float | None = None

    def actualizar(self, detecciones: list) -> None:
        if self.ronda_finalizada:
            return
        for det in detecciones:
            fig_corr = det.forma == self.figura_el
            col_corr = det.color == self.color_el
            if fig_corr:
                self.f_check = True
            if col_corr:
                self.c_check = True
            if fig_corr and col_corr:
                self.t_check = True
        if self.t_check or self.tiempo_restante() <= 0:
            self.fin()

    def tiempo_restante(self) -> float:
        pasado = time.monotonic() - self.tiempo_inicio
        return max(0.0, self.duracion - pasado)

    def finalizar(self) -> bool:
        return self.ronda_finalizada

    def fin(self) -> None:
        self.ronda_finalizada = True
        self.tiempo_finalizado = time.monotonic()

    def resultado_ronda(self) -> Ronda:
        if self.tiempo_finalizado is None:
            self.fin()
        duracion = self.tiempo_finalizado - self.tiempo_inicio
        return Ronda(
            forma_el=self.figura_el,
            color_el=self.color_el,
            f_check=self.f_check,
            c_check=self.c_check,
            t_check=self.t_check,
            tiempo=duracion,
        )
