from models.schemas import PrestamoSimularRequest, PrestamoSolicitudRequest
from services.prestamo_service import PrestamoService

service = PrestamoService()

class PrestamoController:
    async def simular(self, datos: PrestamoSimularRequest) -> dict:
        """Solo calcula la cuota, NO guarda en BD."""
        resultado = service.calcular_cuota(datos.monto, datos.plazo_meses, datos.tasa_anual)
        return {"success": True, "data": resultado}

    async def solicitar(self, datos: PrestamoSolicitudRequest) -> dict:
        """Calcula la cuota Y guarda la solicitud en Supabase."""
        calculo   = service.calcular_cuota(datos.monto, datos.plazo_meses, datos.tasa_anual)
        solicitud = await service.guardar_solicitud({**datos.dict(), **calculo})
        return {"success": True, "data": solicitud}

    async def listar_solicitudes(self, user_id: str) -> dict:
        """Devuelve todas las solicitudes de un usuario."""
        solicitudes = service.obtener_solicitudes(user_id)
        return {"success": True, "data": solicitudes}

    async def ver_solicitud(self, solicitud_id: str) -> dict:
        """Devuelve el detalle de una solicitud."""
        solicitud = service.obtener_solicitud(solicitud_id)
        if not solicitud:
            return {"success": False, "message": "Solicitud no encontrada"}
        return {"success": True, "data": solicitud}

    async def cancelar_solicitud(self, solicitud_id: str) -> dict:
        """Cancela una solicitud pendiente."""
        eliminado = service.eliminar_solicitud(solicitud_id)
        if not eliminado:
            return {"success": False, "message": "No se puede cancelar (no existe o ya fue procesada)"}
        return {"success": True, "message": "Solicitud cancelada correctamente"}
