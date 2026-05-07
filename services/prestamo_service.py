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
        r      = (1 + (tasa_anual / 100)) ** (1 / 12) - 1
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

    def calcular_promedio_cuota(self, user_id: str) -> dict:
        solicitudes = self.repository.obtener_datos_para_recalculo(user_id)
        if not solicitudes:
            return {"promedio_cuota_correcto": 0, "cantidad": 0}

        cuotas_registradas = []
        cuotas_correctas = []

        for s in solicitudes:
            cuotas_registradas.append(s["cuota_mensual"])
            tem = (1 + s["tasa_anual"] / 100) ** (1 / 12) - 1
            cuota = s["monto"] * tem / (1 - (1 + tem) ** -s["plazo_meses"])
            cuotas_correctas.append(round(cuota, 2))

        prom_registrado = sum(cuotas_registradas) / len(cuotas_registradas)
        prom_correcto = sum(cuotas_correctas) / len(cuotas_correctas)

        return {
            "promedio_cuota_registrado": round(prom_registrado, 2),
            "promedio_cuota_correcto": round(prom_correcto, 2),
            "diferencia": round(prom_registrado - prom_correcto, 2),
            "pct_sobreestimacion": round((prom_registrado / prom_correcto - 1) * 100, 2) if prom_correcto > 0 else 0,
            "cantidad_solicitudes": len(solicitudes),
            "advertencia": "cuota_registrada calculada con fórmula TEA/12 incorrecta"
        }

    def obtener_cuota_mas_alta(self, user_id: str) -> dict:
        solicitud = self.repository.obtener_datos_para_recalculo_uno(user_id)
        if not solicitud:
            return None

        tem = (1 + solicitud["tasa_anual"] / 100) ** (1 / 12) - 1
        cuota_correcta = solicitud["monto"] * tem / (1 - (1 + tem) ** -solicitud["plazo_meses"])

        return {
            "id": solicitud["id"],
            "monto": solicitud["monto"],
            "plazo_meses": solicitud["plazo_meses"],
            "tasa_anual": solicitud["tasa_anual"],
            "cuota_registrada": solicitud["cuota_mensual"],
            "cuota_correcta": round(cuota_correcta, 2),
            "diferencia": round(solicitud["cuota_mensual"] - cuota_correcta, 2),
            "advertencia": "cuota_registrada calculada con fórmula TEA/12 incorrecta"
        }
