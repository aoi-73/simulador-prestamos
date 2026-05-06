from repositories.prestamo_repository import PrestamoRepository

class PrestamoService:
    def __init__(self):
        self.repository = PrestamoRepository()

    def calcular_cuota(self, monto: float, plazo: int, tasa_anual: float) -> dict:
        """
        Formula de amortizacion francesa:
        C = P * [r(1+r)^n] / [(1+r)^n - 1]
        Donde: P = monto, r = tasa mensual decimal, n = plazo en meses
        """
        r      = (tasa_anual / 100) / 12
        factor = (1 + r) ** plazo
        cuota  = monto * (r * factor) / (factor - 1)
        total  = cuota * plazo
        return {
            "monto":         round(monto, 2),
            "cuota_mensual": round(cuota, 2),
            "total_pagar":   round(total, 2),
            "total_interes": round(total - monto, 2),
            "plazo_meses":   plazo,
            "tasa_anual":    tasa_anual
        }

    async def guardar_solicitud(self, datos: dict) -> dict:
        """Calcula la cuota y delega la persistencia al Repository."""
        return self.repository.insertar_solicitud(datos)

    def obtener_solicitudes(self, user_id: str) -> list:
        """Obtiene todas las solicitudes de un usuario."""
        return self.repository.obtener_solicitudes_por_usuario(user_id)

    def obtener_solicitud(self, solicitud_id: str) -> dict:
        """Obtiene una solicitud especifica."""
        return self.repository.obtener_solicitud_por_id(solicitud_id)

    def eliminar_solicitud(self, solicitud_id: str) -> bool:
        """Elimina una solicitud pendiente."""
        return self.repository.eliminar_solicitud(solicitud_id)
