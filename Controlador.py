import time
from Bases import Ronda
<<<<<<< HEAD


class Controlador:

    def __init__(self, forma_el: str, color_el: str, duracion: int = 20):
        self.forma_el = forma_el
        self.color_el = color_el
        self.duracion = duracion

        self.tiempo_inicio = time.monotonic()

        self.fig_correcta = False
        self.col_correcta = False
        self.fyc_correcta = False

        self.ronda_finalizada = False
        self.tiempo_finalizado = None


    def actualizar(self, detecciones: list) -> None:
        if self.ronda_finalizada:
            return

        for det in detecciones:
            fig_ok = det.forma == self.forma_el
            col_ok = det.color == self.color_el

            if fig_ok:
                self.fig_correcta = True

            if col_ok:
                self.col_correcta = True

            if fig_ok and col_ok:
                self.fyc_correcta = True

        if self.fyc_correcta or self.tiempo_restante() <= 0:
            self.fin()


    def tiempo_restante(self) -> float:
        return max(0.0, self.duracion - (time.monotonic() - self.tiempo_inicio))


    def fin(self) -> None:
        if not self.ronda_finalizada:
            self.ronda_finalizada = True
            self.tiempo_finalizado = time.monotonic()

    def resultado_ronda(self) -> Ronda:
        if self.tiempo_finalizado is None:
            self.fin()

        tiempo = self.tiempo_finalizado - self.tiempo_inicio

        return Ronda(
            forma_el=self.forma_el,
            color_el=self.color_el,
            f_check=self.fig_correcta,
            c_check=self.col_correcta,
            t_check=self.fyc_correcta,
            tiempo=tiempo
        )
=======
from detector_de_colores import Detectar

class Controlador:
    
    def __init__(self, figura_el: str, color_el: str, duracion: int = 20):
        self.figura_el = figura_el
        self.color_el = color_el
        self.duracion = duracion
        self.tiempo_inicio = time.monotonic()
        self.fig_correcta = False
        self.col_correcto = False
        self.fyc_correcto = False
        self.ronda_finalizada = False
        self.tiempo_finalizado: float | None = None

def actualizar(self, detecciones: list) -> None:
    if self.ronda_finalizada:
        return
    for det in detecciones:
        fig_corr = det.fig == self.figura_el
        col_corr = det.col == self.color_el
        if fig_corr:
            self.fig_correcta = True
        if col_corr:
            self.col_correcto = True
        if fig_corr and col_corr:
            self.fyc_correcto = True
    if self.fyc_correcto or self.tiempo_restante() <= 0:
        self.finalizar()

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
        forma_el=self.forma_el,
        color_el=self.color_el,
        fig_correcta=self.fig_correcta,
        col_correcto=self.col_correcto,
        fyc_correcto=self.fyc_correcto,
        duracion=duracion,
    )
>>>>>>> 647045613a862c0202162a568fb6276917cd2cb3
