from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from .models import SensorEvent

logger = logging.getLogger(__name__)

ALLOWED_VARIABLES = frozenset(
    {
        "vibration_mm_s",
        "temperature_c",
        "current_a",
        "pressure_bar",
        "load_pct",
    }
)


def parse_sensor_payload(body: dict[str, Any]) -> SensorEvent:
    logger.info("Validando payload de sensor: comprobando campos obligatorios.")
    missing = [k for k in ("machine_id", "timestamp", "variable", "value") if k not in body]
    if missing:
        logger.info("Validación fallida: faltan campos %s.", missing)
        raise ValueError(f"Campos requeridos faltantes: {', '.join(missing)}")

    machine_id = str(body["machine_id"]).strip()
    if not machine_id:
        logger.info("Validación fallida: machine_id vacío.")
        raise ValueError("machine_id no puede estar vacío")

    variable = str(body["variable"]).strip()
    if variable not in ALLOWED_VARIABLES:
        logger.info(
            "Validación fallida: variable '%s' no permitida; permitidas: %s.",
            variable,
            sorted(ALLOWED_VARIABLES),
        )
        raise ValueError(f"variable debe ser una de: {', '.join(sorted(ALLOWED_VARIABLES))}")

    try:
        value = float(body["value"])
    except (TypeError, ValueError) as e:
        logger.info("Validación fallida: value no es numérico.")
        raise ValueError("value debe ser numérico") from e

    ts_raw = body["timestamp"]
    if isinstance(ts_raw, datetime):
        ts = ts_raw if ts_raw.tzinfo else ts_raw.replace(tzinfo=timezone.utc)
    else:
        s = str(ts_raw).strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        try:
            ts = datetime.fromisoformat(s)
        except ValueError as e:
            logger.info("Validación fallida: timestamp ISO8601 inválido.")
            raise ValueError("timestamp debe ser ISO8601 (ej. 2026-04-06T10:15:00Z)") from e
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

    ts = ts.astimezone(timezone.utc)
    logger.info(
        "Validación OK: machine_id=%s variable=%s value=%s ts_utc=%s",
        machine_id,
        variable,
        value,
        ts.isoformat(),
    )
    return SensorEvent(machine_id=machine_id, timestamp=ts, variable=variable, value=value)
