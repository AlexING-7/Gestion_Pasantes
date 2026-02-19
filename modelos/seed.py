import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import logging
from herramientas.conversiones import cifrar


# 1. Importa la configuración de tu BD
# Ajusta los nombres de archivo según tu proyecto (ej. database.py, models.py)
from modelos.modulo import session, engine, Base,User, Student,Enterprise,Tutor_Academico,Tutor_Empresarial

# 2. Importa tus Factories
from factories import UserFactory, StudentFactory,EnterpriseFactory,TutorAcademicoFactory,TutorEmpresarialFactory,PasantiaFactory,ConfiguracionFactory

# Configuración básica de logs para ver qué pasa en la consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SEEDER")

def reiniciar_base_de_datos():
    """
    ¡CUIDADO! Esto borra todas las tablas y las crea de nuevo.
    Útil para desarrollo, peligroso en producción.
    """
    logger.info("Eliminando tablas existentes...")
    Base.metadata.drop_all(engine)
    
    logger.info("Creando tablas limpias...")
    Base.metadata.create_all(engine)

def crear_usuarios_sistema():
    """Crea los usuarios fijos para el staff."""
    logger.info("Creando usuarios administrativos...")

    # Usuario Administrador (Para que puedas entrar siempre)
    UserFactory(
        username="admin",
        password=cifrar("123"),  # En producción recuerda hashear esto
        email="admin@psm.edu.ve",
        rol="Administrador"
    )

    # Usuario Secretaria
    UserFactory(
        username="coord",
        password=cifrar("123"),
        email="control_estudios@psm.edu.ve",
        rol="Coordinador"
    )
    
    ConfiguracionFactory(
        clave="autoridad_firmante_1",
        valor="Ing. Alex Rodriguez"   
    )
    
    ConfiguracionFactory(
        clave="ciudad",
        valor="Barinas"   
    )
    ConfiguracionFactory(
        clave="escuela",
        valor="instituto politécnico “santiago mariño” extensión barinas"   
    )
    
    ConfiguracionFactory(
        clave="cargo_autoridad_firmante_1",
        valor="Jefe del departamento de pasantias"   
    )
    
    ConfiguracionFactory(
        clave="autoridad_firmante_2",
        valor="Lcda Febe Montilva"   
    )
    
    ConfiguracionFactory(
        clave="cargo_autoridad_firmante_2",
        valor="Coordinadora de la Extensión"   
    )
    
    ConfiguracionFactory(
        clave="lapso_actual",
        valor="2025-2"   
    )
    
    ConfiguracionFactory(
        clave="inicio_lapso_actual",
        valor="22/09/2025"   
    )
    
    ConfiguracionFactory(
        clave="final_lapso_actual",
        valor="02/02/2026"   
    )
    
    ConfiguracionFactory(
        clave="final_lapso_actual",
        valor="02/02/2026"   
    )
    
    ConfiguracionFactory(
        clave="carreras",
        valor='{"carreras":["Arquitectura","Ingeniería Civil","Ingeniería Eléctrica","Ingeniería Electrónica","Ingeniería Industrial","Ingeniería Sistemas","Ingeniería Diseño Industrial"]}'   
    )
    
    ConfiguracionFactory(
        clave="formatos",
        valor='''{
                    "Carta de Postulación a Pasantía" : "formatos/1. CARTA SOLICITUD DE PASANTIA.docx",
                    "Carta de Aceptación de Pasantía" : "formatos/2.CARTA ACEPTACION DEL PASANTE.docx",
                    "Acta de Inicio" : "formatos/3.ACTA DE INICIO.docx",
                    "Acta de Inicio de Ejecución de Pasantía" : "formatos/4.ACTA DE INICIO DE EJECUCIÓN DE PASANTÍA.docx",
                    "Contrado del Pasante":"formatos/5.CONTRATO DEL PASANTE.docx",
                    "Inscripción de Pasantía":"formatos/6. INSCRIPCION DE PASANTIA.docx",
                    "Cronograma de Actividades":"formatos/8.CRONOGRAMA DE ACTIVIDADES.docx",
                    "Plan de Trabajo":"formatos/9.PLAN DE TRABAJO.docx",
                    "Acta de Aprobacion del Informe de Pasantia":"formatos/10. ACTA DE APROBACION DEL INFORME DE PASANTÍA.docx",
                    "Evaluacion de la Exposición":"formatos/11. EVALUACIÓN DE LA EXPOSICIÓN.docx",
                    "Supervisión del Pasante":"formatos/12. SUPERVISION DEL PASANTE.docx",
                    "Autorización Presentación del Informe":"formatos/14. AUTORIZACION PRESENTACION DEL INFORME.docx",
                    "Evaluación":"formatos/17. EVALUACION.docx",
                    "Evaluación Final":"formatos/18. EVALUACION FINAL.docx",
                    "Carta de Extensión de Pasantía":"formatos/15.CARTA DE EXTENSIÓN DE PASANTIAS.docx"
                }'''   
    )
    
    

def crear_estudiantes_prueba():
    """Crea estudiantes aleatorios y casos específicos."""
    logger.info("Generando estudiantes...")

    StudentFactory(
        cedula=12345678,
        primer_nombre="Prueba",
        primer_apellido="Sistema",
        carrera="Ingeniería de Sistemas",
        semestre=9,
        telefono="04121234567",
        email="prueba@estudiante.com"
    )

    StudentFactory.create_batch(200)

    StudentFactory.create_batch(20, carrera="Arquitectura")
def crear_empresas_prueba():
    logger.info("Generando Empresas...")
    EnterpriseFactory.create_batch(5)
def crear_tutoresA_prueba():
    logger.info("Generando Tutores Academicos...")
    TutorAcademicoFactory.create_batch(20)
    
def crear_tutoresE_prueba():
    logger.info("Generando Tutores Empresariales...")
    TutorEmpresarialFactory.create_batch(80)

def crear_pasantias():
    logger.info("Generando Tutores Empresariales...")    
    # Usar el método de clase `create_batch` pasando el trait `finalizada=True`
    PasantiaFactory.create_batch(40, finalizada=True)
    PasantiaFactory.create_batch(10, nueva=True)
    PasantiaFactory.create_batch(5, activa=True)
def run_seeds():
    try:

        reiniciar_base_de_datos()

        # Paso 2: Poblar
        crear_usuarios_sistema()
        crear_empresas_prueba()
        crear_tutoresA_prueba()
        crear_pasantias()     

        # Paso 3: Confirmar cambios (Aunque FactoryBoy con 'commit' ya lo hace, aseguramos)
        session.commit()
        
        logger.info("✅ ¡Base de datos poblada exitosamente!")
        logger.info(f"Total Usuarios: {session.query(User).count()}")
        logger.info(f"Total Estudiantes: {session.query(Student).count()}")
        logger.info(f"Total Empresas: {session.query(Enterprise).count()}")
        logger.info(f"Total Tutores Academicos: {session.query(Tutor_Academico).count()}")
        logger.info(f"Total Tutores Empresariales: {session.query(Tutor_Empresarial).count()}")

    except Exception as e:
        session.rollback()
        logger.error(f"❌ Error durante el seeding: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    run_seeds()