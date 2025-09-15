# app/utils/qr_generador_registro.py
import os
import qrcode

# URL fija de GitHub Pages (no cambia), solo cambias "path" desde el QR
GHPAGES_BASE = "https://usuarioap03-hash.github.io/hosting"  # <-- Ajusta tu user/repo
URL_REGISTRO = f"{GHPAGES_BASE}/?path=registro_dispositivo"

OUT_DIR = "/Users/cesardaniel/Desktop/GRAY_PROJECT/QR_generade"  # <-- Ajusta a tu ruta

os.makedirs(OUT_DIR, exist_ok=True)

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(URL_REGISTRO)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save(os.path.join(OUT_DIR, "qr_registro_dispositivo.png"))

print(f"✅ QR generado: {os.path.join(OUT_DIR, 'qr_registro_dispositivo.png')}")
print(f"   → {URL_REGISTRO}")