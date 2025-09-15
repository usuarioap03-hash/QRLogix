import os
import tkinter as tk
from tkinter import messagebox
import qrcode
from datetime import datetime
from pathlib import Path
import requests
from PIL import Image

desktop = Path.home() / "Desktop"

# Consultar al backend
def obtener_info():
    try:
        resp = requests.get("http://localhost:8000/api/info")
        if resp.status_code == 200:
            return resp.json()
        else:
            return {
                "base_url": "http://localhost:8000",
                "github_redirect": "https://usuarioap03-hash.github.io/hosting/"
            }
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la info del backend:\n{e}")
        return {
            "base_url": "http://localhost:8000",
            "github_redirect": "https://usuarioap03-hash.github.io/hosting/"
        }

def generar_qr(texto, carpeta, nombre_base):
    carpeta_destino = desktop / carpeta
    carpeta_destino.mkdir(parents=True, exist_ok=True)
    nombre_archivo = f"{nombre_base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    ruta_archivo = carpeta_destino / nombre_archivo

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(ruta_archivo)
    return ruta_archivo

def qr_registro():
    info = obtener_info()
    base_url = info["base_url"]
    ruta = generar_qr(f"{base_url}/scan/registro", "QR_Registros", "registro")
    messagebox.showinfo("QR Generado", f"✅ QR de registro guardado en:\n{ruta}")

def qr_prueba():
    info = obtener_info()
    base_url = info["base_url"]
    ruta = generar_qr(f"{base_url}/scan/prueba", "QR_Pruebas", "prueba")
    messagebox.showinfo("QR Generado", f"✅ QR de prueba guardado en:\n{ruta}")

def borrar_registros():
    carpeta = desktop / "QR_Pruebas"
    if carpeta.exists():
        for f in carpeta.glob("*.png"):
            f.unlink()
        messagebox.showinfo("Limpieza", "🧹 Registros de pruebas borrados.")
    else:
        messagebox.showwarning("Aviso", "No se encontró la carpeta de pruebas.")

# Crear ventana principal
root = tk.Tk()
root.title("Capacitación QRLogix")
root.geometry("450x380")

tk.Label(root, text="Panel de Capacitación QRLogix", font=("Arial", 14, "bold")).pack(pady=20)

btn1 = tk.Button(root, text="Generar QR de Registros", font=("Arial", 12), width=30, command=qr_registro)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Generar QR de Pruebas", font=("Arial", 12), width=30, command=qr_prueba)
btn2.pack(pady=10)

btn3 = tk.Button(root, text="Borrar QR de Pruebas", font=("Arial", 12), width=30, command=borrar_registros)
btn3.pack(pady=10)

# Pie de página con info dinámica
info = obtener_info()
footer = tk.Frame(root)
footer.pack(side="bottom", pady=20)

tk.Label(footer, text=f"Enlace del túnel vigente:\n{info['base_url']}", font=("Arial", 9), fg="blue").pack()
tk.Label(footer, text=f"Página de redirección:\n{info['github_redirect']}", font=("Arial", 9), fg="green").pack()

root.mainloop()