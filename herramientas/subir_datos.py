import mysql.connector
import psycopg2
from psycopg2.extras import execute_values
import datetime

# Configuración
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gestion_pasantes'
}

# Usa la cadena de conexión de "Transaction Pooler" de Supabase (puerto 6543)
# para manejar mejor el límite de 60 conexiones de la cuenta gratuita.
SUPABASE_URL = "postgresql://postgres.wafpccynffvtmiwyhmro:alex304094777@aws-1-us-east-1.pooler.supabase.com:6543/postgres"

def obtener_ultima_sincronizacion(cursor_supa, tabla):
    """Obtiene la fecha del último registro actualizado en Supabase."""
    try:
        cursor_supa.execute(f"SELECT MAX(updated_at) FROM {tabla}")
        res = cursor_supa.fetchone()[0]
        return res if res else datetime.datetime(1970, 1, 1)
    except:
        return datetime.datetime(1970, 1, 1)

def sincronizar_tabla_optimizada(tabla, columnas):
    conn_mysql = None
    conn_supa = None
    try:
        # 1. Conectar a Supabase primero para ver qué datos ya tiene
        conn_supa = psycopg2.connect(SUPABASE_URL)
        cursor_supa = conn_supa.cursor()
        ultima_fecha = obtener_ultima_sincronizacion(cursor_supa, tabla)

        # 2. Conectar a MySQL y traer solo lo NUEVO o MODIFICADO
        conn_mysql = mysql.connector.connect(**MYSQL_CONFIG)
        cursor_mysql = conn_mysql.cursor()
        
        query_select = f"""
            SELECT {', '.join(columnas)} FROM {tabla} 
            WHERE updated_at > %s
        """
        cursor_mysql.execute(query_select, (ultima_fecha,))
        datos = cursor_mysql.fetchall()

        if not datos:
            print(f"--- {tabla}: Todo está al día.")
            return

        # 3. UPSERT en bloques (Batching) para no saturar la conexión gratuita
        # Procesamos de a 100 registros por vez
        batch_size = 100
        update_set = ", ".join([f"{col} = EXCLUDED.{col}" for col in columnas if col != 'id'])
        
        query_upsert = f"""
            INSERT INTO {tabla} ({', '.join(columnas)})
            VALUES %s
            ON CONFLICT (id) 
            DO UPDATE SET {update_set};
        """

        for i in range(0, len(datos), batch_size):
            batch = datos[i:i + batch_size]
            execute_values(cursor_supa, query_upsert, batch)
            conn_supa.commit() # Confirmamos por bloques
            print(f"✅ {tabla}: Sincronizados {len(batch)} registros...")

    except Exception as e:
        print(f"❌ Error en {tabla}: {e}")
    finally:
        if conn_mysql: conn_mysql.close()
        if conn_supa: conn_supa.close()

# --- Ejecución principal ---
if __name__ == "__main__":
    tablas_config = {
    "students": [
        "id", "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido",
        "sexo", "cedula", "telefono", "email", "foto", "direccion", "fecha_de_nacimiento", "updated_at"
    ],
    "enterprises": [
        "id", "rif", "razon_social", "direccion", "email", "telefono", "rubro", "updated_at"
    ],
    "tutores_academicos": [
        "id", "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido",
        "sexo", "foto", "cedula", "email", "fecha_de_nacimiento", "telefono", "especialidad", "updated_at"
    ],
    "tutores_empresariales": [
        "id", "id_empresa", "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido",
        "sexo", "foto", "cedula", "email", "fecha_de_nacimiento", "telefono", "cargo", "updated_at"
    ],
    "pasantias": [
        "id", "student_id", "empresa_id", "tutor_academico_id", "tutor_empresarial_id",
        "carrera", "semestre", "lapso_academico", "inicio_pasantias", "final_pasantias",
        "departamento", "estado", "trabajo_asignado", "titulo_de_informe", "plan_de_trabajo",
        "sede", "direccion", "jefe_de_carta", "cargo_jefe_de_carta", "updated_at"
    ],
    "documentos_adjuntos": [
        "id", "pasantia_id", "tipo_de_documento", "ruta", "fecha_subida", "estado", "updated_at"
    ],
    "evaluaciones": [
        "id", "pasantia_id", "nota_tutor_aca", "nota_tutor_emp", "exposicion", 
        "taller_induccion", "total", "updated_at"
    ],
    "configuraciones": [
        "id", "clave", "valor", "updated_at"
    ]
    }

    print(f"🚀 Iniciando sincronización incremental ({datetime.datetime.now()})")
    for tabla, cols in tablas_config.items():
        sincronizar_tabla_optimizada(tabla, cols)
    print("🏁 Proceso terminado.")