# app/routes/scan.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from datetime import datetime

router = APIRouter()

# Templates: carpeta donde están los HTML
templates = Jinja2Templates(directory="app/templates")

@router.get("/scan/{punto}", response_class=HTMLResponse)
async def scan_qr(request: Request, punto: str, db: Session = Depends(get_db)):
    client_ip = request.client.host
    sesion = crud.get_sesion_activa_por_ip(db, client_ip)

    if sesion:
        # ✅ Guardar el escaneo automáticamente cuando hay sesión activa
        crud.create_escaneo(db, sesion.id, punto)

        return RedirectResponse(
            url=f"/confirmacion?punto={punto}&placa={sesion.camion.placa}",
            status_code=303
        )

    # Si no hay sesión, mostrar formulario
    return templates.TemplateResponse("index.html", {
        "request": request,
        "punto": punto,
        "submitted": False
    })

@router.post("/scan/{punto}", response_class=HTMLResponse)
async def scan_qr_post(request: Request, punto: str, plate: str = Form(...), db: Session = Depends(get_db)):
    client_ip = request.client.host
    camion = crud.get_camion_by_placa(db, plate)

    if not camion:
        camion = crud.create_camion(db, plate, dispositivo_id=client_ip)

    sesion = crud.get_sesion_activa_por_ip(db, client_ip)
    if not sesion:
        sesion = crud.create_sesion(db, camion.id)

    # ✅ Siempre guardar el escaneo al registrar placa
    crud.create_escaneo(db, sesion.id, punto)

    return RedirectResponse(
        url=f"/confirmacion?punto={punto}&placa={camion.placa}",
        status_code=303
    )

@router.get("/confirmacion", response_class=HTMLResponse)
async def confirmacion(request: Request, punto: str, placa: str):
    # Lista ordenada de los puntos
    orden = ["punto1", "punto2", "punto3", "punto4"]

    # Calcular hora actual
    hora = datetime.now().strftime("%I:%M:%S %p")

    # Estados dinámicos de los puntos
    estados = {}
    encontrado = False
    for p in orden:
        if not encontrado:
            estados[p] = "completed"
        if p == punto:
            estados[p] = "completed"
            encontrado = True
        elif encontrado:
            estados[p] = "pending"

    return templates.TemplateResponse("confirmacion.html", {
        "request": request,
        "punto": punto,
        "placa": placa,
        "hora": hora,
        "estados": estados
    })