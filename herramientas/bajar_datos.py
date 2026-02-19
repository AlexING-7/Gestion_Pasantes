import mysql.connector
import psycopg2
import datetime

# Configuración
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gestion_pasantes'
}

# Recuerda quitar los corchetes [] y usar tu ID de proyecto real
SUPABASE_URL = "postgresql://postgres.wafpccynffvtmiwyhmro:alex304094777@aws-1-us-east-1.pooler.supabase.com:6543/postgres"

def obtener_ultima_fecha_local(cursor_mysql, tabla):
    """Obtiene la fecha del último registro en el MySQL local."""
    try:
        cursor_mysql.execute(f"SELECT MAX(updated_at) FROM {tabla}")
        res = cursor_mysql.fetchone()[0]
        return res if res else datetime.datetime(1970, 1, 1)
    except:
        return datetime.datetime(1970, 1, 1)

def sincronizar_hacia_local(tabla, columnas):
    conn_mysql = None
    conn_supa = None
    try:
        # 1. Conectar a MySQL para ver qué tenemos
        conn_mysql = mysql.connector.connect(**MYSQL_CONFIG)
        cursor_mysql = conn_mysql.cursor()
        ultima_fecha = obtener_ultima_fecha_local(cursor_mysql, tabla)

        # 2. Conectar a Supabase y traer lo nuevo
        conn_supa = psycopg2.connect(SUPABASE_URL)
        cursor_supa = conn_supa.cursor()
        
        query_select = f"SELECT {', '.join(columnas)} FROM {tabla} WHERE updated_at > %s"
        cursor_supa.execute(query_select, (ultima_fecha,))
        datos = cursor_supa.fetchall()

        if not datos:
            print(f"--- {tabla}: Local ya está actualizado.")
            return

        # 3. Preparar el UPSERT para MySQL
        placeholders = ", ".join(["%s"] * len(columnas))
        # Generar: columna1=VALUES(columna1), columna2=VALUES(columna2)...
        update_clause = ", ".join([f"{col}=VALUES({col})" for col in columnas if col != 'id'])
        
        query_mysql = f"""
            INSERT INTO {tabla} ({', '.join(columnas)})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {update_clause}
        """

        # 4. Insertar en MySQL
        cursor_mysql.executemany(query_mysql, datos)
        conn_mysql.commit()
        print(f"✅ {tabla}: {cursor_mysql.rowcount} registros bajados a local.")

    except Exception as e:
        print(f"❌ Error en {tabla}: {e}")
    finally:
        if conn_mysql: conn_mysql.close()
        if conn_supa: conn_supa.close()

if __name__ == "__main__":
    # Asegúrate de que los nombres de columnas coincidan con tu MySQL
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
    print(f"📥 Bajando cambios desde Supabase ({datetime.datetime.now()})")
    for tabla, cols in tablas_config.items():
        sincronizar_hacia_local(tabla, cols)
    print("🏁 Sincronización local terminada.")