# app/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# --- Cargar .env ---
# Primero intenta data.env (como lo usas) y si no existe cae a .env
ENV_CANDIDATES = [Path("data.env"), Path(".env")]
for cand in ENV_CANDIDATES:
    if cand.exists():
        load_dotenv(dotenv_path=cand)
        break
else:
    # Si no hay archivo, intenta cargar variables del entorno del sistema
    load_dotenv()

# --- DB ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "QRLogix")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --- Zona horaria para mostrar horas en pantalla ---
TIMEZONE = os.getenv("TIMEZONE", "America/Panama")

# --- Duración de sesión ---
# Puedes definir en data.env:
#   SESSION_DURATION_MINUTES=60
#   o bien
#   SESSION_DURATION_HOURS=1.5
def _session_minutes_from_env() -> int:
    m = os.getenv("SESSION_DURATION_MINUTES")
    h = os.getenv("SESSION_DURATION_HOURS")
    if m is not None and m.strip() != "":
        # permite decimales (ej. 0.5 minutos)
        return max(1, int(round(float(m))))
    if h is not None and h.strip() != "":
        return max(1, int(round(float(h) * 60.0)))
    # por defecto 12 horas
    return 12 * 60

SESSION_DURATION_MINUTES = _session_minutes_from_env()

# --- Puntos QR (orden) ---
# Si algún día quieres 6 u 8 puntos, solo cambia esta lista
POINTS_ORDER = os.getenv("POINTS_ORDER", "punto1,punto2,punto3,punto4").split(",")
POINTS_ORDER = [p.strip() for p in POINTS_ORDER if p.strip()]