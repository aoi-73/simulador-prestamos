import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_KEY", ""))

class PrestamoRepository:
    def insertar_solicitud(self, datos: dict) -> dict:
        """Inserta una solicitud de prestamo en la tabla 'solicitudes_prestamo'."""
        response = supabase.table("solicitudes_prestamo").insert({
            "user_id":       str(datos["user_id"]),
            "monto":         datos["monto"],
            "plazo_meses":   datos["plazo_meses"],
            "tasa_anual":    datos["tasa_anual"],
            "cuota_mensual": datos["cuota_mensual"],
            "proposito":     datos["proposito"],
            "estado":        "pendiente"
        }).execute()
        return response.data[0]

    def obtener_solicitudes_por_usuario(self, user_id: str) -> list:
        """Obtiene todas las solicitudes de un usuario."""
        response = supabase.table("solicitudes_prestamo") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .execute()
        return response.data

    def obtener_solicitud_por_id(self, solicitud_id: str) -> dict:
        """Obtiene una solicitud especifica por su ID."""
        response = supabase.table("solicitudes_prestamo") \
            .select("*") \
            .eq("id", solicitud_id) \
            .execute()
        if not response.data:
            return None
        return response.data[0]

    def eliminar_solicitud(self, solicitud_id: str) -> bool:
        """Elimina una solicitud que este en estado 'pendiente'."""
        response = supabase.table("solicitudes_prestamo") \
            .delete() \
            .eq("id", solicitud_id) \
            .eq("estado", "pendiente") \
            .execute()
        return len(response.data) > 0

    def obtener_datos_para_recalculo(self, user_id: str) -> list:
        """
        Trae los campos necesarios para recalcular la cuota con TEM.
        NO trae cuota_mensual porque ese campo está contaminado.
        El Service es quien calcula — el Repository solo provee los datos fuente.
        """
        response = supabase.table("solicitudes_prestamo") \
            .select("id, monto, plazo_meses, tasa_anual, cuota_mensual, estado") \
            .eq("user_id", user_id) \
            .execute()
        return response.data

    def obtener_datos_para_recalculo_uno(self, user_id: str) -> dict:
        """Trae la solicitud con mayor cuota registrada para recalcular."""
        response = supabase.table("solicitudes_prestamo") \
            .select("id, monto, plazo_meses, tasa_anual, cuota_mensual") \
            .eq("user_id", user_id) \
            .order("cuota_mensual", desc=True) \
            .limit(1) \
            .execute()
        return response.data[0] if response.data else None
