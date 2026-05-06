\# OPERACIÓN SIMULADOR



\## Historia de las prácticas que evitaron una crisis



```

"El código que nadie revisó estuvo activo 8 meses. En ese tiempo, 2,847 solicitudes de crédito llegaron a los

asesores de negocios con cuotas calculadas de forma incorrecta."

```

\## PRÓLOGO — Lo que nadie vio venir



Era martes por la mañana en la sede central de una importante entidad financiera del Perú.



El Departamento de Operaciones acababa de recibir un reporte inusual. Una asesora de negocios de la agencia



San Juan de Lurigancho en Lima reporto una inconsistencia en el calculo del cronograma de pagos de un



cliente. La gerente del dpto de operaciones, Bertha Bares llamo al Gerente de Tecnologias de Informacion (TI),



Jose Garipal.



\_"Hola Jose, buen dia, tengo un cliente aquí que dice que el simulador del homebanking le mostró una cuota de S/\_



\_946 para un crédito de S/ 10,000 a 12 meses. Yo le calculé la cuota con nuestra herramienta interna y me da S/\_



\_920. El cliente ya firmó la solicitud con la cuota del simulador. ¿Cuanto tiempo te llevara solucinarlo?"\_



\_"Hola Bertha ¿Cuántas solicitudes entraron por homebanking este mes?"\_



\_"317."\_



\_"317?... lo validare! Y lo atiendo a la brevedad!"\_



\_"Ok... te envio los detalles por correo."\_



El gerente de TI, Jose Garipal, colgó. Y llamo al \*\* Ing Waydo Pereyra, jefe del Sub Departamento de Desarrollo



de Software Homebanking\*\*, designandole la importante labor.



\## CAPÍTULO 1 — El equipo



En el piso 4 de la sede central, la \*\*Sub Departamento de Desarrollo de Software Homebanking\*\* tenía ese



mes a \*\*siete practicantes\*\* , todos en los últimos ciclos de Ingeniería de Sistemas e Informatica.



Sus nombres:



\*\*Las cuatro ingenieras:\*\*



```

Nombre Significado

```

```

Qori Oro en quechua

```

```

Sisa Flor en quechua

```

```

Illary Amanecer en quechua

```

```

Wayra Viento en quechua

```



\*\*Los tres ingenieros:\*\*



```

Nombre Significado

```

```

Kuntur Cóndor en quechua

```

```

Rimac El que habla en quechua

```

```

Tupac Noble, brillante en quechua

```

El \*\*Ing. Wardo Peyra\*\* , jefe del Sub Departamento de Desarrollo de Software Homebanking con 14 años en la



entidad, entró a la sala saludando a todos:



\_"Buenos dias señoritas!! jovenes!! Necesito que revisen el módulo de simulación de créditos del homebanking.\_



\_Tengo una denuncia de campo. Tienen 48 horas antes de que esto llegue a Cumplimiento Normativo."\_



Qori Mamani levantó la mano:



\_"¿Qué buscamos exactamente?"\_



\_"Un error en la fórmula de cálculo de cuotas. Si lo hay, necesito saber desde cuándo está activo, cuántas\_



\_solicitudes afectó y cuál es el impacto en soles. Cuando terminen, la economista del área de Riesgos va a venir a\_



\_explicarles por qué esto no es solo un bug de código."\_



Salió. Los siete practicantes se miraron.



\## CAPÍTULO 2 — Lo que encontraron



A las dos horas, Tupac encontró la línea exacta. Estaba en services/prestamo\_service.py:



```

\# Código activo en producción — homebanking

\# services/prestamo\_service.py ← CAPA SERVICE

```

```

def calcular\_cuota(self, monto: float, plazo\_meses: int, tasa\_anual: float) ->

dict:

r = (tasa\_anual / 100 ) / 12 # ← ERROR en línea 47: tasa NOMINAL, no

efectiva

factor = ( 1 + r) \*\* plazo\_meses

cuota = monto \* (r \* factor) / (factor - 1 )

return {

"monto": monto,

"cuota\_mensual": round(cuota, 2 ),

"total\_pagar": round(cuota \* plazo\_meses, 2 ),

"total\_interes": round(cuota \* plazo\_meses - monto, 2 ),

"plazo\_meses": plazo\_meses,

"tasa\_anual": tasa\_anual

}

```

Illary abrió el documento oficial de fórmulas de la entidad. Leyó en voz alta:



\_"TEM = (1 + TEA/100) elevado a 1/12, menos 1. No es TEA dividida entre 12."\_





Silencio.



\_"¿Cuánto es la diferencia?"\_ preguntó Kuntur Apaza.



Corrieron los números:



```

TEA Plazo Monto Cuota simulador Cuota correcta Diferencia

```

```

24% 12 S/ 10,000 S/ 946.40 S/ 920.02 S/ 26.

```

```

28% 24 S/ 20,000 S/ 1,073.22 S/ 1,021.15 S/ 52.

```

```

32% 36 S/ 35,000 S/ 1,474.31 S/ 1,384.96 S/ 89.

```

\_"Esperen"\_ , dijo Wayra. \_"Esto no es solo una diferencia de cuota. Si el cliente ve S/ 946 en el simulador y el asesor\_



\_le presenta S/ 920 en el contrato real... ¿qué pasa?"\_



\_"El cliente desconfía. Cree que le están cambiando las condiciones"\_ , respondió Sisa Quispe.



\_"Y si el contrato real sale más caro que el simulador, el cliente puede reclamar ante la SBS."\_



El Ing. Wardo Peyra entró en ese momento, como si hubiera escuchado desde afuera.



\_"Exacto. Eso es lo que va a explicar la economista."\_



\## CAPÍTULO 3 — La clase que nadie esperaba



La \*\*Eco. Maira Cellalo\*\* , del área de Riesgos, tenía 52 años. Había trabajado en la SBS durante 11 años antes de



pasarse al sector privado. No usó diapositivas. Se sentó en el borde de la mesa y empezó así:



\_"¿Alguno de ustedes ha visto a alguien del gota a gota?"\_



Todos asintieron.



\_"¿Saben por qué la gente les paga a esos prestamistas tasas de 300%, 400% anual, cuando pueden venir aquí y\_



\_pagar 28%?"\_



Nadie respondió.



\_"Porque no entienden cómo se calcula una cuota. Un señor saca S/ 200 del gota a gota un lunes. El viernes tiene\_



\_que devolver S/ 220. Parece poco. Pero eso es 10% en 4 días. Anualizado es más de 1,000%. Él no lo sabe. Solo ve\_



\_S/ 20 de interés y le parece manejable."\_



Hizo una pausa.



\_"Hace semanas salió en los medios el caso de una entidad financiera del norte del país intervenida por la SBS.\_



\_Casi un millón de personas afectadas. Uno de los factores: deterioro acelerado de cartera. ¿Saben qué es deterioro\_



\_de cartera?"\_



\_"Clientes que no pagan"\_ , dijo Rimac Ttito.



\_"Correcto. Y los clientes dejan de pagar cuando la cuota que firmaron no es la que podían pagar realmente.\_



\_Cuando el simulador les dijo una cosa y el contrato dijo otra."\_





Se paró. Fue a la pizarra y escribió:



```

FÓRMULA INCORRECTA — lo que tiene hoy el homebanking

(services/prestamo\_service.py):

```

```

tasa\_mensual = TEA / 12

Cuota = Monto × tasa\_mensual / (1 - (1 + tasa\_mensual)^(-n))

```

```

FÓRMULA CORRECTA — lo que exige la normativa SBS:

```

```

TEM = (1 + TEA/100)^(1/12) - 1

Cuota = Monto × TEM / (1 - (1 + TEM)^(-n))

```

\_"La diferencia entre estas dos líneas"\_ , dijo señalando la pizarra, \_"es la diferencia entre una entidad que informa\_



\_correctamente y una que puede ser sancionada por publicidad engañosa en canales digitales. El artículo 8 del\_



\_Reglamento de Transparencia de Información lo dice claro: el simulador es un canal oficial de información al\_



\_cliente."\_



Qori Mamani preguntó:



\_"¿Y cuánto tiempo lleva activo ese error?"\_



El Ing. Wardo Peyra respondió desde la puerta:



\_"El módulo fue desplegado hace 8 meses. En ese tiempo entraron 2,847 solicitudes por homebanking."\_



Nadie habló por varios segundos.



\_"Esas 2,847 solicitudes fueron asignadas a asesores de negocios de 23 agencias a nivel nacional. Algunos\_



\_contratos ya están firmados."\_



La Eco. Maira Cellalo completó:



\_"Su trabajo ahora no es solo corregir el código. Es entender el impacto completo: financiero, normativo y\_



\_operativo. Para eso se van a dividir en equipos."\_



\## CAPÍTULO 4 — La arquitectura que deben conocer



Antes de repartir los casos, el Ing. Wardo Peyra proyectó la arquitectura del backend en la pantalla:



```

ARQUITECTURA FASTAPI — Sub Depto. Desarrollo de Software Homebanking

Proyecto: devappweb\_s2\_m5\_fastapi\_supabase

```

```

Petición HTTP del cliente homebanking

│

▼

┌─────────────────────┐

│ routers/ │ ← CAPA 1: ROUTER

│ prestamos.py │ Define las URLs y métodos HTTP

│ │ @router.post("/simular")

```



```

│ │ @router.get("/solicitudes/{id}")

└────────┬────────────┘

│ llama a

▼

┌─────────────────────┐

│ controllers/ │ ← CAPA 2: CONTROLLER

│ prestamo\_ │ Recibe la petición validada

│ controller.py │ Extrae datos, llama al Service

│ │ Formatea la respuesta JSON

└────────┬────────────┘

│ llama a

▼

┌─────────────────────┐

│ services/ │ ← CAPA 3: SERVICE ← AQUÍ ESTÁ EL ERROR

│ prestamo\_ │ Lógica de negocio pura

│ service.py │ Fórmulas financieras

│ │ Reglas de validación

│ │ NO accede a BD directamente

└────────┬────────────┘

│ llama a

▼

┌─────────────────────┐

│ repositories/ │ ← CAPA 4: REPOSITORY

│ prestamo\_ │ Único que conoce Supabase

│ repository.py │ INSERT, SELECT, DELETE

│ │ Si cambia la BD, solo cambia aquí

└────────┬────────────┘

│ accede a

▼

┌─────────────────────┐

│ models/ │ ← SCHEMAS (Pydantic)

│ schemas.py │ Valida datos de entrada y salida

│ │ Define tipos y restricciones

│ │ Error 422 automático si falla

└─────────────────────┘

│

▼

SUPABASE (PostgreSQL)

tabla: solicitudes\_prestamo

```

\_"Cada caso que van a resolver"\_ , explicó el Ing. Wardo Peyra, \_"tiene un error en una capa específica. No es lo\_



\_mismo corregir el Service que corregir el Repository. Parte de la evaluación es que identifiquen exactamente en\_



\_qué capa está el problema y por qué."\_



La Eco. Maira Cellalo añadió:



\_"Y recuerden: el error financiero está en el Service porque allí vive la lógica de negocio. El Router no sabe de\_



\_fórmulas. El Repository no sabe de tasas. El Controller no calcula nada. Cada capa tiene una sola\_



\_responsabilidad."\_



\## CAPÍTULO 5 — La asignación





El Ing. Wardo Peyra repartió los casos:



\_"Los casos críticos 1 al 5 los resuelven en grupos de 6. Son los errores directos del simulador: la fórmula, el ITF, las\_



\_solicitudes mal asignadas a asesores, los duplicados y las validaciones. El caso crítico 6 lo resuelven como equipo\_



\_completo — los siete. Es el efecto sistémico: lo que pasó con los datos de cartera después de 8 meses con el error\_



\_activo. Es el caso más complejo porque no es corregir una línea de código. Es entender cómo ese error contaminó\_



\_los reportes que usa el directorio para tomar decisiones."\_



\_"Los casos operativos 7 al 12 los resuelven individualmente."\_



\_"Tienen hasta el viernes. El lunes exponen. Grupos críticos 1-5: 7 minutos. Caso crítico 6 grupo completo: 12\_



\_minutos. Individual: 4 minutos."\_



\_"Una última cosa"\_ , añadió la Eco. Maira Cellalo. \_"En 2024 intervinieron dos entidades financieras en menos de un\_



\_año. El sistema financiero peruano está bajo microscopio. Cada error en un canal digital es combustible para la\_



\_desconfianza. Ustedes no están corrigiendo un bug. Están protegiendo la relación entre esta entidad y sus\_



\_clientes."\_



Salió. Los siete practicantes abrieron sus laptops.



\# CASOS CRÍTICOS — GRUPOS DE 6



\## CASO CRÍTICO 1



\### "El simulador miente — 2,847 solicitudes comprometidas"



\*\*Contexto operativo:\*\* El homebanking calcula cuotas con tasa nominal mensual (TEA/12) en lugar de tasa



efectiva mensual (TEM). Error activo 8 meses. 2,847 solicitudes asignadas a asesores en 23 agencias con cuota



incorrecta.



\*\*Síntoma detectado en campo:\*\* Cliente ve S/ 946.40 en el simulador. Contrato del sistema interno refleja S/



920.02 (S/ 10,000 / 24% TEA / 12 meses). Cliente se niega a firmar.



\### Capa afectada: SERVICE



```

routers/prestamos.py ← NO afectado (solo define URLs)

controllers/prestamo\_ctrl.py ← NO afectado (solo coordina)

services/prestamo\_service.py ← AQUÍ ESTÁ EL ERROR

repositories/prestamo\_repo.py ← NO afectado (solo accede a BD)

models/schemas.py ← Revisar límites de validación

```

\### Código en producción con el error



\*\*Archivo:\*\* services/prestamo\_service.py





```

class PrestamoService:

```

```

def \_\_init\_\_(self):

self.repository = PrestamoRepository()

```

```

def calcular\_cuota(self, monto: float, plazo: int, tasa\_anual: float) -> dict:

\# ─────────────────────────────────────────────────────────

\# ERROR FINANCIERO: usa tasa nominal mensual (TEA / 12)

\# La normativa SBS exige Tasa Efectiva Mensual (TEM)

\# ─────────────────────────────────────────────────────────

r = (tasa\_anual / 100 ) / 12 # ← LÍNEA INCORRECTA

factor = ( 1 + r) \*\* plazo

cuota = monto \* (r \* factor) / (factor - 1 )

total = cuota \* plazo

```

```

return {

"monto": round(monto, 2 ),

"cuota\_mensual": round(cuota, 2 ),

"total\_pagar": round(total, 2 ),

"total\_interes": round(total - monto, 2 ),

"plazo\_meses": plazo,

"tasa\_anual": tasa\_anual

}

```

\### Lo que debe entregar el grupo



\*\*Entregable 1 — Diagnóstico técnico por capa\*\*



Explicar con palabras propias:



```

¿Por qué el error está en el Service y no en el Router ni en el Controller?

¿Qué responsabilidad tiene cada capa en la arquitectura FastAPI del proyecto?

Tabla comparativa TEA/12 vs TEM para tres escenarios (24%, 28%, 32%).

```

\*\*Entregable 2 — Corrección del Service\*\*



Archivo: services/prestamo\_service.py



```

class PrestamoService:

```

```

def \_\_init\_\_(self):

self.repository = PrestamoRepository()

```

```

def calcular\_cuota(self, monto: float, plazo: int, tasa\_anual: float) -> dict:

\# ─────────────────────────────────────────────────────────

\# CORRECCIÓN: Tasa Efectiva Mensual según normativa SBS

\# TEM = (1 + TEA/100)^(1/12) - 1

\# ─────────────────────────────────────────────────────────

tem = ( 1 + tasa\_anual / 100 ) \*\* ( 1 / 12 ) - 1 # ← LÍNEA CORREGIDA

cuota = monto \* tem / ( 1 - ( 1 + tem) \*\* -plazo)

```



```

total = cuota \* plazo

itf = round(monto \* 0.00005, 2 ) # ITF 0.005% — Ley 28194

```

```

return {

"monto": round(monto, 2 ),

"tem\_pct": round(tem \* 100 , 4 ),

"cuota\_mensual": round(cuota, 2 ),

"total\_pagar": round(total, 2 ),

"total\_intereses": round(total - monto, 2 ),

"itf": itf,

"plazo\_meses": plazo,

"tasa\_anual": tasa\_anual

}

```

```

async def guardar\_solicitud(self, datos: dict) -> dict:

\# El Service recalcula la cuota antes de guardar

\# No confía en el valor que viene del frontend

calculo = self.calcular\_cuota(

datos\["monto"], datos\["plazo\_meses"], datos\["tasa\_anual"]

)

datos\["cuota\_mensual"] = calculo\["cuota\_mensual"]

return self.repository.insertar\_solicitud(datos)

```

\*\*Entregable 3 — Verificar el Controller\*\*



El Controller no debe cambiar la lógica, pero debe verificar que pasa los parámetros correctamente al Service.



Archivo: controllers/prestamo\_controller.py



```

class PrestamoController:

```

```

async def simular(self, datos: PrestamoSimularRequest) -> dict:

\# El Controller solo coordina: extrae datos y llama al Service

\# No calcula, no accede a BD, no valida reglas financieras

resultado = service.calcular\_cuota(

datos.monto,

datos.plazo\_meses,

datos.tasa\_anual

)

return {"success": True, "data": resultado}

```

```

async def solicitar(self, datos: PrestamoSolicitudRequest) -> dict:

\# El Controller llama al Service pasando los datos del request

\# El Service se encarga de recalcular la cuota antes de guardar

calculo = service.calcular\_cuota(datos.monto, datos.plazo\_meses,

datos.tasa\_anual)

solicitud = await service.guardar\_solicitud({\*\*datos.dict(), \*\*calculo})

return {"success": True, "data": solicitud}

```

\*\*Entregable 4 — Corrección del Schema (models)\*\*





Archivo: models/schemas.py



```

from pydantic import BaseModel, Field, validator

```

```

class PrestamoSimularRequest(BaseModel):

monto: float = Field(ge= 500 , le= 300000 , description="Entre S/ 500 y S/

300,000")

plazo\_meses: int = Field(ge= 6 , le= 60 , description="Entre 6 y 60

meses")

tasa\_anual: float = Field(ge=13.35, le=114.13, description="TEA según

tarifario vigente")

```

```

\# Validación adicional: la TEA mínima varía por producto

\# Para el simulador general usamos el mínimo absoluto del tarifario

```

```

class PrestamoSimularResponse(BaseModel):

monto: float

tem\_pct: float # TEM calculada — nuevo campo informativo

cuota\_mensual: float

total\_pagar: float

total\_intereses: float

itf: float # ITF — nuevo campo requerido por transparencia

plazo\_meses: int

tasa\_anual: float

```

\*\*Entregable 5 — Script de auditoría SQL\*\*



```

\-- Identificar solicitudes con cuota calculada incorrectamente

\-- Diferencia mayor a S/ 5 respecto al cálculo correcto con TEM

```

```

SELECT

id,

user\_id,

monto,

plazo\_meses,

tasa\_anual,

cuota\_mensual AS cuota\_incorrecta,

ROUND(

monto \* (

POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1

) / (

1 - POWER( 1 + (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ), -plazo\_meses)

)

, 2 ) AS cuota\_correcta,

ROUND(

cuota\_mensual - (

monto \* (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ) /

( 1 - POWER( 1 + (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ), -plazo\_meses))

)

, 2 ) AS diferencia,

estado,

```



```

created\_at

FROM solicitudes\_prestamo

WHERE created\_at >= NOW() - INTERVAL '8 months'

AND ABS(

cuota\_mensual - (

monto \* (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ) /

( 1 - POWER( 1 + (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ), -plazo\_meses))

)

) > 5

ORDER BY diferencia DESC;

```

\*\*Entregable 6 — Comunicado interno al área comercial\*\*



Redactar el mensaje que TI envía a los 23 asesores explicando:



```

Qué ocurrió (en términos que entienda un asesor, no un desarrollador)

Qué deben hacer con solicitudes pendientes de firma

Cómo explicarlo al cliente sin generar pánico

Que la cuota correcta es más baja (esto es favorable para el cliente)

```

\*\*Pregunta de defensa del Ing. Wardo Peyra:\*\*



```

"¿Por qué el error no está en el Router ni en el Repository? ¿Qué hubiera pasado si la fórmula incorrecta

estuviera en el Controller en lugar del Service?"

```

\## CASO CRÍTICO 2



\### "El ITF invisible — el costo que nadie informó"



\*\*Contexto operativo:\*\* El simulador no incluye el ITF (0.005%) en el resumen de costos. La normativa obliga a



informar todos los costos en cualquier canal digital oficial. Un cliente presentó reclamo formal ante la SBS



porque el costo total del simulador no coincidió con el contrato.



\*\*Síntoma detectado:\*\* Endpoint /api/prestamos/simular retorna:



\#### {



```

"monto": 15000 ,

"cuota\_mensual": 687.54,

"total\_a\_pagar": 16500.96,

"total\_intereses": 1500.

}

```

El ITF (S/ 0.75 sobre S/ 15,000) no aparece. El contrato sí lo incluye.



\### Capas afectadas: SERVICE + MODELS (schemas)





```

routers/prestamos.py ← NO afectado

controllers/prestamo\_ctrl.py ← NO afectado

services/prestamo\_service.py ← Agregar cálculo de ITF

repositories/prestamo\_repo.py ← NO afectado

models/schemas.py ← Agregar campo itf al Response

```

\### Lo que debe entregar el grupo



\*\*Entregable 1 — Corrección del Service\*\*



Archivo: services/prestamo\_service.py



```

ITF\_TASA = 0.00005 # 0.005% — TUO Ley N° 28194

```

```

def calcular\_cuota(self, monto: float, plazo: int, tasa\_anual: float) -> dict:

tem = ( 1 + tasa\_anual / 100 ) \*\* ( 1 / 12 ) - 1

cuota = monto \* tem / ( 1 - ( 1 + tem) \*\* -plazo)

total = cuota \* plazo

itf = round(monto \* ITF\_TASA, 2 ) # ← NUEVO: ITF sobre monto

desembolsado

```

```

return {

"monto": round(monto, 2 ),

"tem\_pct": round(tem \* 100 , 4 ),

"cuota\_mensual": round(cuota, 2 ),

"total\_intereses": round(total - monto, 2 ),

"itf": itf, # ← NUEVO campo

"importe\_a\_recibir": round(monto - itf, 2 ), # ← NUEVO: monto neto al

cliente

"total\_a\_pagar": round(total, 2 ),

"plazo\_meses": plazo,

"tasa\_anual": tasa\_anual

}

```

\*\*Entregable 3 — Corrección del Schema (models)\*\*



Archivo: models/schemas.py



```

class PrestamoSimularResponse(BaseModel):

monto: float

tem\_pct: float

cuota\_mensual: float

total\_intereses: float

itf: float # ← NUEVO campo obligatorio

importe\_a\_recibir: float # ← NUEVO: monto neto tras descontar ITF

total\_a\_pagar: float

```



```

plazo\_meses: int

tasa\_anual: float

```

\*\*Entregable 4 — Tabla de ITF por monto frecuente\*\*



```

Monto solicitado ITF (0.005%) Importe a recibir

```

```

S/ 2,000 S/ 0.10 S/ 1,999.

```

```

S/ 5,000 S/ 0.25 S/ 4,999.

```

```

S/ 10,000 S/ 0.50 S/ 9,999.

```

```

S/ 20,000 S/ 1.00 S/ 19,999.

```

```

S/ 50,000 S/ 2.50 S/ 49,997.

```

\*\*Entregable 5 — Prueba en Postman\*\*



Captura mostrando que el endpoint corregido retorna el campo itf correctamente para un crédito de S/



8,000.



\*\*Pregunta de defensa del Ing. Wardo Peyra:\*\*



```

"¿El ITF se guarda en la tabla solicitudes\_prestamo? Si no, ¿dónde debe vivir ese dato? ¿Modifica el

Repository o solo el Service y el Schema?"

```

\## CASO CRÍTICO 3



\### "La fuerza de ventas en caos — 23 agencias con datos incorrectos"



\*\*Contexto operativo:\*\* El CRM asigna automáticamente cada solicitud del homebanking a un asesor según zona



geográfica. Las 2,847 solicitudes con cuota incorrecta ya están en los pipelines de 23 agencias. Los asesores



citan la cuota del simulador como referencia. 47 solicitudes tienen estado "cliente no continuó el proceso" por



discrepancia de cuotas.



\*\*Síntoma detectado:\*\*



```

\-- Solicitudes donde el cliente abandonó el proceso

SELECT motivo\_abandono, COUNT(\*) as casos

FROM solicitudes\_prestamo

WHERE estado = 'cliente\_no\_continuo'

AND created\_at >= NOW() - INTERVAL '8 months'

GROUP BY motivo\_abandono

ORDER BY casos DESC;

\-- Resultado principal: "discrepancia entre cuota informada y cuota del contrato" →

47 casos

```

\### Capas afectadas: SERVICE + REPOSITORY + CONTROLLER





```

routers/prestamos.py ← NO afectado

controllers/prestamo\_ctrl.py ← Verificar que no confíe en cuota del frontend

services/prestamo\_service.py ← Recalcular cuota antes de guardar

repositories/prestamo\_repo.py ← Agregar consulta de solicitudes afectadas

models/schemas.py ← NO afectado

```

\### Lo que debe entregar el grupo



\*\*Entregable 1 — Corrección del Service: recalcular antes de guardar\*\*



Archivo: services/prestamo\_service.py



```

async def guardar\_solicitud(self, datos: dict) -> dict:

\# REGLA CRÍTICA: El Service NUNCA confía en la cuota que viene del frontend

\# Siempre recalcula con TEM antes de persistir

calculo = self.calcular\_cuota(

datos\["monto"],

datos\["plazo\_meses"],

datos\["tasa\_anual"]

)

\# Sobreescribe la cuota\_mensual con el valor correcto

datos\["cuota\_mensual"] = calculo\["cuota\_mensual"]

return self.repository.insertar\_solicitud(datos)

```

\*\*Entregable 2 — Verificar el Controller: no debe recibir cuota del cliente\*\*



Archivo: controllers/prestamo\_controller.py



```

async def solicitar(self, datos: PrestamoSolicitudRequest) -> dict:

\# El Controller no recibe cuota\_mensual del cliente

\# El Service la calcula internamente

\# Si el schema tiene cuota\_mensual como campo de entrada, eliminarlo

solicitud = await service.guardar\_solicitud(datos.dict())

return {"success": True, "data": solicitud}

```

\*\*Entregable 3 — Nueva consulta en el Repository\*\*



Archivo: repositories/prestamo\_repository.py



```

def obtener\_solicitudes\_afectadas(self, meses\_atras: int = 8 ) -> list:

"""Obtiene solicitudes con posible cuota incorrecta para auditoría."""

response = supabase.rpc("solicitudes\_con\_cuota\_incorrecta", {

"meses": meses\_atras

}).execute()

return response.data

```



```

def obtener\_solicitudes\_pendientes\_por\_agencia(self, codigo\_agencia: str) -> list:

"""Para que cada asesor vea solo sus solicitudes pendientes."""

response = supabase.table("solicitudes\_prestamo") \\

.select("\*, asesores!inner(codigo\_agencia)") \\

.eq("asesores.codigo\_agencia", codigo\_agencia) \\

.eq("estado", "pendiente") \\

.order("created\_at", desc=True) \\

.execute()

return response.data

```

\*\*Entregable 4 — Script de recálculo masivo en SQL\*\*



```

\-- Recalcular cuota correcta para todas las solicitudes afectadas

\-- y mostrar la diferencia para priorizar el contacto con clientes

```

```

WITH solicitudes\_recalculadas AS (

SELECT

id,

user\_id,

monto,

plazo\_meses,

tasa\_anual,

cuota\_mensual AS

cuota\_incorrecta,

ROUND(

monto \* (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ) /

( 1 - POWER( 1 + (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ), -plazo\_meses))

, 2 ) AS cuota\_correcta,

estado,

created\_at

FROM solicitudes\_prestamo

WHERE created\_at >= NOW() - INTERVAL '8 months'

AND estado = 'pendiente'

)

SELECT

\*,

(cuota\_incorrecta - cuota\_correcta) AS diferencia,

CASE

WHEN (cuota\_incorrecta - cuota\_correcta) > 50 THEN 'URGENTE — llamar hoy'

WHEN (cuota\_incorrecta - cuota\_correcta) > 20 THEN 'PRIORIDAD — llamar esta

semana'

ELSE 'NORMAL — incluir en siguiente contacto'

END AS prioridad\_contacto

FROM solicitudes\_recalculadas

ORDER BY diferencia DESC;

```

\*\*Pregunta de defensa del Ing. Wardo Peyra:\*\*



```

"¿Por qué el Service debe recalcular la cuota antes de pasarla al Repository, en lugar de confiar en el valor

que viene del Controller?"

```



\## CASO CRÍTICO 4



\### "Doble solicitud — el botón que se presionó dos veces"



\*\*Contexto operativo:\*\* El homebanking no protege contra solicitudes duplicadas. Con conexión lenta, el botón



"Solicitar" puede ejecutarse dos veces en menos de 3 segundos. El CRM asigna las dos solicitudes a dos



asesores distintos. El cliente recibe dos llamadas del banco para el mismo crédito. 23 casos confirmados el



último mes.



\*\*Síntoma detectado:\*\*



```

SELECT user\_id, monto, plazo\_meses, COUNT(\*) as duplicados,

EXTRACT(EPOCH FROM (MAX(created\_at) - MIN(created\_at))) as

segundos\_diferencia

FROM solicitudes\_prestamo

WHERE estado = 'pendiente'

GROUP BY user\_id, monto, plazo\_meses

HAVING COUNT(\*) > 1

AND EXTRACT(EPOCH FROM (MAX(created\_at) - MIN(created\_at))) < 10 ;

\-- Resultado: 23 pares de solicitudes duplicadas

```

\### Capas afectadas: SERVICE + REPOSITORY + MODELS



```

routers/prestamos.py ← NO afectado

controllers/prestamo\_ctrl.py ← NO afectado

services/prestamo\_service.py ← Verificar duplicado antes de guardar

repositories/prestamo\_repo.py ← Agregar consulta de duplicado reciente

models/schemas.py ← NO afectado (validación estructural)

```

\### Lo que debe entregar el grupo



\*\*Entregable 1 — Diagnóstico por capa\*\*



Explicar en qué capa debería existir la validación de duplicados y por qué no es responsabilidad del Router ni



del Controller. Describir las tres capas de protección posibles: frontend, Service, base de datos.



\*\*Entregable 2 — Corrección del Service\*\*



Archivo: services/prestamo\_service.py



```

async def guardar\_solicitud(self, datos: dict) -> dict:

\# CAPA 1: El Service verifica si ya existe solicitud idéntica

\# en los últimos 30 segundos antes de persistir

duplicado = self.repository.buscar\_solicitud\_reciente(

user\_id = datos\["user\_id"],

monto = datos\["monto"],

```



```

plazo\_meses = datos\["plazo\_meses"],

segundos = 30

)

if duplicado:

\# En lugar de error, retorna la solicitud existente

\# El cliente obtiene el mismo resultado sin doble registro

return duplicado

```

```

\# Si no hay duplicado, recalcula y persiste

calculo = self.calcular\_cuota(datos\["monto"], datos\["plazo\_meses"],

datos\["tasa\_anual"])

datos\["cuota\_mensual"] = calculo\["cuota\_mensual"]

return self.repository.insertar\_solicitud(datos)

```

\*\*Entregable 3 — Nueva consulta en el Repository\*\*



Archivo: repositories/prestamo\_repository.py



```

def buscar\_solicitud\_reciente(self, user\_id: str, monto: float,

plazo\_meses: int, segundos: int = 30 ) -> dict:

"""Busca solicitud idéntica en los últimos N segundos — previene duplicados."""

from datetime import datetime, timedelta

desde = (datetime.utcnow() - timedelta(seconds=segundos)).isoformat()

```

```

response = supabase.table("solicitudes\_prestamo") \\

.select("\*") \\

.eq("user\_id", user\_id) \\

.eq("monto", monto) \\

.eq("plazo\_meses", plazo\_meses) \\

.gte("created\_at", desde) \\

.order("created\_at", desc=True) \\

.limit( 1 ) \\

.execute()

```

```

return response.data\[ 0 ] if response.data else None

```

\*\*Entregable 4 — Constraint en base de datos (segunda capa de protección)\*\*



```

\-- Índice único parcial: no puede haber dos solicitudes del mismo usuario

\-- con el mismo monto y plazo dentro de un intervalo de 30 segundos

\-- (implementado a nivel de BD como segunda línea de defensa)

```

```

CREATE UNIQUE INDEX idx\_no\_duplicados\_solicitud

ON solicitudes\_prestamo (user\_id, monto, plazo\_meses,

DATE\_TRUNC('minute', created\_at));

```

```

\-- Explicar por qué esto complementa (no reemplaza) la validación del Service

```

\*\*Entregable 5 — Script de limpieza de duplicados existentes\*\*





```

\-- Eliminar el duplicado más reciente de cada par

\-- Conservar siempre el primero cronológicamente

```

```

DELETE FROM solicitudes\_prestamo

WHERE id IN (

SELECT id FROM (

SELECT id,

ROW\_NUMBER() OVER (

PARTITION BY user\_id, monto, plazo\_meses

ORDER BY created\_at DESC

) AS rn

FROM solicitudes\_prestamo

WHERE estado = 'pendiente'

AND (user\_id, monto, plazo\_meses) IN (

SELECT user\_id, monto, plazo\_meses

FROM solicitudes\_prestamo

WHERE estado = 'pendiente'

GROUP BY user\_id, monto, plazo\_meses

HAVING COUNT(\*) > 1

)

) ranked

WHERE rn = 1

);

```

\*\*Entregable 6 — Prueba de doble click en Postman\*\*



Describir y capturar cómo simular dos peticiones POST simultáneas al mismo endpoint y mostrar que el



sistema corregido retorna la misma solicitud en ambas respuestas en lugar de crear dos registros.



\*\*Pregunta de defensa del Ing. Wardo Peyra:\*\*



```

"Si la validación de duplicados está tanto en el Service como en la base de datos, ¿cuál de las dos es la más

importante y por qué? ¿Qué pasa si solo tienes una de las dos?"

```

\## CASO CRÍTICO 5



\### "El simulador sin límites — cualquier número entra"



\*\*Contexto operativo:\*\* El endpoint de simulación acepta valores fuera del rango normativo sin retornar error. Se



detectaron simulaciones con TEA de 200%, monto S/ 0 y plazo de 120 meses. Estos casos generan datos basura



en los registros y podrían ser explorados para detectar vulnerabilidades del sistema.



\*\*Síntoma detectado:\*\*



```

\# Estas peticiones reciben HTTP 200 en lugar de HTTP 400/422:

POST /api/prestamos/simular { "monto": 0, "plazo\_meses": 120, "tasa\_anual": 200 }

POST /api/prestamos/simular { "monto": -5000, "plazo\_meses": 3, "tasa\_anual": 28 }

POST /api/prestamos/simular { "monto": 500000, "plazo\_meses": 0, "tasa\_anual": 0 }

```



\### Capas afectadas: MODELS (schemas) + SERVICE + ROUTER



```

routers/prestamos.py ← Verificar que los decoradores sean correctos

controllers/prestamo\_ctrl.py ← NO afectado

services/prestamo\_service.py ← Segunda capa de validación de negocio

repositories/prestamo\_repo.py ← NO afectado

models/schemas.py ← PRIMERA CAPA — validación de formato y rangos

```

\### Lo que debe entregar el grupo



\*\*Entregable 1 — Tabla de validaciones requeridas por tarifario\*\*



```

Campo Mínimo Máximo Tipo de error si falla Fuente

```

```

monto S/ 500 S/ 300,000 HTTP 422 — Pydantic Reglamento interno

```

```

plazo\_meses 6 60 HTTP 422 — Pydantic Tarifario vigente

```

```

tasa\_anual 13.35% 114.13% HTTP 422 — Pydantic Tarifario SBS

```

\*\*Entregable 2 — Corrección del Schema (PRIMERA CAPA — models)\*\*



Archivo: models/schemas.py



```

from pydantic import BaseModel, Field, validator

```

```

class PrestamoSimularRequest(BaseModel):

monto: float = Field(

ge= 500 ,

le= 300000 ,

description="Monto entre S/ 500 y S/ 300,000 según reglamento"

)

plazo\_meses: int = Field(

ge= 6 ,

le= 60 ,

description="Plazo entre 6 y 60 meses según tarifario vigente"

)

tasa\_anual: float = Field(

ge=13.35,

le=114.13,

description="TEA según tarifario SBS vigente"

)

```

```

class Config:

schema\_extra = {

"example": {

"monto": 10000 ,

"plazo\_meses": 12 ,

"tasa\_anual": 25.

```



\#### }



\#### }



\*\*Entregable 3 — Validación de negocio en el Service (SEGUNDA CAPA — service)\*\*



Archivo: services/prestamo\_service.py



```

def validar\_parametros\_credito(self, monto: float, plazo: int, tea: float) -> None:

"""Segunda capa de validación — reglas de negocio que Pydantic no puede

validar."""

\# Pydantic valida el formato; el Service valida las reglas de negocio

if tea < 13.35 or tea > 114.13:

raise ValueError(f"TEA {tea}% fuera del rango normativo (13.35% -

114.13%)")

if plazo < 6 or plazo > 60 :

raise ValueError(f"Plazo {plazo} meses fuera del rango permitido (6 - 60)")

if monto < 500 or monto > 300000 :

raise ValueError(f"Monto S/ {monto} fuera del rango permitido (500 -

300,000)")

```

```

def calcular\_cuota(self, monto: float, plazo: int, tasa\_anual: float) -> dict:

self.validar\_parametros\_credito(monto, plazo, tasa\_anual) # ← Validar primero

tem = ( 1 + tasa\_anual / 100 ) \*\* ( 1 / 12 ) - 1

cuota = monto \* tem / ( 1 - ( 1 + tem) \*\* -plazo)

\# ... resto del cálculo

```

\*\*Entregable 4 — Verificar el Router\*\*



Archivo: routers/prestamos.py



```

from fastapi import APIRouter, HTTPException

from models.schemas import PrestamoSimularRequest

from controllers.prestamo\_controller import PrestamoController

```

```

router = APIRouter()

controller = PrestamoController()

```

```

@router.post(

"/simular",

summary="Simular cuota de préstamo",

response\_description="Cuota mensual y cronograma calculados con TEM"

)

async def simular\_prestamo(datos: PrestamoSimularRequest):

\# El Router solo pasa los datos validados al Controller

\# Pydantic ya validó el formato antes de llegar aquí

\# Si Pydantic falla, retorna 422 automáticamente — no llega al Controller

try:

return await controller.simular(datos)

```



```

except ValueError as e:

raise HTTPException(status\_code= 400 , detail=str(e))

```

\*\*Entregable 5 — Pruebas de los 6 casos borde en Postman\*\*



```

\# Input Respuesta esperada Capa que rechaza

```

```

1 monto = 0 HTTP 422 Pydantic (Schema)

```

```

2 monto = -5000 HTTP 422 Pydantic (Schema)

```

```

3 monto = 300001 HTTP 422 Pydantic (Schema)

```

```

4 plazo\_meses = 5 HTTP 422 Pydantic (Schema)

```

```

5 plazo\_meses = 61 HTTP 422 Pydantic (Schema)

```

```

6 tasa\_anual = 114.14 HTTP 422 Pydantic (Schema)

```

\*\*Pregunta de defensa del Ing. Wardo Peyra:\*\*



```

"¿Por qué ponemos validaciones tanto en el Schema Pydantic (models) como en el Service? ¿No es

redundante? Explica qué valida cada capa y qué pasaría si solo tuvieras una de las dos."

```

\## CASO CRÍTICO 6



\### "El efecto dominó — 8 meses de cuotas incorrectas contaminaron la cartera"



\*\*Practicantes:\*\* Kuntur, Rimac, Wayra, Illary, Sisa, Qori y Tupac (grupo completo)



```

"Encontraron la línea incorrecta en el Service. Eso es lo visible. Lo que tienen que entender ahora es lo

invisible: qué pasó con los 2,847 registros que esa línea generó durante 8 meses. Porque esos registros

siguen en la base de datos. Y el área de Riesgos los usa para tomar decisiones todos los lunes." — Ing.

Wardo Peyra

```

\### Contexto operativo



El jueves por la tarde, cuando los cinco grupos ya habían presentado los casos críticos 1 al 5 y parecía que lo



más difícil había pasado, el Ing. Wardo Peyra entró a la sala con una impresión en la mano.



Era un reporte del área de Riesgos. Lo puso sobre la mesa sin decir nada.



La Eco. Maira Cellalo lo leyó en voz alta:



\_"Dashboard Ejecutivo de Cartera — Semana 18. Cuota mensual promedio de solicitudes: S/ 687.32.\_



\_Recomendación: la cartera muestra una cuota promedio manejable para el segmento objetivo. Se aprueba\_



\_ampliar el límite de crédito personal de S/ 30,000 a S/ 50,000."\_



Silencio.



\_"¿Saben de dónde viene ese S/ 687.32?"\_ , preguntó el Ing. Wardo Peyra.





Nadie respondió.



\_"Del endpoint GET /api/prestamos/promedio-cuota. El mismo módulo del simulador que corrigieron esta\_



\_semana. Ese endpoint calcula el promedio de las cuota\_mensual guardadas en la tabla\_



\_solicitudes\_prestamo. Y como descubrieron en el caso crítico 1, todas esas cuotas fueron calculadas con\_



\_TEA/12 durante 8 meses. El promedio que el área de Riesgos presentó al directorio el lunes pasado está inflado.\_



\_No refleja la capacidad de pago real de los clientes."\_



Qori fue la primera en entenderlo:



\_"El error del simulador no solo afectó lo que el cliente vio en pantalla. Afectó los datos que quedaron guardados\_



\_en la base de datos. Y esos datos contaminados alimentan los reportes de Riesgos."\_



\_"Exacto"\_ , dijo la Eco. Maira Cellalo. \_"El caso crítico 6 no es un nuevo error. Es el mismo error del caso 1, pero visto\_



\_desde arriba. Desde el impacto que tuvo en la información que usa el directorio para tomar decisiones de\_



\_cartera."\_



\### El origen: un solo error raíz con tres efectos en cadena



Todo parte del error detectado en el \*\*Caso Crítico 1\*\* : la función calcular\_cuota() en



services/prestamo\_service.py usó TEA/12 en lugar de TEM durante 8 meses.



Ese error produjo tres efectos en cadena que ahora contaminan los reportes de cartera:



```

ERROR RAÍZ (Caso Crítico 1)

services/prestamo\_service.py — línea 47

r = (tasa\_anual / 100) / 12 ← fórmula incorrecta

│

│ generó cuotas infladas que se guardaron en la BD

│ durante 8 meses en 2,847 solicitudes

│

▼

┌─────────────────────────────────────────────────────────┐

│ tabla: solicitudes\_prestamo │

│ campo: cuota\_mensual │

│ │

│ 2,847 registros con cuota\_mensual INFLADA │

│ Ejemplo real: │

│ monto=10,000 / TEA=24% / plazo=12 │

│ Cuota guardada: S/ 946.40 (incorrecta) │

│ Cuota correcta: S/ 920.02 (con TEM) │

│ Diferencia: S/ 26.38 por registro │

└──────────┬──────────────────────────────────────────────┘

│

│ los datos contaminados alimentan 3 endpoints

│ que usa el área de Riesgos cada lunes

│

┌─────┴──────────────────────────────────┐

│ │

▼ ▼

EFECTO 1 EFECTO 2

```



```

GET /api/prestamos/promedio-cuota GET /api/prestamos/cuota-mas-alta

services/prestamo\_service.py services/prestamo\_service.py

AVG(cuota\_mensual) ORDER BY cuota\_mensual DESC

→ Promedia cuotas infladas → Retorna la cuota inflada más alta

→ S/ 687.32 en lugar de S/ 631.45 → S/ 2,891.40 en lugar de S/ 2,734.18

→ Referencia incorrecta para → Referencia incorrecta para evaluar

nuevos productos capacidad de pago máxima

│ │

└──────────────────┬─────────────────────┘

│

▼

EFECTO 3

El área de Riesgos construye el

Dashboard Ejecutivo de Cartera con

datos contaminados y el directorio

aprueba ampliar el límite de crédito

basándose en una cuota promedio

que no existe

```

\### El dashboard que llegó al directorio



\#### DASHBOARD EJECUTIVO DE CARTERA — SEMANA 18



```

Fuente: Homebanking Backend — GET /api/prestamos/promedio-cuota

GET /api/prestamos/cuota-mas-alta

Generado: lunes 07:00 AM

```

```

┌──────────────────────────────────────────────────────────────┐

│ INDICADOR VALOR REPORTADO ORIGEN DEL DATO │

├──────────────────────────────────────────────────────────────┤

│ Cuota mensual promedio S/ 687.32 AVG(cuota\_mensual│

│ de 2,847 registros│

│ con fórmula TEA/12│

│ │

│ Cuota mensual más alta S/ 2,891.40 MAX(cuota\_mensual│

│ con fórmula TEA/12│

└──────────────────────────────────────────────────────────────┘

```

```

ANÁLISIS DEL ÁREA DE RIESGOS:

"La cuota promedio de S/ 687.32 indica que el segmento objetivo

tiene capacidad de pago holgada. Se recomienda ampliar el límite

de crédito personal de S/ 30,000 a S/ 50,000."

```

```

DECISIÓN DEL DIRECTORIO: APROBADA

```

Los valores correctos, recalculando con TEM sobre los mismos 2,847 registros:



\#### DASHBOARD CORREGIDO — SEMANA 18



\#### ┌──────────────────────────────────────────────────────────────┐





\#### │ INDICADOR VALOR CORRECTO DIFERENCIA │



\#### ├──────────────────────────────────────────────────────────────┤



```

│ Cuota mensual promedio S/ 631.45 -S/ 55.87 (-8.1%) │

│ Cuota mensual más alta S/ 2,734.18 -S/ 157.22 (-5.4%)│

└──────────────────────────────────────────────────────────────┘

```

```

ANÁLISIS CORRECTO:

La cuota promedio real es 8.1% menor que la reportada.

Esto indica que el segmento tiene MENOR capacidad de absorber

deuda de lo que el dashboard sugería.

La decisión de ampliar el límite debe revisarse con datos reales.

```

\### Capas afectadas: SERVICE + REPOSITORY + CONTROLLER + ROUTER



```

routers/prestamos.py ← Expone los endpoints contaminados al área de

Riesgos

No valida que los datos de salida sean

consistentes

```

```

controllers/prestamo\_ctrl.py ← Retransmite los datos contaminados sin cuestionar

No tiene lógica de verificación de integridad

```

```

services/prestamo\_service.py ← ORIGEN PRINCIPAL DEL PROBLEMA

calcular\_promedio\_cuota(): promedia cuota\_mensual

guardada en lugar de recalcular con TEM

obtener\_cuota\_mas\_alta(): retorna cuota de BD

sin recalcular con TEM

```

```

repositories/prestamo\_repo.py ← Lee cuota\_mensual de la BD sin advertir

que ese valor fue calculado con fórmula incorrecta

No hay mecanismo de detección de datos corruptos

```

```

models/schemas.py ← El response schema de promedio\_cuota no distingue

entre cuota registrada y cuota correcta

No hay campo que indique la fórmula usada

```

\### Lo que debe entregar el grupo



\*\*Entregable 1 — Demostrar la cadena causa-efecto\*\*



Tabla que muestra el recorrido del error desde el código hasta la decisión del directorio:



```

Paso Qué ocurrió Archivo involucrado Capa

```

\#### 1



```

calcular\_cuota() usó TEA/12 en lugar

de TEM

```

```

services/prestamo\_service.py Service

```



```

Paso Qué ocurrió Archivo involucrado Capa

```

\#### 2



```

guardar\_solicitud() guardó la cuota

incorrecta en BD

```

```

repositories/prestamo\_repository.py Repository

```

\#### 3



```

2,847 registros en

solicitudes\_prestamo.cuota\_mensual

quedaron inflados

```

```

BD Supabase

```

```

Base de

datos

```

\#### 4



```

calcular\_promedio\_cuota() promedió

las cuotas infladas

```

```

services/prestamo\_service.py Service

```

\#### 5



```

obtener\_cuota\_mas\_alta() retornó la

cuota inflada más alta

```

```

services/prestamo\_service.py Service

```

\#### 6



```

El Router expuso los endpoints

contaminados sin advertencia

```

```

routers/prestamos.py Router

```

\#### 7



```

El área de Riesgos usó esos endpoints

para el dashboard

```

```

Dashboard externo —

```

\#### 8



```

El directorio aprobó ampliar el límite de

crédito con datos incorrectos

```

```

Decisión de negocio —

```

\*\*Entregable 2 — Corrección del Service: recalcular en lugar de leer\*\*



Archivo: services/prestamo\_service.py



El principio central de la corrección: \*\*el Service nunca debe confiar en cuota\_mensual guardada en la BD\*\*



\*\*porque ese valor fue calculado con la fórmula incorrecta\*\*. Siempre debe recalcular usando monto,



tasa\_anual y plazo\_meses con la TEM correcta.



```

\# CORRECCIÓN: calcular\_promedio\_cuota()

\# ANTES: promediaba cuota\_mensual guardada en BD (contaminada)

\# DESPUÉS: recalcula cada cuota con TEM antes de promediar

```

```

def calcular\_promedio\_cuota(self, user\_id: str) -> dict:

\# El Repository trae monto, plazo y tasa — NO cuota\_mensual

\# porque ese campo está contaminado en la BD

solicitudes = self.repository.obtener\_datos\_para\_recalculo(user\_id)

if not solicitudes:

return {"promedio\_cuota\_correcto": 0 , "cantidad": 0 }

```

```

cuotas\_registradas = \[]

cuotas\_correctas = \[]

```

```

for s in solicitudes:

\# Cuota como está guardada en BD (con error)

cuotas\_registradas.append(s\["cuota\_mensual"])

```

```

\# Cuota recalculada con TEM correcta

tem = ( 1 + s\["tasa\_anual"] / 100 ) \*\* ( 1 / 12 ) - 1

cuota = s\["monto"] \* tem / ( 1 - ( 1 + tem) \*\* -s\["plazo\_meses"])

```



```

cuotas\_correctas.append(round(cuota, 2 ))

```

```

prom\_registrado = sum(cuotas\_registradas) / len(cuotas\_registradas)

prom\_correcto = sum(cuotas\_correctas) / len(cuotas\_correctas)

```

```

return {

"promedio\_cuota\_registrado": round(prom\_registrado, 2 ), # dato contaminado

"promedio\_cuota\_correcto": round(prom\_correcto, 2 ), # dato real

"diferencia": round(prom\_registrado - prom\_correcto, 2 ),

"pct\_sobreestimacion": round((prom\_registrado / prom\_correcto - 1 ) \*

100 , 2 ),

"cantidad\_solicitudes": len(solicitudes),

"advertencia": "cuota\_registrada calculada con fórmula TEA/12

incorrecta"

}

```

```

\# CORRECCIÓN: obtener\_cuota\_mas\_alta()

\# ANTES: retornaba la solicitud con mayor cuota\_mensual guardada (contaminada)

\# DESPUÉS: recalcula con TEM y muestra ambos valores para comparar

```

```

def obtener\_cuota\_mas\_alta(self, user\_id: str) -> dict:

solicitud = self.repository.obtener\_datos\_para\_recalculo\_uno(user\_id)

if not solicitud:

return None

```

```

tem = ( 1 + solicitud\["tasa\_anual"] / 100 ) \*\* ( 1 / 12 ) - 1

cuota\_correcta = solicitud\["monto"] \* tem / (

1 - ( 1 + tem) \*\* -solicitud\["plazo\_meses"]

)

```

```

return {

"id": solicitud\["id"],

"monto": solicitud\["monto"],

"plazo\_meses": solicitud\["plazo\_meses"],

"tasa\_anual": solicitud\["tasa\_anual"],

"cuota\_registrada": solicitud\["cuota\_mensual"], # valor contaminado

"cuota\_correcta": round(cuota\_correcta, 2 ), # valor real con TEM

"diferencia": round(solicitud\["cuota\_mensual"] - cuota\_correcta,

2 ),

"advertencia": "cuota\_registrada calculada con fórmula TEA/12

incorrecta"

}

```

\*\*Entregable 3 — Corrección del Repository: traer los datos correctos\*\*



Archivo: repositories/prestamo\_repository.py



```

\# NUEVO MÉTODO: obtener\_datos\_para\_recalculo()

\# En lugar de traer cuota\_mensual, trae monto + tasa + plazo

\# para que el Service pueda recalcular con TEM correcta

```



```

def obtener\_datos\_para\_recalculo(self, user\_id: str) -> list:

"""

Trae los campos necesarios para recalcular la cuota con TEM.

NO trae cuota\_mensual porque ese campo está contaminado.

El Service es quien calcula — el Repository solo provee los datos fuente.

"""

response = supabase.table("solicitudes\_prestamo") \\

.select("id, monto, plazo\_meses, tasa\_anual, cuota\_mensual, estado") \\

.eq("user\_id", user\_id) \\

.execute()

return response.data

```

```

def obtener\_datos\_para\_recalculo\_uno(self, user\_id: str) -> dict:

"""Trae la solicitud con mayor cuota registrada para recalcular."""

response = supabase.table("solicitudes\_prestamo") \\

.select("id, monto, plazo\_meses, tasa\_anual, cuota\_mensual") \\

.eq("user\_id", user\_id) \\

.order("cuota\_mensual", desc=True) \\

.limit( 1 ) \\

.execute()

return response.data\[ 0 ] if response.data else None

```

\*\*Entregable 4 — Corrección del Router: advertir al consumidor del endpoint\*\*



Archivo: routers/prestamos.py



```

@router.get(

"/promedio-cuota/{user\_id}",

summary="Cuota promedio recalculada con TEM correcta",

description="""

Retorna el promedio de cuota mensual recalculado con TEM (Tasa Efectiva

Mensual).

IMPORTANTE: El campo cuota\_registrada refleja el valor almacenado

históricamente

con la fórmula TEA/12 (incorrecta). El campo cuota\_correcta es el valor real

calculado con TEM según normativa SBS.

El área de Riesgos debe usar cuota\_correcta para reportes ejecutivos.

"""

)

async def promedio\_cuota(user\_id: str):

return await controller.promedio\_cuota(user\_id)

```

```

@router.get(

"/cuota-mas-alta/{user\_id}",

summary="Cuota más alta recalculada con TEM correcta"

)

async def cuota\_mas\_alta(user\_id: str):

return await controller.cuota\_mas\_alta(user\_id)

```

\*\*Entregable 5 — Corrección del Controller: agregar contexto de integridad\*\*





Archivo: controllers/prestamo\_controller.py



```

async def promedio\_cuota(self, user\_id: str) -> dict:

data = service.calcular\_promedio\_cuota(user\_id)

return {

"success": True,

"data": data,

"nota\_integridad": (

"Los valores cuota\_registrada fueron calculados con fórmula TEA/12 "

"durante el período 01/2024-08/2024. Usar cuota\_correcta para reportes

"

"y decisiones de cartera."

)

}

```

```

async def cuota\_mas\_alta(self, user\_id: str) -> dict:

data = service.obtener\_cuota\_mas\_alta(user\_id)

if not data:

return {"success": False, "message": "Sin solicitudes registradas"}

return {

"success": True,

"data": data,

"nota\_integridad": (

"cuota\_registrada corresponde al período con fórmula incorrecta. "

"Usar cuota\_correcta para evaluación de capacidad de pago."

)

}

```

\*\*Entregable 6 — Script SQL de auditoría de daño en cartera\*\*



```

\-- IMPACTO COMPLETO DEL ERROR EN LA TABLA solicitudes\_prestamo

\-- Cuantifica cuánto están infladas las cuotas registradas vs las correctas

```

```

WITH recalculo AS (

SELECT

id,

user\_id,

monto,

plazo\_meses,

tasa\_anual,

cuota\_mensual AS

cuota\_registrada,

ROUND(

monto \* (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ) /

( 1 - POWER( 1 + (POWER( 1 + tasa\_anual/ 100 , 1.0/ 12 ) - 1 ), -plazo\_meses))

, 2 ) AS

cuota\_correcta,

estado,

created\_at

FROM solicitudes\_prestamo

WHERE created\_at >= NOW() - INTERVAL '8 months'

```



\#### )



\#### SELECT



```

\-- Impacto en promedios (lo que vio el dashboard)

ROUND(AVG(cuota\_registrada), 2 ) AS promedio\_cuota\_dashboard,

ROUND(AVG(cuota\_correcta), 2 ) AS promedio\_cuota\_real,

ROUND(AVG(cuota\_registrada - cuota\_correcta), 2 ) AS diferencia\_promedio,

ROUND((AVG(cuota\_registrada) / AVG(cuota\_correcta) - 1 ) \* 100 , 2 )

AS sobreestimacion\_pct,

```

```

\-- Impacto en máximos (la cuota más alta del dashboard)

ROUND(MAX(cuota\_registrada), 2 ) AS max\_cuota\_dashboard,

ROUND(MAX(cuota\_correcta), 2 ) AS max\_cuota\_real,

```

```

\-- Cantidad de registros afectados

COUNT(\*) AS total\_solicitudes\_afectadas,

COUNT(\*) FILTER (WHERE estado = 'pendiente') AS pendientes\_con\_cuota\_erronea,

COUNT(\*) FILTER (WHERE estado = 'aprobado') AS aprobados\_con\_cuota\_erronea

```

```

FROM recalculo;

```

\*\*Entregable 7 — Informe ejecutivo al directorio\*\*



El grupo redacta el informe que el Ing. Wardo Peyra y la Eco. Maira Cellalo presentarán al directorio. Debe



responder tres preguntas concretas sin usar términos técnicos:



1\. ¿Por qué el promedio de cuota del dashboard de la semana 18 era incorrecto?

2\. ¿Cuántos contratos pueden verse afectados y en qué sentido?

3\. ¿Qué debe hacer el directorio con la decisión de ampliar el límite de crédito?



\*\*Tabla de asignación de entregables por integrante\*\*



```

Integrante Rol en la exposición Entregable principal

```

```

Kuntur Explica la cadena causa-efecto Entregable 1 — tabla completa

```

```

Rimac Defiende la corrección del Service Entregable 2 — recálculo con TEM

```

```

Wayra Defiende la corrección del Repository Entregable 3 — nuevos métodos

```

```

Illary Defiende la corrección del Router Entregable 4 — documentación del endpoint

```

```

Sisa Defiende la corrección del Controller Entregable 5 — nota de integridad

```

```

Qori Ejecuta y explica el script SQL Entregable 6 — números reales

```

```

Tupac Presenta el informe al directorio Entregable 7 — lenguaje ejecutivo

```

\*\*Pregunta de defensa del Ing. Wardo Peyra:\*\*



```

"¿Por qué en la corrección del Service el método calcular\_promedio\_cuota() no lee cuota\_mensual

de la BD sino que pide monto, tasa\_anual y plazo\_meses para recalcular? ¿Qué principio de

arquitectura respalda esa decisión?"

```



\## EPÍLOGO — El viernes



El viernes a las 6 PM, los siete practicantes enviaron sus reportes al Ing. Wardo Peyra.



A las 8 PM recibieron su respuesta:



\_"Casos críticos 1 al 6: aprobados para presentación. Casos operativos 7 al 12: cinco aprobados, dos con\_



\_observaciones menores. El lunes a las 9 AM exponen ante Cumplimiento Normativo, el área comercial y —\_



\_atención — ante dos miembros del directorio que quieren entender qué pasó con el dashboard de la semana 18.\_



\_No es simulacro. Vengan preparados."\_



Hubo silencio en el grupo de WhatsApp por treinta segundos.



Illary escribió primero:



\_"¿El directorio va a estar ahí?"\_



El Ing. Wardo Peyra respondió directamente:



\_"Sí. La Eco. Maira Cellalo les explicó que fueron ustedes quienes detectaron que el dashboard tenía seis errores\_



\_simultáneos. Quieren conocerlos."\_



Tupac le escribió a Qori:



\_"¿Te diste cuenta que el error del simulador es exactamente lo que hace la gente del gota a gota pero al revés?\_



\_Ellos ocultan cuánto te cobran realmente. Nosotros mostrábamos una cuota más alta de la real sin darnos\_



\_cuenta."\_



Qori respondió después de un momento:



\_"Sí. Y los dos dañan al cliente. La diferencia es que nosotros lo podemos corregir."\_



Kuntur añadió:



\_"Lo peor no fue el error de la fórmula. Lo peor fue que seis errores pequeños, cada uno en su propia capa,\_



\_construyeron juntos una foto de la cartera que no existía. Y el directorio tomó una decisión de S/ 50,000 de límite\_



\_de crédito basada en esa foto."\_



La Eco. Maira Cellalo leyó el reporte final esa noche. Anotó al margen:



\_"Estos practicantes entendieron algo que muchos desarrolladores senior no entienden: el código financiero no es\_



\_solo código. Es un contrato con el cliente. Y cuando falla, no falla en el servidor. Falla en la vida de las personas."\_



\## REFERENCIA RÁPIDA — Arquitectura del proyecto



```

devappweb\_s2\_m5\_fastapi\_supabase/

│

├── routers/

│ └── prestamos.py CAPA 1: Define URLs y métodos HTTP

│ @router.post("/simular")

│ @router.get("/dashboard-riesgos/{user\_id}")

│

```



```

├── controllers/

│ └── prestamo\_controller.py CAPA 2: Coordina petición y respuesta

│ No calcula, no accede a BD

│ Nuevo: dashboard\_riesgos()

│

├── services/

│ └── prestamo\_service.py CAPA 3: Lógica de negocio y fórmulas

│ ← AQUÍ ESTABAN LOS ERRORES FINANCIEROS

│ calcular\_cuota() con TEM corregida

│ calcular\_promedio\_cuota() recalculado

│ calcular\_plazo\_promedio() con filtro estado

│

├── repositories/

│ └── prestamo\_repository.py CAPA 4: Único que conoce Supabase

│ INSERT, SELECT, DELETE

│ ← AQUÍ ESTABAN LOS ERRORES DE FILTRO

│ contar\_por\_estado() con user\_id

│ obtener\_total\_aprobado() con estado

│ obtener\_pendientes() con ORDER BY y LIMIT

│

├── models/

│ └── schemas.py SCHEMAS: Validación Pydantic

│ Campos, tipos, rangos

│ Error 422 automático si falla

│ Nuevo: DashboardRiesgosResponse

│

├── main.py Punto de entrada — configura FastAPI

└── .env Credenciales Supabase (no subir a Git)

```

```

Caso Tipo Capas afectadas Error principal

```

```

Crítico 1 Grupo Service Fórmula TEM incorrecta en calcular\_cuota()

```

```

Crítico 2 Grupo Service + Models ITF no calculado ni informado al cliente

```

```

Crítico 3 Grupo

```

```

Service + Repository +

Controller

```

```

Cuota no recalculada antes de guardar en BD

```

```

Crítico 4 Grupo

```

```

Service + Repository +

Models

```

```

Sin protección contra solicitudes duplicadas

```

```

Crítico 5 Grupo Models + Service + Router

```

```

Sin validación de rangos normativos del

tarifario

```

```

Crítico

6

```

```

Grupo

completo

```

```

Todas las capas

```

```

Seis errores combinados desinforman al

directorio

```

\_Fin de la historia. Inicio de los casos.\_



\_Sub Departamento de Desarrollo de Software Homebanking Ing. Wardo Peyra — Eco. Maira Cellalo\_







