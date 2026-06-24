import time
from Bases import Ronda


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
