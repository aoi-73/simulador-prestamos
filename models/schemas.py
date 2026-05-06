from pydantic import BaseModel, Field, validator
from uuid import UUID

class PrestamoSimularRequest(BaseModel):
    """Datos necesarios para simular un prestamo (sin guardar en BD)."""
    monto:       float = Field(gt=0, le=100000, description="Monto del prestamo en soles")
    plazo_meses: int   = Field(ge=6,  le=60,    description="Plazo en meses")
    tasa_anual:  float = Field(gt=0,  le=50,    description="Tasa de interes anual %")

class PrestamoSolicitudRequest(BaseModel):
    """Datos necesarios para solicitar un prestamo (se guarda en BD)."""
    user_id:            UUID
    monto:              float
    plazo_meses:        int
    tasa_anual:         float
    proposito:          str
    ingresos_mensuales: float

    @validator("proposito")
    def validar_proposito(cls, v):
        opciones = ["consumo", "educacion", "salud", "vivienda", "negocio"]
        if v not in opciones:
            raise ValueError(f"Proposito debe ser uno de: {opciones}")
        return v

class PrestamoSimularResponse(BaseModel):
    """Resultado de la simulacion que se envia al usuario."""
    monto:         float
    cuota_mensual: float
    total_pagar:   float
    total_interes: float
    plazo_meses:   int
    tasa_anual:    float
