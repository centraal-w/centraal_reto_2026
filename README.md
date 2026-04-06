# Predictive Maintenance Platform

## Descripción General

Esta solución implementa una plataforma de mantenimiento predictivo
orientada a equipos industriales, basada en la ingesta de telemetría
operativa y el cálculo de probabilidad de fallo en una ventana de 24
horas.

El sistema está construido bajo un enfoque serverless, utilizando Azure
Functions para la exposición de APIs y Azure Blob Storage como base de
persistencia, organizado bajo un modelo de data lake lógico.

## Capacidades

-   Ingesta de eventos de sensores en tiempo casi real.
-   Persistencia de eventos en una zona raw.
-   Procesamiento bajo demanda de datos históricos.
-   Cálculo de probabilidad de fallo basada en scoring.
-   Exposición de predicciones mediante APIs REST.

------------------------------------------------------------------------

## Arquitectura

-   Azure Functions (HTTP) para APIs.
-   Blob Storage como data lake lógico.
-   Procesamiento en tiempo de consulta.

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

------------------------------------------------------------------------

## Data Lake Lógico

raw/machine_id=PUMP-1001/year=2026/month=04/day=06/events.ndjson

Formato: NDJSON (append-only)

------------------------------------------------------------------------

## Lógica de Predicción

failure_probability_24h = sigmoid(weighted_score)

------------------------------------------------------------------------

## APIs

PUT /api/sensors
GET /api/machines/{machine_id}/prediction
GET /api/predictions

------------------------------------------------------------------------

## Ejecución Local

https://learn.microsoft.com/azure/azure-functions/functions-run-local\
https://learn.microsoft.com/azure/storage/common/storage-use-azurite
