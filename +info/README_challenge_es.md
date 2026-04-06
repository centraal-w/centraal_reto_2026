# Predictive Maintenance Challenge

## Introducción

Esta solución implementa un escenario simplificado de mantenimiento
predictivo para equipos industriales.

El objetivo es construir un sistema capaz de: - recibir datos de
sensores, - almacenarlos correctamente, - analizar comportamiento
reciente, - estimar probabilidad de fallo en las próximas 24 horas.

La arquitectura es simple, pero refleja patrones reales usados en
entornos cloud.

------------------------------------------------------------------------

## Arquitectura Explicada (Paso a Paso)

La solución se compone de tres bloques principales:

### 1. Ingesta de datos (HTTP API)

Endpoint:

PUT /api/sensors

Recibe eventos individuales de sensores.

Cada evento: - pertenece a una máquina, - representa una variable, -
tiene un timestamp.

👉 Hint: No estás guardando estados, estás guardando **eventos
históricos**.

------------------------------------------------------------------------

### 2. Almacenamiento (Data Lake lógico)

Los eventos se almacenan en Azure Blob Storage (Azurite en local).

Estructura:

raw/machine_id=.../year=.../month=.../day=.../events.ndjson

Formato: - NDJSON (una línea = un evento) - escritura incremental

👉 Hints: - No necesitas leer todo el dataset para escribir. - Piensa en
"append" en lugar de "overwrite". - La estructura de carpetas es clave
para poder consultar luego.

------------------------------------------------------------------------

### 3. Predicción (Lectura + Cálculo)

Endpoints:

GET /api/machines/{machine_id}/prediction\
GET /api/predictions

Qué hacen: 1. Leen eventos de las últimas 24h. 2. Agrupan por variable.
3. Calculan valores simples (último, promedio, máximo). 4. Comparan con
valores esperados. 5. Generan un score. 6. Aplican una función sigmoide.


------------------------------------------------------------------------

## Modelo de Datos

``` json
{
  "machine_id": "PUMP-1001",
  "timestamp": "2026-04-06T10:15:00Z",
  "variable": "temperature_c",
  "value": 78.4
}
```

Variables esperadas:

-   vibration_mm_s
-   temperature_c
-   current_a
-   pressure_bar
-   load_pct

------------------------------------------------------------------------

## APIs

PUT /api/sensors\
GET /api/machines/{machine_id}/prediction\
GET /api/predictions

------------------------------------------------------------------------

## Ejecución Local (Guía General)

Para ejecutar este proyecto necesitas:

-   Python
-   Azure Functions Core Tools
-   Azurite

Flujo general:

1.  Levantar Azurite.
2.  Configurar connection string.
3.  Ejecutar Azure Functions.
4.  Probar endpoints.

👉 Hints:

-   Si ves errores de conexión, probablemente sea el connection string.
-   Azurite simula Azure Storage localmente.
-   Puedes usar Storage Explorer para inspeccionar archivos.
-   Si no sabes cómo arrancar Functions, busca "Azure Functions run
    local python".

------------------------------------------------------------------------

## Documentación útil

-   Azure Functions local:
    https://learn.microsoft.com/azure/azure-functions/functions-run-local

-   Azurite:
    https://learn.microsoft.com/azure/storage/common/storage-use-azurite

------------------------------------------------------------------------

## Qué deberías observar al final

-   Archivos NDJSON creciendo en storage.
-   Datos organizados por máquina y fecha.
-   Endpoints respondiendo con JSON.
-   Probabilidades coherentes (no aleatorias).

👉 Hint final: Si algo no cuadra, imprime logs. Este reto es más de
**entender el flujo** que de escribir mucho código.
