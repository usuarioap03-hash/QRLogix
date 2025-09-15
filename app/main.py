# punto de entrada de FastAPI
# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import scan

# Crear la app FastAPI
app = FastAPI()

# Archivos estáticos (logo, CSS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir las rutas de escaneo
app.include_router(scan.router)