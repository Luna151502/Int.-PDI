import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

ANCHO, ALTO = 400, 400
imagen_original = None
imagen_yiq = None
imagen_mostrada = None

app = tk.Tk()
app.title("PDI")
app.configure(bg='beige')
app.geometry(f"+{200}+{30}")
app.geometry("1100x450")

#---------------------------------- Conversiones ----------------------------------#
def rgb_a_yiq(rgb):
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    I = 0.596 * R - 0.274 * G - 0.322 * B
    Q = 0.211 * R - 0.523 * G + 0.312 * B
    return np.stack((Y, I, Q), axis=-1)

def yiq_a_rgb(yiq):
    matriz = np.array([
        [1.0,  0.956,  0.621],
        [1.0, -0.272, -0.647],
        [1.0, -1.106,  1.703]
    ])
    return np.clip(np.tensordot(yiq, matriz.T, axes=([2], [0])), 0, 1)

#------------------------------- Funciones principales -----------------------------#
def cargar():
    global imagen_original
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")])
    if ruta:
        imagen_original = Image.open(ruta)
        img_redim = imagen_original.resize((ANCHO, ALTO))
        img_tk = ImageTk.PhotoImage(img_redim)
        label_img.config(image=img_tk)
        label_img.image = img_tk
        label_info.config(text="Imagen seleccionada", fg="green")
        label_info.after(1000, lambda: label_info.config(text=""))

def pasar_a_yiq():
    global imagen_yiq
    if not imagen_original:
        label_info.config(text="⚠️ Primero seleccione una imagen", fg="red")
        return

    rgb = np.array(imagen_original.resize((ANCHO, ALTO)), dtype=np.float32) / 255.0
    imagen_yiq = rgb_a_yiq(rgb)
    mostrar_imagen(yiq_a_rgb(imagen_yiq))
    boton_canales.config(state="normal")
    boton_modificar.config(state="normal")

def mostrar_imagen(rgb):
    global imagen_mostrada
    imagen_mostrada = Image.fromarray((rgb * 255).astype(np.uint8))
    img_tk = ImageTk.PhotoImage(imagen_mostrada)
    label_img2.config(image=img_tk)
    label_img2.image = img_tk

def mostrar_canales():
    if imagen_yiq is None: return
    if imagen_yiq is None:
        label_info.config(text="⚠️ Primero convierta la imagen a YIQ", fg="red")
        return

    x_base = app.winfo_rootx()
    y_base = app.winfo_rooty() + app.winfo_height() + 10

    for i, nombre in enumerate("YIQ"):
        canal = np.clip(imagen_yiq[..., i] * 255, 0, 255).astype(np.uint8)
        img = Image.fromarray(canal)
        img.thumbnail((250, 250))
        img_tk = ImageTk.PhotoImage(img)

        ventana = tk.Toplevel(app)
        ventana.title(f"Canal {nombre}")
        ventana.geometry(f"+{x_base + i * 260}+{y_base}")
        tk.Label(ventana, image=img_tk).pack()
        ventana.image = img_tk

def modificar_y_i():
    if imagen_yiq is None:
        label_info.config(text="⚠️ Primero convierta la imagen a YIQ", fg="red")
        return

    def aplicar():
        α = slider_alpha.get() / 100.0
        β = slider_beta.get() / 100.0
        yiq_mod = imagen_yiq.copy()
        yiq_mod[..., 0] = np.clip(α * yiq_mod[..., 0], 0, 1)
        yiq_mod[..., 2] *= β
        mostrar_imagen(yiq_a_rgb(yiq_mod))

    ventana = tk.Toplevel(app)
    ventana.title("Modificar Y e I")
    ventana.geometry(f"+{app.winfo_rootx() + 1100}+30")

    for texto, slider in [("Luminancia (α)", 100), ("Saturación (β)", 100)]:
        tk.Label(ventana, text=texto).pack()
        s = tk.Scale(ventana, from_=0, to=200, orient="horizontal")
        s.set(slider)
        s.pack()
        if texto.startswith("Luminancia"): slider_alpha = s
        else: slider_beta = s

    tk.Button(ventana, text="Aplicar", command=aplicar).pack(pady=10)

def guardar():
    if imagen_mostrada is None:
        label_info.config(text="⚠️ No hay imagen procesada para guardar", fg="red")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("BMP", "*.bmp"), ("TIFF", "*.tiff")],
        title="Guardar imagen procesada"
    )
    if ruta:
        try:
            imagen_mostrada.save(ruta)
            label_info.config(text="✅ Imagen guardada", fg="green")
        except Exception as e:
            label_info.config(text=f"Error al guardar: {e}", fg="red")

def salir():
    app.destroy()

#------------------------------- Interfaz gráfica ----------------------------------#
def crear_panel_imagen(padre):
    panel = tk.Frame(padre, width=ANCHO, height=ALTO, bg='white')
    panel.grid_propagate(False)
    label = tk.Label(panel, bg='white')
    label.pack(expand=True, fill='both')
    return panel, label

def crear_botones(padre):
    botones = [
        ("Cargar imagen", cargar),
        ("Pasar de RGB a YIQ", pasar_a_yiq),
        ("Mostrar canales", mostrar_canales),
        ("Modificar Y, I", modificar_y_i),
        ("Guardar img.",guardar),
        ("Salir", salir)
    ]
    for texto, comando in botones:
        estado = "normal" if texto in ["Cargar imagen", "Pasar de RGB a YIQ","Guardar img.", "Salir"] else "disabled"
        btn = tk.Button(padre, text=texto, command=comando, width=20)
        btn.pack(pady=10)
        if texto == "Mostrar canales": global boton_canales; boton_canales = btn
        if texto == "Modificar Y, I": global boton_modificar; boton_modificar = btn

label_info = tk.Label(app, text="Seleccione una imagen para empezar", bg='beige', font=('Verdana', 9, 'underline'))
label_info.grid(row=0, column=0, columnspan=3, pady=5)

panel_izq, label_img = crear_panel_imagen(app)
panel_izq.grid(row=1, column=0, padx=10, pady=10)

panel_central = tk.Frame(app, width=200, height=ALTO, bg='beige')
panel_central.grid(row=1, column=1, padx=10, pady=10)
panel_central.grid_propagate(False)
contenedor = tk.Frame(panel_central, bg='beige')
contenedor.place(relx=0.5, rely=0.5, anchor='center')
crear_botones(contenedor)

panel_der, label_img2 = crear_panel_imagen(app)
panel_der.grid(row=1, column=2, padx=10, pady=10)

app.mainloop()

