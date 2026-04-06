from __future__ import annotations

import json
import logging

import azure.functions as func

from .storage import append_event
from .validation import parse_sensor_payload

logger = logging.getLogger(__name__)


def handle_put_sensor(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("--- Ingesta: recibida petición PUT /api/sensors ---")
    try:
        body = req.get_json()
    except ValueError:
        logger.info("Ingesta: rechazo — cuerpo no es JSON válido.")
        return func.HttpResponse(
            json.dumps({"error": "Cuerpo debe ser JSON"}),
            status_code=400,
            mimetype="application/json",
        )
    if not isinstance(body, dict):
        logger.info("Ingesta: rechazo — JSON raíz debe ser objeto.")
        return func.HttpResponse(
            json.dumps({"error": "JSON debe ser un objeto"}),
            status_code=400,
            mimetype="application/json",
        )
    try:
        event = parse_sensor_payload(body)
    except ValueError as e:
        logger.info("Ingesta: validación fallida — %s", e)
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json",
        )
    try:
        blob_path = append_event(event)
    except Exception as e:
        logger.info("Ingesta: error al escribir en storage — %s", e, exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": "Error de almacenamiento", "detail": str(e)}),
            status_code=500,
            mimetype="application/json",
        )
    logger.info(
        "Ingesta: flujo completado — evento persistido; blob relativo=%s",
        blob_path,
    )
    return func.HttpResponse(
        json.dumps(
            {
                "status": "ok",
                "machine_id": event.machine_id,
                "stored_path": blob_path,
            },
            ensure_ascii=False,
        ),
        status_code=200,
        mimetype="application/json",
    )
