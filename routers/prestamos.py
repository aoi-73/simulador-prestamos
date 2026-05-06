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
