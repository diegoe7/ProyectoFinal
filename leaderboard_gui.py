import tkinter as tk
import traceback
import random

from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Memoria import cargar_leaderboard


class LeaderboardGUI:
    def __init__(self, master=None):

        self.window = tk.Toplevel(master)
        self.window.title("Leaderboard")
        self.window.geometry("850x600")
        self.window.resizable(False, False)

        self.img = Image.open("final.png")
        self.img = self.img.resize((840, 600))
        self.photo = ImageTk.PhotoImage(self.img)

        self.img_label = tk.Label(self.window, image=self.photo)
        self.img_label.image = self.photo
        self.img_label.place(x=0, y=0)

        tk.Label(
            self.window,
            text="🏆 LEADERBOARD",
            font=("Arial", 18, "bold"),
            bg="#f8f8f8",
            fg="#222222"
        ).place(x=280, y=5)

        tk.Button(
            self.window,
            text="Actualizar",
            bg="orange",
            fg="white",
            command=self.mostrar
        ).place(x=700, y=10)

        self.left_panel = tk.Frame(
            self.window,
            bg="#95beec",
            highlightthickness=1,
            highlightbackground="#309bd9"
        )
        self.left_panel.place(x=90, y=100, width=270, height=400)

        self.grafico_panel = tk.Frame(
            self.window,
            bg="#2861d4",
            highlightthickness=1,
            highlightbackground="#08147a"
        )
        self.grafico_panel.place(x=380, y=100, width=400, height=400)

        self.grafico_frame = self.grafico_panel
        self.img_label.lower()
        self.left_panel.lift()
        self.grafico_panel.lift()

        self.mostrar()

    def mostrar(self):

        try:
            records = cargar_leaderboard()
            records.sort(key=lambda r: r.puntaje, reverse=True)

            self.mostrar_lista(records)
            self.mostrar_grafico(records)

        except Exception:
            print(traceback.format_exc())

    def mostrar_lista(self, records):

        for widget in self.left_panel.winfo_children():
            widget.destroy()

        for i, r in enumerate(records, start=1):

            texto = f"{i}. {r.jugador} | {r.carrera} | {r.puntaje} pts"

            tk.Label(
                self.left_panel,
                text=texto,
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#111111",
                anchor="w"
            ).pack(fill="x", pady=3, padx=8)

    def mostrar_grafico(self, records):

        for w in self.grafico_frame.winfo_children():
            w.destroy()

        if not records:
            return

        nombres = [r.jugador for r in records]
        puntajes = [r.puntaje for r in records]

        colores = ["red", "blue", "green", "orange", "purple"]

        fig, ax = plt.subplots(figsize=(3, 3))

        ax.bar(
            nombres,
            puntajes,
            color=[random.choice(colores) for _ in nombres]
        )

        ax.set_title("Puntajes")
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)