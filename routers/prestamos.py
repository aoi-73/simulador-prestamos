from fastapi import APIRouter
from models.schemas import PrestamoSimularRequest, PrestamoSolicitudRequest
from controllers.prestamo_controller import PrestamoController

router     = APIRouter()
controller = PrestamoController()

@router.post("/simular", summary="Simular cuota de prestamo")
async def simular_prestamo(datos: PrestamoSimularRequest):
    return await controller.simular(datos)

@router.post("/solicitar", summary="Enviar solicitud de prestamo")
async def solicitar_prestamo(datos: PrestamoSolicitudRequest):
    return await controller.solicitar(datos)

@router.get("/solicitudes/{user_id}", summary="Listar solicitudes por usuario")
async def listar_solicitudes(user_id: str):
    return await controller.listar_solicitudes(user_id)

@router.get("/solicitudes/{user_id}/{solicitud_id}", summary="Ver detalle de solicitud")
async def ver_solicitud(user_id: str, solicitud_id: str):
    return await controller.ver_solicitud(solicitud_id)

@router.delete("/solicitudes/{solicitud_id}", summary="Cancelar solicitud pendiente")
async def cancelar_solicitud(solicitud_id: str):
    return await controller.cancelar_solicitud(solicitud_id)

@router.get(
    "/promedio-cuota/{user_id}",
    summary="Cuota promedio recalculada con TEM correcta",
    description="""
    Retorna el promedio de cuota mensual recalculado con TEM (Tasa Efectiva Mensual).
    IMPORTANTE: El campo cuota_registrada refleja el valor almacenado históricamente 
    con la fórmula TEA/12 (incorrecta). El campo cuota_correcta es el valor real 
    calculado con TEM según normativa SBS.
    El área de Riesgos debe usar cuota_correcta para reportes ejecutivos.
    """
)
async def promedio_cuota(user_id: str):
    return await controller.promedio_cuota(user_id)

@router.get(
    "/cuota-mas-alta/{user_id}",
    summary="Cuota más alta recalculada con TEM correcta"
)
async def cuota_mas_alta(user_id: str):
    return await controller.cuota_mas_alta(user_id)
