import subprocess
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from sqlalchemy.engine import make_url


def respaldo_desde_url(db_url: Optional[str] = None, archivo_salida: Optional[str] = None) -> str:
    """Crea un respaldo completo (mysqldump) de la base indicada en una URL SQLAlchemy.

    - Si `db_url` es None, intenta leer `DB_URL` desde la variable de entorno.
    - Devuelve la ruta del archivo de respaldo creado.

    Requiere que `mysqldump` esté en el PATH y que la URL sea del tipo mysql+pymysql://user:pass@host/dbname
    """
    # Priorizar argumento, luego variable de entorno
    db_url = db_url or os.environ.get("DB_URL")
    if not db_url:
        raise ValueError("No se encontró URL de base de datos. Pasa db_url o define DB_URL en el entorno.")

    url = make_url(db_url)
    if url.drivername.startswith("mysql") is False:
        raise ValueError("Solo se soportan URLs MySQL para este respaldo.")

    usuario = url.username or "root"
    password = url.password or ""
    host = url.host or "127.0.0.1"
    puerto = url.port
    nombre_bd = url.database

    if not nombre_bd:
        raise ValueError("No se pudo determinar el nombre de la base de datos desde la URL.")

    # Nombre de archivo por timestamp si no se especifica
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_salida = archivo_salida or f"backup_{nombre_bd}_{timestamp}.sql"

    # Preparar comando mysqldump
    # localizar mysqldump en PATH o usar MYSQLDUMP_PATH
    def _find_executable(name: str, env_var: Optional[str] = None) -> str:
        if env_var and os.environ.get(env_var):
            candidate = os.environ.get(env_var)
            if Path(candidate).exists():
                return candidate
        found = shutil.which(name)
        if found:
            return found
        raise FileNotFoundError(
            f"El ejecutable '{name}' no se encontró en el PATH. Instala el cliente de MySQL o añade su ruta a PATH,\n"
            f"o define la variable de entorno '{env_var or name.upper() + "_PATH"}'."
        )

    mysqldump_path = _find_executable("mysqldump", "MYSQLDUMP_PATH")
    comando = [mysqldump_path, "-u", usuario]
    if host:
        comando += ["-h", host]
    if puerto:
        comando += ["-P", str(puerto)]
    # Incluir la base de datos al final
    comando.append(nombre_bd)

    env = os.environ.copy()
    # Evitar dejar contraseña en la línea de comandos: usar MYSQL_PWD
    if password:
        env["MYSQL_PWD"] = password

    salida_path = Path(archivo_salida)
    try:
        with salida_path.open("wb") as f:
            subprocess.run(comando, env=env, stdout=f, check=True)
        return str(salida_path.resolve())
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error al ejecutar mysqldump: {e}") from e


def restaurar_mysql(nombre_bd_destino: str, archivo_sql: str, db_user: Optional[str] = None, db_pass: Optional[str] = None, db_host: Optional[str] = None, db_port: Optional[int] = None):
    """Restaura un archivo .sql a la base indicada usando cliente `mysql`.

    Esta función no crea la base; debe existir previamente.
    """
    archivo = Path(archivo_sql)
    if not archivo.exists():
        raise FileNotFoundError("El archivo de respaldo no existe: " + archivo_sql)

    # localizar cliente mysql
    mysql_path = _find_executable("mysql", "MYSQL_CLIENT_PATH") # pyright: ignore[reportUndefinedVariable]
    comando = [mysql_path]
    if db_user:
        comando += ["-u", db_user]
    if db_host:
        comando += ["-h", db_host]
    if db_port:
        comando += ["-P", str(db_port)]
    comando.append(nombre_bd_destino)

    env = os.environ.copy()
    if db_pass:
        env["MYSQL_PWD"] = db_pass

    with archivo.open("rb") as f:
        try:
            subprocess.run(comando, env=env, stdin=f, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error al restaurar la base: {e}") from e

# Nota: no ejecutar nada al importar este módulo. Usar las funciones desde código o CLI.