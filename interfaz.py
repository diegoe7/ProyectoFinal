from PIL import Image, ImageTk
import tkinter as tk
import threading
import cv2
import time
from Bases import Jugador, Partida
from Controlador import Controlador
from detector_de_colores import detectar_figuras
from Memoria import guardar_partida
from logs import get_logger

logger = get_logger(__name__)


class JuegoGUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("JUEGO DE FIGURAS")
        self.root.geometry("600x800")

        self.ultimo_texto = ""
        self.controlador = None
        self.partida = None

        self.frames = []
        self.frame_index = 0

        self.ejecutando = True

        self.crear_fondo()
        self.crear_widgets()
        self.actualizar_ui()

    def crear_fondo(self):

        try:
            gif = Image.open("portada1_mov.gif")

            while True:
                frame = gif.copy().resize((600, 800))
                self.frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(self.frames))

        except EOFError:
            pass

        except Exception as e:
            logger.error(f"Error cargando gif: {e}")

        self.fondo = tk.Label(self.root)
        self.fondo.place(x=0, y=0, relwidth=1, relheight=1)

        self.animar()

    def animar(self):
        if self.frames:
            self.fondo.config(image=self.frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        self.root.after(100, self.animar)

    def crear_widgets(self):

        tk.Label(self.root, text="Nombre:", bg="#F14559", fg="white").place(x=140, y=500)
        self.entrada_nombre = tk.Entry(self.root)
        self.entrada_nombre.place(x=230, y=500)

        tk.Label(self.root, text="Carrera:", bg="#F14559", fg="white").place(x=140, y=540)
        self.entrada_carrera = tk.Entry(self.root)
        self.entrada_carrera.place(x=230, y=540)

        self.resultado = tk.Label(self.root, text="", bg="black", fg="white")
        self.resultado.place(x=180, y=700)

        tk.Button(self.root, text="Iniciar", bg="green", fg="white",
                  command=self.iniciar).place(x=220, y=600)

        tk.Button(self.root, text="Ver Resultados", bg="#3A86FF", fg="white",
                  command=self.abrir_leaderboard).place(x=310, y=600)

        tk.Button(self.root, text="Salir", bg="red", fg="white",
                  command=self.salir_app).place(x=10, y=10)

    def salir_app(self):
        self.ejecutando = False
        cv2.destroyAllWindows()
        self.root.destroy()

    def actualizar_ui(self):
        if not self.ejecutando:
            return
        self.resultado.config(text=self.ultimo_texto)
        self.root.after(300, self.actualizar_ui)

    def abrir_leaderboard(self):
        try:
            from leaderboard_gui import LeaderboardGUI
            LeaderboardGUI(master=self.root)
        except Exception as e:
            logger.error(f"Error abriendo leaderboard: {e}")
            self.ultimo_texto = "Error al abrir leaderboard"

    def iniciar(self):

        nombre = self.entrada_nombre.get()
        carrera = self.entrada_carrera.get()

        if not nombre or not carrera:
            self.ultimo_texto = "Completa los datos"
            return

        jugador = Jugador(nombre, carrera)
        self.partida = Partida(jugador)

        threading.Thread(
            target=self.juego,
            args=(self.partida,),
            daemon=True
        ).start()

    def juego(self, partida):

        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            self.ultimo_texto = "ERROR CAMARA"
            return

        forma, color = partida.siguiente_fig()
        self.controlador = Controlador(forma, color, 20)

        ronda = 1

        while ronda <= 3 and self.ejecutando:

            ret, frame = cam.read()
            if not ret:
                break

            detecciones = detectar_figuras(frame)
            self.controlador.actualizar(detecciones)

            tiempo = int(self.controlador.tiempo_restante())

            self.ultimo_texto = f"{forma} {color} | {tiempo}s"

            alto, ancho, _ = frame.shape
            cx = ancho // 2
            cy = alto // 2

            cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
            cv2.rectangle(frame, (cx-40, cy-40), (cx+40, cy+40), (0, 255, 255), 2)

            for det in detecciones:

                x, y, w, h = det.box

                obj_cx = x + w // 2
                obj_cy = y + h // 2

                if (cx-40 < obj_cx < cx+40) and (cy-40 < obj_cy < cy+40):

                    es_objetivo = (det.forma == forma and det.color == color)

                    if es_objetivo:
                        cv2.putText(frame, "ACIERTO", (x, y-20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                    (0, 255, 0), 2)


            cv2.putText(frame, f"Busca: {forma} {color}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.putText(frame, f"Tiempo: {tiempo}s", (20, 85),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.putText(frame, f"Ronda: {ronda}/3", (20, 118),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("JUEGO", frame)

            if self.controlador.ronda_finalizada:
                resultado = self.controlador.resultado_ronda()
                partida.res_ronda(resultado)

                ronda += 1

                if ronda <= 3:
                    forma, color = partida.siguiente_fig()
                    self.controlador = Controlador(forma, color, 20)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cam.release()
        cv2.destroyAllWindows()

        record = partida.resultado()
        guardar_partida(record)

        self.ultimo_texto = f"FIN | Puntaje: {record.puntaje}"

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = JuegoGUI()
    app.ejecutar()
