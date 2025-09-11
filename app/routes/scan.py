# app/routes/scan.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app import crud, models
from fastapi import APIRouter, Request, Form, Depends, Response
import uuid

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# Lista dinámica de puntos
PUNTOS = ["punto1", "punto2", "punto3", "punto4", "punto5", "punto6"]
# Nombres más legibles para la UI
NOMBRES = {
    "punto1": "Patio",
    "punto2": "Punto de Carga",
    "punto3": "Punto 3",
    "punto4": "Punto 4",
    "punto5": "Punto 5",
    "punto6": "Punto 6",
}

@router.get("/scan/{punto}", response_class=HTMLResponse)
async def scan_qr(request: Request, punto: str, db: Session = Depends(get_db)):
    # Obtener o crear cookie
    device_id = request.cookies.get("device_id")
    if not device_id:
        device_id = str(uuid.uuid4())  # identificador único

    sesion = crud.get_sesion_activa_por_ip(db, device_id)

    if sesion:
        crud.create_escaneo(db, sesion.id, punto)
        response = RedirectResponse(
            url=f"/confirmacion?punto={punto}&placa={sesion.camion.placa}",
            status_code=303,
        )
        response.set_cookie(key="device_id", value=device_id, httponly=True)
        return response

    response = templates.TemplateResponse("index.html", {
        "request": request,
        "punto": punto,
        "submitted": False
    })
    response.set_cookie(key="device_id", value=device_id, httponly=True)
    return response


@router.post("/scan/{punto}", response_class=HTMLResponse)
async def scan_qr_post(request: Request, punto: str, plate: str = Form(...), db: Session = Depends(get_db)):
    # Obtener o crear cookie
    device_id = request.cookies.get("device_id")
    if not device_id:
        device_id = str(uuid.uuid4())

    camion = crud.get_camion_by_placa(db, plate)
    if not camion:
        camion = crud.create_camion(db, plate, dispositivo_id=device_id)

    sesion = crud.get_sesion_activa_por_ip(db, device_id)
    if not sesion:
        sesion = crud.create_sesion(db, camion.id)

    crud.create_escaneo(db, sesion.id, punto)

    response = RedirectResponse(
        url=f"/confirmacion?punto={punto}&placa={camion.placa}",
        status_code=303,
    )
    response.set_cookie(key="device_id", value=device_id, httponly=True)
    return response


@router.get("/confirmacion", response_class=HTMLResponse)
async def confirmacion(request: Request, punto: str, placa: str, db: Session = Depends(get_db)):
    # Buscar la sesión del camión
    camion = crud.get_camion_by_placa(db, placa)
    sesion = crud.get_sesion_activa_por_ip(db, request.client.host)

    # Escaneos de esa sesión
    escaneados = []
    if sesion:
        escaneados = [e.punto for e in db.query(models.Escaneo).filter(models.Escaneo.sesion_id == sesion.id).all()]

    estados = {}
    ultimo_idx = -1
    for idx, p in enumerate(PUNTOS):
        if p in escaneados:
            estados[p] = "completed"
            ultimo_idx = idx
        else:
            if idx < ultimo_idx:  # Saltado
                estados[p] = "skipped"
            elif idx == ultimo_idx + 1:  # El siguiente esperado
                estados[p] = "current"
            else:
                estados[p] = "pending"

    return templates.TemplateResponse("confirmacion.html", {
        "request": request,
        "punto": punto,
        "placa": placa,
        "hora": datetime.now().strftime("%H:%M:%S"),
        "estados": estados,
        "puntos": PUNTOS,
        "nombres": NOMBRES
    })
