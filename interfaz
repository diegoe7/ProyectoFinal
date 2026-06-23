from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.title("ENTRADA PRINCIPAL")
root.geometry("600x800")
# ===== GIF ANIMADO =====
gif = Image.open("portada1_mov.gif")
frames = []

try:
    while True:
        frame = gif.copy()
        frame = frame.resize((600, 800))
        frames.append(ImageTk.PhotoImage(frame))
        gif.seek(len(frames))
except:
    pass

frame_index = 0

fondo = tk.Label(root)
fondo.place(x=0, y=0, relwidth=1, relheight=1)

def animar():
    global frame_index
    fondo.config(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    root.after(100, animar)  # velocidad

animar()

# ===== CAMPOS DE REGISTRO =====

tk.Label(
    root,
    text="Nombre:",
    bg="#F14559",
    fg="white",
    font=("Arial", 14, "bold")
).place(x=140, y=500)

frame_nombre = tk.Frame(root, bg="#1E90FF", padx=2, pady=2)
frame_nombre.place(x=230, y=500)

entrada_nombre = tk.Entry(frame_nombre, width=23, bd=0)
entrada_nombre.pack()

tk.Label(
    root,
    text="Carrera:",
    bg="#F14559",
    fg="white",
    font=("Arial", 14, "bold")
).place(x=140, y=540)

frame_carrera = tk.Frame(root, bg="#1E90FF", padx=2, pady=2)
frame_carrera.place(x=230, y=540)

entrada_carrera = tk.Entry(frame_carrera, width=23, bd=0)
entrada_carrera.pack()

# ===== RESULTADOS =====

resultado = tk.Label(
    root,
    text="",
    bg="#000000",
    fg="white",
    font=("Arial", 10, "bold")
)
resultado.place(x=200, y=650)

def iniciar_juego():
    nombre = entrada_nombre.get()
    carrera = entrada_carrera.get()

    resultado.config(
        text=f"Jugador: {nombre}\nCarrera: {carrera}"
    )

# ===== BOTONES =====

btn_inicio = tk.Button(
    root,
    text="Iniciar Juego",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    command=iniciar_juego
)
btn_inicio.place(x=130, y=600)

btn_resultados = tk.Button(
    root,
    text="Ver Resultados",
    bg="#E025D7",
    fg="white",
    font=("Arial", 12, "bold")
)
btn_resultados.place(x=290, y=600)

root.mainloop()
