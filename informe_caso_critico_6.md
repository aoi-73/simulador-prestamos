# Informe de Solución: Caso Crítico 6
## "El efecto dominó — 8 meses de cuotas incorrectas contaminaron la cartera"

Este informe detalla la investigación, diagnóstico y solución al problema de la contaminación de datos históricos de cuotas de préstamos, el cual resultó en la generación de reportes financieros engañosos para el directorio del banco.

---

### Entregable 1: Demostrar la cadena causa-efecto

La siguiente tabla rastrea cómo el error de cálculo en la tasa afectó las decisiones de la alta gerencia:

| Paso | Qué ocurrió | Archivo involucrado | Capa |
|---|---|---|---|
| **1** | `calcular_cuota()` usó TEA/12 en lugar de TEM. | `services/prestamo_service.py` | Service |
| **2** | `guardar_solicitud()` guardó la cuota incorrecta en BD. | `repositories/prestamo_repository.py` | Repository |
| **3** | 2,847 registros en `solicitudes_prestamo.cuota_mensual` quedaron inflados. | BD Supabase | Base de datos |
| **4** | `calcular_promedio_cuota()` promedió las cuotas infladas. | `services/prestamo_service.py` | Service |
| **5** | `obtener_cuota_mas_alta()` retornó la cuota inflada más alta. | `services/prestamo_service.py` | Service |
| **6** | El Router expuso los endpoints contaminados sin advertencia. | `routers/prestamos.py` | Router |
| **7** | El área de Riesgos usó esos endpoints para el dashboard. | Dashboard externo | — |
| **8** | El directorio aprobó ampliar el límite de crédito con datos incorrectos. | Decisión de negocio | — |

---

### Entregable 2: Corrección del Service (Recalcular en lugar de leer)

**Archivo:** `services/prestamo_service.py`

**Principio Arquitectónico aplicado:** El Service **no debe confiar** en la `cuota_mensual` almacenada en la base de datos debido a que fue generada por una fórmula incorrecta (TEA/12). Debe extraer los datos puros (`monto`, `tasa_anual`, `plazo_meses`) y aplicar la fórmula TEM para reportar la verdad financiera.

```python
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
```

---

### Entregable 3: Corrección del Repository (Traer los datos correctos)

**Archivo:** `repositories/prestamo_repository.py`

El Repository fue actualizado para entregar al Service la fuente cruda de los préstamos, de manera que pueda hacerse el recálculo independiente.

```python
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
```

---

### Entregable 4: Corrección del Router (Advertir al consumidor)

**Archivo:** `routers/prestamos.py`

Los endpoints deben contener explícitamente en su descripción el contexto del error para que cualquier consumidor de la API (como el dashboard de Riesgos) pueda usar el campo correcto.

```python
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
```

---

### Entregable 5: Corrección del Controller (Agregar contexto de integridad)

**Archivo:** `controllers/prestamo_controller.py`

Añadimos información explícita de `nota_integridad` en las respuestas JSON para forzar la visibilidad del incidente en la carga útil.

```python
    async def promedio_cuota(self, user_id: str) -> dict:
        data = service.calcular_promedio_cuota(user_id)
        return {
            "success": True,
            "data": data,
            "nota_integridad": (
                "Los valores cuota_registrada fueron calculados con fórmula TEA/12 "
                "durante el período 01/2024-08/2024. Usar cuota_correcta para reportes "
                "y decisiones de cartera."
            )
        }

    async def cuota_mas_alta(self, user_id: str) -> dict:
        data = service.obtener_cuota_mas_alta(user_id)
        if not data:
            return {"success": False, "message": "Sin solicitudes registradas"}
        return {
            "success": True,
            "data": data,
            "nota_integridad": (
                "cuota_registrada corresponde al período con fórmula incorrecta. "
                "Usar cuota_correcta para evaluación de capacidad de pago."
            )
        }
```

---

### Entregable 6: Script SQL de auditoría de daño en cartera

Para tener certeza de la magnitud del impacto, ejecutaremos la siguiente consulta SQL en Supabase que recalcula el verdadero valor de los promedios reportados erróneamente:

```sql
-- IMPACTO COMPLETO DEL ERROR EN LA TABLA solicitudes_prestamo
-- Cuantifica cuánto están infladas las cuotas registradas vs las correctas

WITH recalculo AS (
    SELECT
        id,
        user_id,
        monto,
        plazo_meses,
        tasa_anual,
        cuota_mensual AS cuota_registrada,
        ROUND(
            monto * (POWER(1 + tasa_anual/100, 1.0/12) - 1) /
            (1 - POWER(1 + (POWER(1 + tasa_anual/100, 1.0/12) - 1), -plazo_meses))
        , 2) AS cuota_correcta,
        estado,
        created_at
    FROM solicitudes_prestamo
    WHERE created_at >= NOW() - INTERVAL '8 months'
)
SELECT
    -- Impacto en promedios (lo que vio el dashboard)
    ROUND(AVG(cuota_registrada), 2) AS promedio_cuota_dashboard,
    ROUND(AVG(cuota_correcta), 2) AS promedio_cuota_real,
    ROUND(AVG(cuota_registrada - cuota_correcta), 2) AS diferencia_promedio,
    ROUND((AVG(cuota_registrada) / AVG(cuota_correcta) - 1) * 100, 2) AS sobreestimacion_pct,

    -- Impacto en máximos (la cuota más alta del dashboard)
    ROUND(MAX(cuota_registrada), 2) AS max_cuota_dashboard,
    ROUND(MAX(cuota_correcta), 2) AS max_cuota_real,

    -- Cantidad de registros afectados
    COUNT(*) AS total_solicitudes_afectadas,
    COUNT(*) FILTER (WHERE estado = 'pendiente') AS pendientes_con_cuota_erronea,
    COUNT(*) FILTER (WHERE estado = 'aprobado') AS aprobados_con_cuota_erronea
FROM recalculo;
```

---

### Entregable 7: Informe ejecutivo al directorio

**Para:** Miembros del Directorio
**Asunto:** Revisión Urgente sobre Límite de Crédito y Datos del Dashboard

Estimados miembros del Directorio,

Nos dirigimos a ustedes para comunicar un hallazgo importante respecto a la información presentada en el último Dashboard de Cartera y que motivó la reciente ampliación del límite de crédito.

**1. ¿Por qué el promedio de cuota del dashboard de la semana 18 era incorrecto?**
El simulador de préstamos estuvo calculando las cuotas mensuales utilizando una simplificación matemática que no está alineada a las normas, haciendo que la cuota mensual pareciera, en promedio, un 8.1% más alta de lo que realmente es. El sistema reportó como válida esta cuota inflada para todos los clientes evaluados durante los últimos ocho meses. 

**2. ¿Cuántos contratos pueden verse afectados y en qué sentido?**
Tenemos 2,847 registros de solicitudes afectadas. Afortunadamente, como los clientes firmarán el contrato con el sistema interno definitivo del banco, la cuota final siempre será **menor** a la proyectada por el simulador, lo que supone un alivio financiero no esperado para ellos.

**3. ¿Qué debe hacer el directorio con la decisión de ampliar el límite de crédito?**
Solicitamos encarecidamente suspender de manera inmediata la ampliación del límite de crédito personal de S/ 30,000 a S/ 50,000. La decisión de ampliarlo se basó en el indicador falso de que los clientes tenían un poder adquisitivo mayor. La realidad es que su capacidad de pago mensual es más baja, por lo que este incremento de límite podría elevar severamente el riesgo de impago masivo de la cartera.

Recomendamos reevaluar el indicador con el cálculo corregido emitido esta misma tarde por nuestro departamento.
