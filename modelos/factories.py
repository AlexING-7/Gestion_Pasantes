import factory
from datetime import date, timedelta
from modelos.modulo import session,User,Student,Enterprise,Tutor_Academico,Tutor_Empresarial,Pasantia,Configuracion,Evaluacion,DocumentoAdjunto
import random
import os
import shutil
import uuid
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
    foto = factory.LazyAttribute(lambda o: "resources/images/avatar1.png" if o.sexo=="Masculino" else "resources/images/avatar2.png")
    
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
    foto = "resources/images/avatar1.png"
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
    
    foto = factory.LazyAttribute(lambda o: "resources/images/avatar1.png" if o.sexo=="M" else "resources/images/avatar2.png")
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

    student = factory.SubFactory(StudentFactory)
    
    @factory.lazy_attribute
    def empresa(self):
        ids = [e.id for e in session.query(Enterprise.id).all()]
        if ids:
            return session.get(Enterprise, random.choice(ids))
        return EnterpriseFactory()
    #empresa = factory.SubFactory(EnterpriseFactory)      
    
    @factory.lazy_attribute
    def tutor_academico(self):
        ids = [t.id for t in session.query(Tutor_Academico.id).all()]
        if ids:
            return session.get(Tutor_Academico, random.choice(ids))
        return TutorAcademicoFactory()
    #tutor_academico = factory.SubFactory(TutorAcademicoFactory)

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
       "Arquitectura","Ingeniería Civil","Ingeniería Eléctrica","Ingeniería Electrónica","Ingeniería Industrial","Ingeniería Sistemas","Ingeniería Diseño Industrial"
    ])
    semestre = factory.Faker('random_int', min=8, max=10)
    lapso_academico = factory.Faker('random_element', elements=['2022-1', '2022-2','2023-1', '2023-2', '2024-1', '2024-2', '2025-1', '2025-2', '2026-1'])
    
    
    inicio_pasantias = factory.Faker('date_between', start_date='-180d', end_date='today')
    final_pasantias = factory.LazyAttribute(lambda o: (o.inicio_pasantias + timedelta(days=90)) if o.inicio_pasantias else None)
    departamento = factory.Faker('random_element', elements=['Sistemas', 'Recursos Humanos', 'Producción', None])
    estado = factory.Faker('random_element', elements=['solicitada', 'aprobada', 'en progreso', 'finalizada'])
    trabajo_asignado = factory.Faker('paragraph', nb_sentences=3, locale='es_ES')
    titulo_de_informe = factory.LazyAttribute(lambda o: f"Informe de {o.carrera} - {o.lapso_academico}")
    plan_de_trabajo = factory.Faker('paragraph', nb_sentences=5, locale='es_ES')
    sede = factory.Faker('boolean')
    
    direccion = factory.Maybe(
        'sede',
        yes_declaration=None,
        no_declaration=factory.Faker('address', locale='es_ES')
    )
    jefe_de_carta = factory.Faker('name', locale='es_ES')
    cargo_jefe_de_carta = factory.Faker('job', locale='es_ES')
    
    @factory.post_generation
    def crear_evaluacion_asociada(obj, create, extracted, **kwargs):
        if not create:
            return
        
        # Si el estado es finalizada, creamos la evaluación
        if obj.estado == "finalizada":
            EvaluacionFactory(pasantia=obj)  
            
    @factory.post_generation
    def generar_documentos_asociados(obj, create, extracted, **kwargs):
        if not create:
            return

        DocumentoAdjuntoFactory.create_batch(2, pasantia=obj, solicitud=True)


        if obj.estado in ["aprobada", "en_curso", "finalizada"]:
            DocumentoAdjuntoFactory(pasantia=obj, aprobada=True)

        if obj.estado in ["en_curso", "finalizada"]:
            DocumentoAdjuntoFactory.create_batch(3, pasantia=obj, en_curso=True)

        if obj.estado == "finalizada":
            DocumentoAdjuntoFactory.create_batch(2, pasantia=obj, finalizada=True)  
    class Params:
        # Pasantía recién creada, sin aprobar
        nueva = factory.Trait(
            estado="solicitada",
            tutor_academico=None,
            inicio_pasantias=None,
            final_pasantias=None,
            trabajo_asignado=None,
            titulo_de_informe=None,

        )

        # Pasantía activa (tiene todo asignado)
        activa = factory.Trait(
            estado="aprobada",

        )
        en_curso = factory.Trait(
            estado="en_curso",

        )


        # Pasantía terminada (tiene informe)
        finalizada = factory.Trait(
            estado="finalizada",
        )


class EvaluacionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Evaluacion
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    # Aseguramos que la pasantía asociada esté en un estado evaluable
    pasantia = factory.SubFactory(
        PasantiaFactory,
        estado='finalizada',
        inicio_pasantias=factory.LazyFunction(lambda: date.today() - timedelta(days=120)),
        final_pasantias=factory.LazyFunction(lambda: date.today() - timedelta(days=30)),
    )

    # Notas generadas aleatoriamente en rango realista (1.0 - 20.0)
    nota_tutor_aca = factory.LazyFunction(lambda: round(random.uniform(1.0, 20.0), 2))
    nota_tutor_emp = factory.LazyFunction(lambda: round(random.uniform(1.0, 20.0), 2))
    exposicion = factory.LazyFunction(lambda: round(random.uniform(1.0, 20.0), 2))
    taller_induccion = factory.Faker('boolean')

    @factory.lazy_attribute
    def total(self):
        w_a = 0.40
        w_e = 0.40
        w_expo = 0.15
        w_taller = 0.05
        total = (
            (self.nota_tutor_aca or 0) * w_a
            + (self.nota_tutor_emp or 0) * w_e
            + (self.exposicion or 0) * w_expo
            + (20 if self.taller_induccion else 0) * w_taller
        )
        return round(max(1.0, min(20.0, total)), 2)


class DocumentoAdjuntoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DocumentoAdjunto
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'
        
        exclude = ('_doc_data',)

    # Relación por defecto (puedes sobrescribirla al llamarlo)
    pasantia_id = None 

    # Fecha aleatoria en los últimos 6 meses
    fecha_subida = factory.Faker('date_time_between', start_date='-1w', end_date='now')

    # ---------------------------------------------------------
    # 1. EL DATO VIRTUAL (Tupla por defecto)
    # ---------------------------------------------------------
    # Si no le pasas ningún parámetro, usará esto por defecto:
    _doc_data = factory.Faker('random_element', elements=[
        ("Documento Genérico", "/storage/docs/general/archivo.pdf")
    ])

    # ---------------------------------------------------------
    # 2. SEPARACIÓN DE LOS DATOS (Lazy Attributes)
    # ---------------------------------------------------------
    @factory.lazy_attribute
    def tipo_de_documento(self):
        # Toma el primer elemento de la tupla seleccionada
        return self._doc_data[0]
    
    @factory.lazy_attribute
    def ruta(self):
        CARPETA_DESTINO="resources/documentos/prueba"
        # 1. Obtenemos la ruta base (Origen) que definiste en el Trait
        # Ej: "storage/docs/solicitudes/postulacion.pdf"
        ruta_origen = self._doc_data[1]
        
        # --- SALVAVIDAS ---
        # Si el archivo original no existe en tu PC, Python dará error al intentar copiarlo.
        # Este bloque crea un archivo PDF falso (vacío) en el origen si no lo encuentra.
        if not os.path.exists(ruta_origen):
            os.makedirs(os.path.dirname(ruta_origen), exist_ok=True)
            with open(ruta_origen, 'w') as f:
                f.write("Este es un documento de prueba generado para la tesis.")
        # -----------------

        # 2. Generamos el nuevo nombre único
        nombre_archivo = os.path.basename(ruta_origen) # "postulacion.pdf"
        nombre, extension = os.path.splitext(nombre_archivo) # "postulacion", ".pdf"
        
        uuid_str = uuid_str = str(uuid.uuid4())[:6]
        nuevo_nombre = f"{nombre}_{uuid_str}{extension}" # "postulacion_a1b2c3.pdf"

        # 3. Preparamos la ruta de destino (donde se va a copiar)
        ruta_destino_fisica = os.path.join(CARPETA_DESTINO, nuevo_nombre)

        # 4. Nos aseguramos de que la carpeta destino exista
        os.makedirs(CARPETA_DESTINO, exist_ok=True)

        # 5. ¡LA MAGIA! Copiamos el archivo físico del Origen al Destino
        shutil.copy(ruta_origen, ruta_destino_fisica)

        # 6. Devolvemos la ruta que se va a guardar en la Base de Datos
        # Es buena práctica guardar rutas relativas en la BD, no rutas absolutas como "C:/Usuarios/..."
        ruta_para_bd = f"resources/documentos/prueba/{nuevo_nombre}"
        return ruta_para_bd

    # ---------------------------------------------------------
    # 3. LOS PARÁMETROS CONDICIONALES (Traits)
    # ---------------------------------------------------------
    class Params:
        # Etapa 1: Solicitud de Pasantía
        solicitud = factory.Trait(
            estado="revision",#factory.Faker('random_element', elements=['revision', 'aprobado']),
            _doc_data=factory.Faker('random_element', elements=[
                ("Carta de Postulación", "resources/formatos_pdf_BD/1. CARTA SOLICITUD DE PASANTIA.pdf"),
                ("Carta de Aceptación", "resources/formatos_pdf_BD/2.CARTA ACEPTACION DEL PASANTE.pdf")
            ])
        )

        # Etapa 2: Pasantía Aprobada
        aprobada = factory.Trait(
            estado="aprobado",
            _doc_data=factory.Faker('random_element', elements=[
                ("Carta de Aceptación", "resources/formatos_pdf_BD/2.CARTA ACEPTACION DEL PASANTE.pdf"),
                ("Acta de Inicio De Ejecución de Pasantias", "resources/formatos_pdf_BD/3.ACTA DE INICIO.pdf"),
                ("Contrato del Pasante", "resources/formatos_pdf_BD/5.CONTRATO DEL PASANTE.pdf"),
                ("Inscripción de Pasantias", "resources/formatos_pdf_BD/6. INSCRIPCION DE PASANTIA.pdf"),
            ])
        )

        # Etapa 3: Pasantía En Curso
        en_curso = factory.Trait(
            estado=factory.Faker('random_element', elements=['revision', 'aprobado']),
            _doc_data=factory.Faker('random_element', elements=[
                ("Cronograma de Actividades", "resources/formatos_pdf_BD/8.CRONOGRAMA DE ACTIVIDADES.pdf"),
                ("Plan de Trabajo", "resources/formatos_pdf_BD/9.PLAN DE TRABAJO.pdf"),
                ("Acta de Aprobación del Informe", "resources/formatos_pdf_BD/10. ACTA DE APROBACION DEL INFORME DE PASANTÍA.pdf"),
                ("Autorización Presentación del Informe", "resources/formatos_pdf_BD/14. AUTORIZACION PRESENTACION DEL INFORME.pdf"),
            ])
        )

        # Etapa 4: Pasantía Finalizada
        finalizada = factory.Trait(
            estado="aprobado",
            _doc_data=factory.Faker('random_element', elements=[
                ("Evaluacion", "resources/formatos_pdf_BD/EVALUACION.pdf"),
                ("Evaluacion Final", "resources/formatos_pdf_BD/EVALUACION FINAL.pdf"),
            ])
        )

class ConfiguracionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Configuracion
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    # Clave única para la variable de configuración
    clave = factory.Sequence(lambda n: f"clave_{n}")
    # Valor puede ser cualquier cadena; usamos una frase corta en español
    valor = factory.Faker('sentence', nb_words=4, locale='es_ES')