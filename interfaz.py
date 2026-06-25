import tkinter as tk
from tkinter import messagebox
from Bases import Jugador, DatosInvalidos, Record, CamaraNoEncontrada, Partida
from logs import get_logger
from PIL import Image, ImageTk
import cv2
from detector_de_colores import detectar_figuras
from Controlador import Controlador
from Memoria import guardar_partida
from leaderboard_gui import LeaderboardGUI


logger = get_logger(__name__)

class FormCol(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formas y Colores")
        self.geometry("600x800")
        self.resizable(False, False)
        self.jugador_act: Jugador | None = None
        self.espacio = tk.Frame(self)
        self.espacio.pack(fill="both", expand=True)
        self.frames: dict[str, tk.Frame] = {}
        self.pantalla_inicial(PantallaDeInicio)
        self.pantalla_inicial(Jugar)
        self.pantalla_inicial(LeaderboardGUI)
        self.mostrar_ventana("PantallaDeInicio")

    def pantalla_inicial(self, tipo):
        frame = tipo(principal=self.espacio, app=self)
        self.frames[tipo.__name__] = frame
        frame.place(x=0, y=0, relwidth=1, relheight=1)

    def mostrar_ventana(self, nombre: str):
        frame = self.frames[nombre]
        if hasattr(frame, "mostrar"):
            frame.mostrar()
        frame.tkraise()


class PantallaDeInicio(tk.Frame):
    def __init__(self, principal, app: "FormCol"):
        super().__init__(principal)
        self.app = app
        self.background()
        self.registros()
        self.botones()

    def background(self):
        self.etiqueta = tk.Label(self)
        self.etiqueta.place(x=0, y=0, relwidth=1, relheight=1)
        gif = Image.open("portada1_mov.gif")
        self.gif_frames = []
        try:
            while True:
                frame = gif.copy().resize((600, 800))
                self.gif_frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(self.gif_frames))
        except (EOFError, FileNotFoundError):
            pass
        self.indice = 0
        self.fondo()

    def fondo(self):
        if not self.gif_frames:
            return
        self.etiqueta.config(image=self.gif_frames[self.indice])
        self.indice = (self.indice + 1) % len(self.gif_frames)
        self.after(100, self.fondo)

    def registros(self):
        tk.Label(self, text="Nombre:", bg="#F14559", fg="white",
                 font=("Arial", 14, "bold")).place(x=140, y=500)
        self.nombre = tk.Entry(self, width=23, bd=0)
        self.nombre.place(x=230, y=500)

        tk.Label(self, text="Carrera:", bg="#F14559", fg="white",
                 font=("Arial", 14, "bold")).place(x=140, y=540)
        self.carrera = tk.Entry(self, width=23, bd=0)
        self.carrera.place(x=230, y=540)

    def botones(self):
        tk.Button(self, text="Iniciar Partida", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                   command=self.iniciar_partida).place(x=130, y=600)
        tk.Button(self, text="Leaderboard", bg="#E025D7", fg="white", font=("Arial", 12, "bold"),
                   command=self.mostrar_leaderboard).place(x=290, y=600)

    def iniciar_partida(self):
        nombre = self.nombre.get()
        carrera = self.carrera.get()
        try:
            jugador = Jugador(nombre=nombre, carrera=carrera)
        except DatosInvalidos as exc:
            messagebox.showerror("Datos de Jugador Invalidos", str(exc))
            return
        self.app.jugador_act = jugador
        self.app.mostrar_ventana("Jugar")

    def mostrar_leaderboard(self):
        self.app.mostrar_ventana("LeaderboardGUI")


class Jugar(tk.Frame):
    def __init__(self, principal, app: "FormCol"):
        super().__init__(principal, bg="#1a1a1a")
        self.app = app
        self.partida: Partida | None = None
        self.controlador: Controlador | None = None
        self.capturas: cv2.VideoCapture | None = None
        self.widgets()

    def widgets(self):
        self.etiq_vid = tk.Label(self, bg="Black")
        self.etiq_vid.place(x=20, y=20, width=560, height=420)

        self.etiq_bus = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#1a1a1a", fg="white")
        self.etiq_bus.place(x=20, y=460)

        self.etiq_temp = tk.Label(self, text="", font=("Arial", 36, "bold"), bg="#1a1a1a", fg="white")
        self.etiq_temp.place(x=20, y=510)

        self.etiq_pun = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#1a1a1a", fg="white")
        self.etiq_pun.place(x=20, y=580)

    def mostrar(self):
        self.partida = Partida(self.app.jugador_act)
        try:
            self.capturas = cv2.VideoCapture(0)
            if not self.capturas.isOpened():
                raise CamaraNoEncontrada("Cámara no encontrada")
        except CamaraNoEncontrada as exc:
            messagebox.showerror("Error de cámara", str(exc))
            self.app.mostrar_ventana("PantallaDeInicio")
            return

        self.siguiente_ronda()

    def siguiente_ronda(self):
        fig_el, col_el = self.partida.siguiente_el()
        self.controlador = Controlador(fig_el, col_el, duracion=20)
        self.etiq_bus.config(text=f"Muestra un: {fig_el.upper()} {col_el.upper()}")
        self.actualizar_punt()
        self.actualizar()

    def actualizar(self):
        ret, frame = self.capturas.read()
        if not ret:
            self.after(30, self.actualizar)
            return
        frame = cv2.flip(frame, 1)
        items = detectar_figuras(frame)
        self.controlador.actualizar(items)
        self.render(frame, items)
        self.actualizar_timer()

        if self.controlador.finalizar():
            self.finalizar_ronda()
            return
        self.after(30, self.actualizar)

    def render(self, frame, items):
        disp = frame.copy()

        for i in items:
            x, y, w, h = i.box
            cv2.rectangle(disp, (x, y), (x + w, y + h), (0, 250, 0), 2)
            etiq = f"{i.color} {i.forma}"
            cv2.putText(disp, etiq, (x, max(0, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        rgb = cv2.cvtColor(disp, cv2.COLOR_BGR2RGB)
        imagen = Image.fromarray(rgb)
        imagen = imagen.resize((560, 420))
        foto = ImageTk.PhotoImage(imagen)
        self.etiq_vid.config(image=foto)
        self.etiq_vid.image = foto

    def actualizar_timer(self):
        restante = self.controlador.tiempo_restante()
        self.etiq_temp.config(text=f"{restante:.1f}s")

    def actualizar_punt(self):
        num_rond = len(self.partida.rondas_jugadas) + 1
        self.etiq_pun.config(text=f"Ronda {num_rond}/{3}  |  "
                              f"Puntaje: {self.partida.puntaje_total}pts")

    def finalizar_ronda(self):
        resultado = self.controlador.resultado_ronda()
        self.partida.res_ronda(resultado)
        if self.partida.terminado():
            self.finalizar_partida()
        else:
            self.siguiente_ronda()

    def finalizar_partida(self):
        self.liberar_camara()
        record = self.partida.resultado()
        por_color = sum(record.puntaje_c.values())
        por_forma = sum(record.puntaje_f.values())

        try:
            guardar_partida(record)
        except OSError as exc:
            logger.error(f"Error al guardar la partida: {exc}")
            messagebox.showwarning("Advertencia de guardado", "Tu puntaje no se guardo correctamente")

        messagebox.showinfo(
            "Resultados",
            f"Jugador: {record.jugador}\n"
            f"Puntaje final: {record.puntaje}\n"
            f"Por forma: {por_color}\n"
            f"Por color: {por_forma}"
        )
        self.app.mostrar_ventana("PantallaDeInicio")

    def liberar_camara(self):
        if self.capturas is not None and self.capturas.isOpened():
            self.capturas.release()
        self.capturas = None


if __name__ == "__main__":
    app = FormCol()
    app.mainloop()
