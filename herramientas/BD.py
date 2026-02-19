import subprocess
import os

# Configuración Global
DB_USER = "tu_usuario"
DB_PASS = "tu_password"  # Ten cuidado con las contraseñas en texto plano
DB_HOST = "localhost"

def respaldar_mysql(nombre_bd, archivo_salida="backup.sql"):
    """Genera un archivo .sql con toda la estructura y datos."""
    # Seteamos la contraseña en el entorno para que mysqldump no la pida por consola
    env = os.environ.copy()
    env["MYSQL_PWD"] = DB_PASS
    
    comando = [
        "mysqldump",
        "-u", DB_USER,
        "-h", DB_HOST,
        nombre_bd
    ]
    
    try:
        with open(archivo_salida, "w") as f:
            subprocess.run(comando, env=env, stdout=f, check=True)
        print(f"✅ Respaldo exitoso: {archivo_salida}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al respaldar: {e}")

def restaurar_mysql(nombre_bd_destino, archivo_sql):
    """Lee un archivo .sql y lo vuelca en una base de datos existente."""
    if not os.path.exists(archivo_sql):
        print("Error: El archivo de respaldo no existe.")
        return

    env = os.environ.copy()
    env["MYSQL_PWD"] = DB_PASS

    comando = [
        "mysql",
        "-u", DB_USER,
        "-h", DB_HOST,
        nombre_bd_destino
    ]

    try:
        with open(archivo_sql, "r") as f:
            subprocess.run(comando, env=env, stdin=f, check=True)
        print(f"✅ Restauración exitosa en '{nombre_bd_destino}'")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al restaurar: {e}")

# --- EJEMPLO DE USO ---
# 1. Creamos el backup de la base 'produccion'
respaldar_mysql("mi_base_produccion", "respaldo_febrero.sql")

# 2. Restauramos en una base llamada 'clon_pruebas' 
# (Asegúrate de que 'clon_pruebas' ya esté creada en MySQL)
restaurar_mysql("clon_pruebas", "respaldo_febrero.sql")