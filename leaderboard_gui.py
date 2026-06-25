import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
matplotlib.use("Agg")
from Bases import Record, orden_formas, orden_colores, LeaderboardVacio
import tkinter as tk
import traceback
import random

from PIL import Image, ImageTk

from Memoria import cargar_leaderboard


class LeaderboardGUI(tk.Frame):
    def __init__(self, principal, app):
        super().__init__(principal)
        self.app = app
        try:
            self.img = Image.open("final.png")
            self.img = self.img.resize((600,800))
            self.photo = ImageTk.PhotoImage(self.img)
            self.img_label = tk.Label(self, image=self.photo)
            self.img_label.image = self.photo
            self.img_label.place(x=0, y=0)
        except FileNotFoundError:
            self.config(bg="#2C3E50")

        tk.Label(
            self,
            text="🏆 LEADERBOARD",
            font=("Arial", 18, "bold"),
            bg="#f8f8f8",
            fg="#222222"
        ).place(x=180, y=20)

        tk.Button(
            self,
            text="Actualizar",
            bg="orange",
            fg="white",
            command=self.mostrar
        ).place(x=420, y=20)

        tk.Button(
            self,
            text="Volver",
            bg="#E74C3C",
            fg="white",
            command=self.volver
        ).place(x=510, y=20)

        self.left_panel = tk.Frame(
            self,
            bg="#95beec",
            highlightthickness=1,
            highlightbackground="#309bd9"
        )
        self.left_panel.place(x=50, y=80, width=500, height=280)

        self.grafico_panel = tk.Frame(
            self,
            bg="#2861d4",
            highlightthickness=1,
            highlightbackground="#08147a"
        )
        self.grafico_panel.place(x=50, y=380, width=500, height=380)

        self.grafico_frame = self.grafico_panel

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.mostrar()

    def mostrar(self):
        try:
            records = cargar_leaderboard()
        except LeaderboardVacio:
            self.mostrar_lista([])
            for w in self.grafico_frame.winfo_children():
                w.destroy()
            tk.Label(
                self.grafico_frame,
                text="No existen partidas registradas",
                font=("Arial", 12),
                bg="#2861d4",
                fg="white",
            ).pack(expand=True)
            return
        self.mostrar_lista(records[:10])
        self.mostrar_grafico(records[:5])
        

    def mostrar_lista(self, records):
        for widget in self.left_panel.winfo_children():
            widget.destroy()

        for i, r in enumerate(records, start=1):
            texto = f"{i}. {r.jugador} | {r.carrera} | {r.puntaje} pts"
            tk.Label(
                self.left_panel,
                text=texto,
                font=("Arial", 12),
                bg="#f5f5f5",
                fg="#111111",
                anchor="w"
            ).pack(fill="x", pady=4, padx=10)

    def mostrar_grafico(self, records):

        for w in self.grafico_frame.winfo_children():
            w.destroy()
        if not records:
            return

        nombres = [r.jugador for r in records]
        puntajes = [r.puntaje for r in records]
        colores = ["red", "blue", "green", "orange", "purple"]
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.bar(
            nombres,
            puntajes,
            color=[random.choice(colores) for _ in nombres]
        )
        ax.set_title("Top Puntajes", fontsize=14)
        ax.tick_params(axis='x', rotation=15)
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def volver(self):
        self.app.jugador_act = None
        self.app.mostrar_ventana("PantallaDeInicio")
