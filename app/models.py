# tablas de SQLAlchemy

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timedelta

class Camion(Base):
    __tablename__ = "camiones"
    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(20), unique=True, index=True, nullable=False)
    dispositivo_id = Column(String, nullable=True)
    sesiones = relationship("Sesion", back_populates="camion")

class Sesion(Base):
    __tablename__ = "sesiones"
    id = Column(Integer, primary_key=True, index=True)
    camion_id = Column(Integer, ForeignKey("camiones.id"))
    inicio = Column(DateTime, default=datetime.utcnow)
    fin = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=12))
    camion = relationship("Camion", back_populates="sesiones")

class Escaneo(Base):
    __tablename__ = "escaneos"
    id = Column(Integer, primary_key=True, index=True)
    sesion_id = Column(Integer, ForeignKey("sesiones.id"))
    punto = Column(String)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    sesion = relationship("Sesion")

class Alerta(Base):
    __tablename__ = "alertas"
    id = Column(Integer, primary_key=True, index=True)
    sesion_id = Column(Integer, ForeignKey("sesiones.id"))
    punto_saltado = Column(String)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    correo_enviado = Column(Boolean, default=False)
    sesion = relationship("Sesion")