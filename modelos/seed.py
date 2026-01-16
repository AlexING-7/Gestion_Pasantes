import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import logging

# 1. Importa la configuración de tu BD
# Ajusta los nombres de archivo según tu proyecto (ej. database.py, models.py)
from modelos.modulo import session, engine, Base,User, Student,Enterprise,Tutor_Academico,Tutor_Empresarial

# 2. Importa tus Factories
from factories import UserFactory, StudentFactory,EnterpriseFactory,TutorAcademicoFactory,TutorEmpresarialFactory,PasantiaFactory

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
        password="123",  # En producción recuerda hashear esto
        email="admin@psm.edu.ve",
        rol="Administrador"
    )

    # Usuario Secretaria
    UserFactory(
        username="secretaria",
        password="123",
        email="control_estudios@psm.edu.ve",
        rol="Secretaria"
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
    EnterpriseFactory.create_batch(100)
def crear_tutoresA_prueba():
    logger.info("Generando Tutores Academicos...")
    TutorAcademicoFactory.create_batch(50)
    
def crear_tutoresE_prueba():
    logger.info("Generando Tutores Empresariales...")
    TutorEmpresarialFactory.create_batch(80)

def crear_pasantias():
    logger.info("Generando Tutores Empresariales...")    
    PasantiaFactory.create_batch(20)
def run_seeds():
    try:

        reiniciar_base_de_datos()

        # Paso 2: Poblar
        crear_usuarios_sistema()
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