

from sqlalchemy import (create_engine,ForeignKey,Column,Integer,String,Date,Float,DateTime,Boolean,event)
from sqlalchemy.orm import Mapped, mapped_column,declarative_base,relationship,sessionmaker
from sqlalchemy.dialects.mysql import LONGTEXT
from typing import Optional,List
from datetime import date, datetime
from sqlalchemy_utils import database_exists,create_database
mysql_db_url="mysql+pymysql://root@127.0.0.1/gestion_pasantes"

engine=create_engine(mysql_db_url)
Session=sessionmaker(bind=engine)
session=Session()

Base = declarative_base()

class BaseModel(Base):
    __abstract__=True
    __allow_unmapped__=True
    
    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)
    
class User(BaseModel):
    __tablename__="users"
    
    username: Mapped[str]=mapped_column(String(30),unique=True)
    password: Mapped[str]=mapped_column(String(20))
    email: Mapped[str]=mapped_column(String(100), unique=True)
    rol: Mapped[Optional[str]]=mapped_column(String(20))#(admin,coordinador)
    
    tsessions: Mapped[List["TSession"]] = relationship()
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, rol={self.rol!r})"
    
class TSession(BaseModel):
    __tablename__="sessions"
       
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    mac_adresss: Mapped[str]=mapped_column(String(25))
    data_session= Column(LONGTEXT)
    last_activity:Mapped[int]
    
    user: Mapped["User"] = relationship(back_populates="tsessions")
    
    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, mac_adresss={self.mac_adresss!r}, last_activity={self.last_activity!r})"
    
class Student(BaseModel):
    __tablename__="students"
    
    primer_nombre: Mapped[str]=mapped_column(String(20))
    segundo_nombre: Mapped[str]=mapped_column(String(20),nullable=True)
    primer_apellido: Mapped[str]=mapped_column(String(20))
    segundo_apellido: Mapped[str]=mapped_column(String(20),nullable=True)
    sexo: Mapped[Optional[str]] = mapped_column(String(3))
    cedula:Mapped[int]=mapped_column(unique=True)
    telefono: Mapped[str]=mapped_column(String(11),nullable=True)
    email: Mapped[str]=mapped_column(String(100), unique=True)
    foto: Mapped[str]=mapped_column(String(255),nullable=True)  
    direccion: Mapped[str] = mapped_column(LONGTEXT,nullable=True)
    fecha_de_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    pasantias: Mapped[List["Pasantia"]] = relationship()
    
    def __repr__(self) -> str:
        return f"Student {self.primer_nombre} {self.primer_apellido} CIV:{self.cedula}"

class Enterprise(BaseModel):
    __tablename__="enterprises"
    
    rif:Mapped[int]=mapped_column(unique=True)
    razon_social: Mapped[str]=mapped_column(String(50))
    direccion: Mapped[str]=mapped_column(String(255),default="Edo Barinas")
    email: Mapped[str]=mapped_column(String(100), unique=True)
    telefono: Mapped[str]=mapped_column(String(11), unique=True)
    rubro: Mapped[str]=mapped_column (String(20),nullable=True)
    
    tutores: Mapped[List["Tutor_Empresarial"]] = relationship()
    pasantias: Mapped[List["Pasantia"]] = relationship()

    def __repr__(self) -> str:
        return f"Enterprise {self.razon_social} RIF:{self.rif}"
    
    
class Tutor_Academico(BaseModel):
    __tablename__="tutores_academicos"
    
    primer_nombre: Mapped[str]=mapped_column(String(20))
    segundo_nombre: Mapped[str]=mapped_column(String(20),nullable=True)
    primer_apellido: Mapped[str]=mapped_column(String(20))
    segundo_apellido: Mapped[str]=mapped_column(String(20),nullable=True)
    sexo: Mapped[Optional[str]] = mapped_column(String(3))
    foto: Mapped[str]=mapped_column(String(255),nullable=True)
    cedula:Mapped[int]=mapped_column(unique=True)
    email: Mapped[str]=mapped_column(String(100), unique=True)
    fecha_de_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    telefono: Mapped[str]=mapped_column(String(11),nullable=True)

    especialidad: Mapped[str]=mapped_column(String(20))
    pasantias: Mapped[List["Pasantia"]] = relationship()

    def __repr__(self) -> str:
        return f"Tutor Academico {self.primer_nombre} {self.primer_apellido} CIV:{self.cedula}"

class Tutor_Empresarial(BaseModel):
    __tablename__="tutores_empresariales"
    
    id_empresa:Mapped[int]=mapped_column(ForeignKey("enterprises.id"))
    primer_nombre: Mapped[str]=mapped_column(String(20))
    segundo_nombre: Mapped[str]=mapped_column(String(20),nullable=True)
    primer_apellido: Mapped[str]=mapped_column(String(20))
    segundo_apellido: Mapped[str]=mapped_column(String(20),nullable=True)
    sexo: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    foto: Mapped[str]=mapped_column(String(255),nullable=True)
    cedula:Mapped[int]=mapped_column(unique=True)
    email: Mapped[str]=mapped_column(String(100), unique=True)
    fecha_de_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    telefono: Mapped[str]=mapped_column(String(11), unique=True)
    
    cargo: Mapped[str]=mapped_column(String(20))
    
    pasantias: Mapped[List["Pasantia"]] = relationship()
    empresa: Mapped["Enterprise"] = relationship(back_populates="tutores")
    
    def __repr__(self) -> str:
        return f"Tutores Empresariales {self.primer_nombre} {self.primer_apellido} CIV:{self.cedula}"

class Pasantia(BaseModel):
    __tablename__ = "pasantias"

    # Claves foráneas
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    empresa_id: Mapped[Optional[int]] = mapped_column(ForeignKey("enterprises.id"), nullable=True)
    tutor_academico_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tutores_academicos.id"), nullable=True)
    tutor_empresarial_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tutores_empresariales.id"), nullable=True)

    # Campos de la pasantía
    carrera: Mapped[str]=mapped_column(String(100))
    semestre: Mapped[int]
    lapso_academico: Mapped[str] = mapped_column(String(50))
    inicio_pasantias: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    final_pasantias: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    departamento: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="solicitada")
    trabajo_asignado: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)
    titulo_de_informe: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    plan_de_trabajo: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)
    sede: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    direccion: Mapped[str] = mapped_column(String(255), nullable=True)
    jefe_de_carta: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    cargo_jefe_de_carta: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    #lugar_de_entrenamiento
    #escuela

    # Relaciones (opcionalmente navegables desde la pasantía)
    student: Mapped["Student"] = relationship(back_populates="pasantias")
    empresa: Mapped["Enterprise"] = relationship(back_populates="pasantias")
    tutor_academico: Mapped["Tutor_Academico"] = relationship(back_populates="pasantias")
    tutor_empresarial: Mapped["Tutor_Empresarial"] = relationship(back_populates="pasantias")
    evaluacion: Mapped[Optional["Evaluacion"]] = relationship(
        back_populates="pasantia", 
        cascade="all, delete-orphan"
    )
    documentos: Mapped[List["DocumentoAdjunto"]] = relationship(back_populates="pasantia")


@event.listens_for(Pasantia, "before_insert")
@event.listens_for(Pasantia, "before_update")
def _pasantia_empty_strings_to_none(mapper, connection, target):
    """Convertir atributos tipo str con cadena vacía a None antes de persistir."""
    for col in target.__table__.columns:
        try:
            val = getattr(target, col.name)
        except AttributeError:
            continue
        if isinstance(val, str) and val == "":
            setattr(target, col.name, None)

class Evaluacion(BaseModel):
    __tablename__ = "evaluaciones"

    pasantia_id: Mapped[int] = mapped_column(ForeignKey("pasantias.id"))
    nota_tutor_aca: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    nota_tutor_emp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    exposicion: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    taller_induccion: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    pasantia: Mapped["Pasantia"] = relationship(back_populates="evaluacion")

    def __repr__(self) -> str:
        return f"Evaluacion(pasantia_id={self.pasantia_id!r}, nota_tutor_aca={self.nota_tutor_aca!r})"

class DocumentoAdjunto(BaseModel):
    __tablename__ = "documentos_adjuntos"

    pasantia_id: Mapped[int] = mapped_column(ForeignKey("pasantias.id"))
    tipo_de_documento: Mapped[str] = mapped_column(String(100))
    ruta: Mapped[str] = mapped_column(String(255))
    fecha_subida: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    estado: Mapped[str] = mapped_column(String(20), default="revision")  # aprobado, revision, denegado

    pasantia: Mapped["Pasantia"] = relationship(back_populates="documentos")

    def __repr__(self) -> str:
        return f"DocumentoAdjunto(pasantia_id={self.pasantia_id!r}, tipo={self.tipo_de_documento!r})"

class Configuracion(BaseModel):
    __tablename__ = "configuraciones"
    clave:Mapped[str] = mapped_column(String(100))
    valor:Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return (f"Variable(clave={self.clave!r}, valor={self.valor!r})")

class SistemaLog(BaseModel):
    __tablename__ = "sistema_logs"

    fecha_hora: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    usuario: Mapped[str] = mapped_column(String(50), nullable=False)
    accion: Mapped[str] = mapped_column(String(20), nullable=False)
    tabla_afectada: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    id_registro_afectado: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    valores_anteriores = Column(LONGTEXT, nullable=True)
    valores_nuevos = Column(LONGTEXT, nullable=True)
    mensaje: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    ip_maquina: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    def __repr__(self) -> str:
        return (
            f"SistemaLog(id={self.id!r}, usuario={self.usuario!r}, accion={self.accion!r}, "
            f"tabla={self.tabla_afectada!r}, id_registro={self.id_registro_afectado!r})"
        )

    @classmethod
    def crear_log(cls, session, usuario: str, accion: str, tabla_afectada: Optional[str] = None,
                  id_registro_afectado: Optional[int] = None, valores_anteriores: Optional[str] = None,
                  valores_nuevos: Optional[str] = None, mensaje: Optional[str] = None,
                  ip_maquina: Optional[str] = None):
        log = cls(
            usuario=usuario,
            accion=accion,
            tabla_afectada=tabla_afectada,
            id_registro_afectado=id_registro_afectado,
            valores_anteriores=valores_anteriores,
            valores_nuevos=valores_nuevos,
            mensaje=mensaje,
            ip_maquina=ip_maquina,
        )
        session.add(log)
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

if __name__=="__main__":
    if not database_exists(mysql_db_url):
        create_database(mysql_db_url)
    #Base.metadata.create_all(engine)
