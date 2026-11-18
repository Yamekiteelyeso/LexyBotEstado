#!/usr/bin/env python3
"""LexyBotEstado: presencia personalizada de Discord (sin token ni self-bot)."""

from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from pathlib import Path
from typing import Any

from pypresence import Presence


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = BASE_DIR / "config.json"
STOP = False


def request_stop(_signum: int, _frame: Any) -> None:
    global STOP
    STOP = True


def load_config(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(
            f"Falta {path.name}. Copia config.example.json a config.json "
            "y configura el client_id de tu aplicación Discord."
        ) from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("La configuración debe ser un objeto JSON.")

    client_id = str(data.get("client_id", "")).strip()
    if not (client_id.isascii() and client_id.isdecimal() and 15 <= len(client_id) <= 22):
        raise ValueError("client_id debe ser el Application ID numérico de Discord.")

    for field in ("game", "details", "state", "large_image", "large_text"):
        value = data.get(field, "")
        if not isinstance(value, str):
            raise ValueError(f"{field} debe ser texto.")
        if len(value) > 128:
            raise ValueError(f"{field} debe tener 128 caracteres o menos.")

    for field in ("elapsed_hours", "refresh_seconds", "retry_seconds"):
        value = data.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{field} debe ser un entero no negativo.")

    if data["refresh_seconds"] < 15:
        raise ValueError("refresh_seconds debe ser al menos 15.")
    if data["retry_seconds"] < 5:
        raise ValueError("retry_seconds debe ser al menos 5.")

    return data


def make_activity(config: dict[str, Any], started_at: int) -> dict[str, Any]:
    activity: dict[str, Any] = {
        "name": config.get("game") or "Grand Theft Auto VI",
        "details": config.get("details") or "Jugando en PlayStation 5",
        "state": config.get("state") or "PS5",
        "start": started_at,
    }
    if config.get("large_image"):
        activity["large_image"] = config["large_image"]
        activity["large_text"] = config.get("large_text") or config["game"]
    return activity


def run(config: dict[str, Any]) -> None:
    global STOP
    client_id = str(config["client_id"]).strip()
    started_at = int(time.time()) - config["elapsed_hours"] * 3600
    activity = make_activity(config, started_at)
    retry_seconds = config["retry_seconds"]
    refresh_seconds = config["refresh_seconds"]

    signal.signal(signal.SIGINT, request_stop)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, request_stop)

    print("LexyBotEstado iniciado. Discord de escritorio debe estar abierto.")
    print(f"Actividad: {activity['name']} | {activity['details']}")
    print("Pulsa Ctrl+C para detener.")

    while not STOP:
        rpc: Presence | None = None
        try:
            rpc = Presence(client_id)
            rpc.connect()
            rpc.update(**activity)
            print("Presencia activada en Discord.")
            next_refresh = time.monotonic() + refresh_seconds
            while not STOP:
                time.sleep(1)
                if STOP:
                    break
                # Actualiza en intervalos estables y conserva el contador original.
                if time.monotonic() >= next_refresh:
                    rpc.update(**activity)
                    next_refresh = time.monotonic() + refresh_seconds
        except Exception as exc:
            if not STOP:
                print(f"No se pudo conectar o actualizar Discord: {exc}", file=sys.stderr)
                print(f"Reintentando en {retry_seconds} segundos...")
                for _ in range(retry_seconds):
                    if STOP:
                        break
                    time.sleep(1)
        finally:
            if rpc is not None:
                try:
                    rpc.clear()
                except Exception:
                    pass
                try:
                    rpc.close()
                except Exception:
                    pass

    print("LexyBotEstado detenido.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rich Presence de GTA VI en Discord.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Ruta de configuración JSON (por defecto: config.json)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verifica la configuración sin conectar a Discord.",
    )
    args = parser.parse_args()
    try:
        config = load_config(args.config)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if args.check:
        print(f"Configuración válida: {config.get('game')} en {config.get('details')}.")
        return 0
    run(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
