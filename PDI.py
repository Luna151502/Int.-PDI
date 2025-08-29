import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

# Tamaño ampliado para los paneles
ANCHO_PANEL = 400
ALTO_PANEL = 400

# ventana principal
ventana = tk.Tk()
ventana.title("PDI - Procesamiento Digital de Imágenes")
ventana.configure(bg="#d9b3ff")  #Color del fondo

# Variables globales
imagen_original = None
imagen_procesada = None

# Función para cargar imagen
def cargar_imagen():
    global imagen_original
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if ruta:
        imagen_original = Image.open(ruta)
        imagen_redimensionada = imagen_original.resize((ANCHO_PANEL, ALTO_PANEL))
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
        etiqueta_izquierda.config(image=imagen_tk)
        etiqueta_izquierda.image = imagen_tk

# Función para procesar imagen
def procesar_imagen():
    global imagen_procesada
    if imagen_original:
      #  imagen_procesada = imagen_original.convert("L")#la pasa a griz
        imagen_redimensionada = imagen_procesada.resize((ANCHO_PANEL, ALTO_PANEL))
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
        etiqueta_derecha.config(image=imagen_tk)
        etiqueta_derecha.image = imagen_tk

# Función para guardar imagen procesada
def guardar_imagen():
    global imagen_procesada
    if imagen_procesada:
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
                ("TIFF", "*.tiff")
            ],
            title="Guardar imagen procesada"
        )
        if ruta_guardado:
            try:
                imagen_procesada.save(ruta_guardado)
                print(f"Imagen guardada en: {ruta_guardado}")
            except Exception as e:
                print(f"Error al guardar la imagen: {e}")


# cuadro zquierdo (imagen original)
panel_izquierdo = tk.Frame(ventana, width=ANCHO_PANEL, height=ALTO_PANEL, bg="white")
panel_izquierdo.grid(row=0, column=0, padx=10, pady=10)
etiqueta_izquierda = tk.Label(panel_izquierdo, bg="white")
etiqueta_izquierda.pack(expand=True, fill="both")

# botones
panel_central = tk.Frame(ventana, bg="#d9b3ff")
panel_central.grid(row=0, column=1, padx=10, pady=10)

boton_cargar = tk.Button(panel_central, text="Cargar imagen", command=cargar_imagen)
boton_cargar.pack(pady=10)

boton_procesar = tk.Button(panel_central, text="Procesar imagen", command=procesar_imagen)
boton_procesar.pack(pady=10)

boton_guardar = tk.Button(panel_central, text="Guardar imagen", command=guardar_imagen)
boton_guardar.pack(pady=10)

#cuadro derecho (imagen procesada)
panel_derecho = tk.Frame(ventana, width=ANCHO_PANEL, height=ALTO_PANEL, bg="white")
panel_derecho.grid(row=0, column=2, padx=10, pady=10)
etiqueta_derecha = tk.Label(panel_derecho, bg="white")
etiqueta_derecha.pack(expand=True, fill="both")

# Ejecutar la aplicación
ventana.mainloop()
