import numpy as np
import sounddevice as sd
import tkinter as tk

# Frecuencias de las notas (en Hz)
LA = 440.0          # La
DO = 261.63         # Do
MI = 329.63         # Mi

# Duración de cada pulso en segundos
DURACION = 0.5

MUESTREO = 44100

def tono(frecuencia, duracion):
    t = np.linspace(0, duracion, int(MUESTREO * duracion), False)
    return np.sin(2 * np.pi * frecuencia * t)

def acorde(frecuencias, duracion):
    t = np.linspace(0, duracion, int(MUESTREO * duracion), False)
    senales = [np.sin(2 * np.pi * f * t) for f in frecuencias]
    # Promediamos para evitar clipping
    return sum(senales) / len(senales)

pulso_la = tono(LA, DURACION)
pulso_do_mi = acorde([DO, MI], DURACION)

pulsos = [pulso_la, pulso_do_mi, pulso_do_mi]


root = tk.Tk()
root.title("Pulsos")

canvas = tk.Canvas(root, width=300, height=100)
canvas.pack()

rects = []
for i in range(3):
    rect = canvas.create_rectangle(10 + i * 100, 10, 90 + i * 100, 90,
                                   fill="gray")
    rects.append(rect)

indice = 0

def desactivar(idx):
    canvas.itemconfig(rects[idx], fill="gray")

def reproducir():
    global indice
    actual = indice % 3
    canvas.itemconfig(rects[actual], fill="yellow")
    sd.play(pulsos[actual], MUESTREO, blocking=False)
    root.after(int(DURACION * 1000), lambda idx=actual: desactivar(idx))
    indice += 1
    root.after(int(DURACION * 1000), reproducir)

print("Reproduciendo pulsos visuales y de sonido... (cerrar ventana para salir)")
reproducir()
root.mainloop()
