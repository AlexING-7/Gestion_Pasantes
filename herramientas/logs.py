import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import json
from modelos.modulo import SistemaLog
import socket
from datetime import date, datetime


def _json_default(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    raise TypeError(f"Type {type(o)} not serializable")

def registrar_log(
    session,
    usuario: str,
    accion: str,
    tabla_afectada: str | None = None,
    id_registro_afectado: int | None = None,
    valores_anteriores: dict | None = None,
    valores_nuevos: dict | None = None,
    mensaje: str | None = None,
    ip_maquina: str | None = None
):
    
    if ip_maquina is None:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # no hace conexión real a Internet, solo resuelve la IP local usada
                s.connect(("8.8.8.8", 80))
                ip_maquina = s.getsockname()[0]
            except Exception:
                ip_maquina = "127.0.0.1"
            finally:
                try:
                    s.close()
                except Exception:
                    pass
    def _sanitize(obj):
        if obj is None:
            return None
        # Convertir objetos no JSON-serializables (p. ej. date/datetime) a strings
        return json.loads(json.dumps(obj, ensure_ascii=False, default=_json_default))

    log = SistemaLog(
        usuario=usuario,
        accion=accion,
        tabla_afectada=tabla_afectada,
        id_registro_afectado=id_registro_afectado,
        valores_anteriores=_sanitize(valores_anteriores),
        valores_nuevos=_sanitize(valores_nuevos),
        mensaje=mensaje,
        ip_maquina=ip_maquina,
    )

    session.add(log)
    session.commit()