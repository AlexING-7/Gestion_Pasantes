import factory
from datetime import date, timedelta
from modelos.modulo import session,User,Student,Enterprise,Tutor_Academico,Tutor_Empresarial,Pasantia

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model=User
        sqlalchemy_session = session 
        sqlalchemy_session_persistence = 'commit'
    id = factory.Sequence(lambda n: n + 1)
    username = factory.Faker('name', locale='es_ES')
    password = factory.Faker('password', length=12)
    email = factory.Sequence(lambda n: f"user{n}@santiagomarino.edu.ve")
    rol = factory.Faker('random_element', elements=['Administrador', 'Coordinador'])
    
class StudentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Student
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    # 1. NOMBRES: Usamos locale='es_ES' para nombres hispanos
    primer_nombre = factory.Faker('first_name', locale='es_ES')

    # 2. CAMPOS OPCIONALES (Nullable): 
    # factory.Maybe decide si pone un valor o deja None (50% de probabilidad)
    segundo_nombre = factory.Maybe(
        factory.Faker('boolean', chance_of_getting_true=80),
        yes_declaration=factory.Faker('first_name', locale='es_ES'),
        no_declaration=None
    )

    primer_apellido = factory.Faker('last_name', locale='es_ES')
    
    segundo_apellido = factory.Maybe(
        factory.Faker('boolean', chance_of_getting_true=80),
        yes_declaration=factory.Faker('last_name', locale='es_ES'),
        no_declaration=None
    )

    # 3. SEXO
    sexo = factory.Faker('random_element', elements=['Masculino', 'Femenino'])

    # 4. CÉDULA (Unique):
    # Iniciamos en 20 millones para que parezcan cédulas reales y usamos Sequence para no repetir
    cedula = factory.Sequence(lambda n: 20000000 + n)

    # 5. TELÉFONO (Unique String 11):
    # Generamos formato 0412xxxxxxx usando la secuencia 'n' para garantizar unicidad
    # {n:07d} rellena con ceros hasta tener 7 dígitos (ej: 0000001, 0000002)
    telefono = factory.Sequence(lambda n: f"0412{n:07d}")

    # 6. EMAIL (Unique):
    email = factory.Sequence(lambda n: f"estudiante{n}@santiagomarino.edu.ve")

    # 7. OTROS DATOS
    foto = "resources/images/ejemplo.png" # O puedes poner "default.png"
    
    # Carreras típicas del Santiago Mariño
    # carrera = factory.Faker('random_element', elements=[
    #     'Ingeniería de Sistemas', 
    #     'Ingeniería Civil', 
    #     'Ingeniería Industrial', 
    #     'Arquitectura'
    # ])
    
    # semestre = factory.Faker('random_int', min=1, max=10)
    
    direccion = factory.Faker('address', locale='es_ES')
    
    # Edad realista para universitarios (17 a 30 años)
    fecha_de_nacimiento = factory.Faker(
        'date_of_birth', 
        minimum_age=17, 
        maximum_age=30
    )


class EnterpriseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Enterprise
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    # RIF como número único (ej: 10000000+)
    rif = factory.Sequence(lambda n: 10000000 + n)
    razon_social = factory.Faker('company', locale='es_ES')
    direccion = factory.Faker('address', locale='es_ES')
    email = factory.Sequence(lambda n: f"empresa{n}@santiagomarino.edu.ve")
    telefono = factory.Sequence(lambda n: f"0414{n:07d}")
    rubro = factory.Faker('random_element', elements=[
        'Tecnología', 'Manufactura', 'Servicios', 'Comercio', 'Construcción'
    ])


class TutorAcademicoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Tutor_Academico
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    primer_nombre = factory.Faker('first_name', locale='es_ES')

    segundo_nombre = factory.Maybe(
        factory.Faker('boolean', chance_of_getting_true=60),
        yes_declaration=factory.Faker('first_name', locale='es_ES'),
        no_declaration=None
    )

    primer_apellido = factory.Faker('last_name', locale='es_ES')
    segundo_apellido = factory.Maybe(
        factory.Faker('boolean', chance_of_getting_true=60),
        yes_declaration=factory.Faker('last_name', locale='es_ES'),
        no_declaration=None
    )

    sexo = factory.Faker('random_element', elements=['M', 'F'])
    foto = "resources/images/ejemplo.png"
    cedula = factory.Sequence(lambda n: 30000000 + n)
    email = factory.Sequence(lambda n: f"tutoraca{n}@santiagomarino.edu.ve")
    fecha_de_nacimiento = factory.Faker('date_of_birth', minimum_age=30, maximum_age=70)
    telefono = factory.Sequence(lambda n: f"0212{n:07d}")
    especialidad = factory.Faker('random_element', elements=['Matemáticas', 'Lenguaje', 'Informática', 'Física'])


class TutorEmpresarialFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Tutor_Empresarial
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    # Crea o asocia una empresa mediante SubFactory
    empresa = factory.SubFactory(EnterpriseFactory)
    primer_nombre = factory.Faker('first_name', locale='es_ES')

    segundo_nombre = factory.Maybe(
        factory.Faker('boolean', chance_of_getting_true=60),
        yes_declaration=factory.Faker('first_name', locale='es_ES'),
        no_declaration=None
    )

    primer_apellido = factory.Faker('last_name', locale='es_ES')
    segundo_apellido = factory.Maybe(
        factory.Faker('boolean', chance_of_getting_true=60),
        yes_declaration=factory.Faker('last_name', locale='es_ES'),
        no_declaration=None
    )

    sexo = factory.Faker('random_element', elements=['M', 'F'])
    foto = "resources/images/ejemplo.png"
    cedula = factory.Sequence(lambda n: 40000000 + n)
    email = factory.Sequence(lambda n: f"tutoremp{n}@santiagomarino.edu.ve")
    fecha_de_nacimiento = factory.Faker('date_of_birth', minimum_age=25, maximum_age=70)
    telefono = factory.Sequence(lambda n: f"0416{n:07d}")
    cargo = factory.Faker('job')
    
class PasantiaFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Pasantia
            sqlalchemy_session = session
            sqlalchemy_session_persistence = 'commit'

        # Asociaciones: crea entidades relacionadas si no existen
        student = factory.SubFactory(StudentFactory)
        empresa = factory.SubFactory(EnterpriseFactory)
        tutor_academico = factory.SubFactory(TutorAcademicoFactory)

        @factory.post_generation
        def tutor_empresarial(self, create, extracted, **kwargs):
            if not create:
                return

            # If caller passed an explicit tutor instance, use it
            if extracted:
                self.tutor_empresarial = extracted
                return

            # Ensure empresa exists; SubFactory on 'empresa' should have created it
            if not getattr(self, 'empresa', None):
                self.empresa = EnterpriseFactory()

            tutor = TutorEmpresarialFactory(empresa=self.empresa)
            self.tutor_empresarial = tutor
            # Persist the association
            session.add(self)
            session.commit()

        # Campos de la pasantía
        carrera = factory.Faker('random_element', elements=[
            'Ingeniería de Sistemas', 'Ingeniería Civil', 'Ingeniería Industrial', 'Arquitectura'
        ])
        semestre = factory.Faker('random_int', min=1, max=10)
        lapso_academico = factory.Faker('random_element', elements=['2023-1', '2023-2', '2024-1', '2024-2'])
        inicio_pasantias = factory.Faker('date_between', start_date='-180d', end_date='today')
        final_pasantias = factory.LazyAttribute(lambda o: (o.inicio_pasantias + timedelta(days=90)) if o.inicio_pasantias else None)
        departamento = factory.Faker('random_element', elements=['Sistemas', 'Recursos Humanos', 'Producción', None])
        estado = factory.Faker('random_element', elements=['solicitada', 'aprobada', 'en progreso', 'finalizada'])
        trabajo_asignado = factory.Faker('paragraph', nb_sentences=3, locale='es_ES')
        titulo_de_informe = factory.LazyAttribute(lambda o: f"Informe de {o.carrera} - {o.lapso_academico}")