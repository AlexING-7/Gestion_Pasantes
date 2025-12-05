

from sqlalchemy import (create_engine,ForeignKey,Column,Integer,String)
from sqlalchemy.orm import Mapped, mapped_column,declarative_base,relationship,sessionmaker
from sqlalchemy.dialects.mysql import LONGTEXT
from typing import Optional,List
from sqlalchemy_utils import database_exists,create_database
mysql_db_url="mysql+pymysql://root@127.0.0.1/gestion_pasantes"

engine=create_engine(mysql_db_url)
Session=sessionmaker(bind=engine)
session=Session()

Base = declarative_base()

class BaseModel(Base):
    __abstract__=True
    __allow_unmapped__=True
    
    id=Column(Integer,primary_key=True)
    
class User(BaseModel):
    __tablename__="users"
    
    username: Mapped[str]=mapped_column(String(30),unique=True)
    password: Mapped[str]=mapped_column(String(20))
    email: Mapped[str]=mapped_column(String(100), unique=True)
    rol: Mapped[Optional[str]]=mapped_column(String(20))
    
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
    cedula:Mapped[int]=mapped_column(unique=True)
    email: Mapped[str]=mapped_column(String(100), unique=True)
    carrera: Mapped[str]=mapped_column(String(100))
    semestre: Mapped[int]
    telefono: Mapped[str]=mapped_column(String(11))#unique
    direccion: Mapped[str]=mapped_column(String(255))
    
    def __repr__(self) -> str:
        return f"Student {self.primer_nombre} {self.primer_apellido} CIV:{self.cedula}"

class Enterprise(BaseModel):
    __tablename__="enterprises"
    
    rif:Mapped[int]=mapped_column(unique=True)
    razon_social: Mapped[str]=mapped_column(String(50))
    direccion: Mapped[str]=mapped_column(String(255))
    telefono: Mapped[str]=mapped_column(String(11))#unique
    rubro: Mapped[str]=mapped_column(String(20))
    
    tutores: Mapped[List["Tutor_Empresarial"]] = relationship()

    def __repr__(self) -> str:
        return f"Enterprise {self.razon_social} RIF:{self.rif}"
    
    
class Tutor_Academico(BaseModel):
    __tablename__="tutores_academicos"
    
    primer_nombre: Mapped[str]=mapped_column(String(20))
    segundo_nombre: Mapped[str]=mapped_column(String(20),nullable=True)
    primer_apellido: Mapped[str]=mapped_column(String(20))
    segundo_apellido: Mapped[str]=mapped_column(String(20),nullable=True)
    cedula:Mapped[int]=mapped_column(unique=True)
    email: Mapped[str]=mapped_column(String(100), unique=True)
    especialidad: Mapped[str]=mapped_column(String(20))

    def __repr__(self) -> str:
        return f"Tutor Academico {self.primer_nombre} {self.primer_apellido} CIV:{self.cedula}"

class Tutor_Empresarial(BaseModel):
    __tablename__="tutores_empresariales"
    
    id_empresa:Mapped[int]=mapped_column(ForeignKey("enterprises.id"))
    primer_nombre: Mapped[str]=mapped_column(String(20))
    segundo_nombre: Mapped[str]=mapped_column(String(20),nullable=True)
    primer_apellido: Mapped[str]=mapped_column(String(20))
    segundo_apellido: Mapped[str]=mapped_column(String(20),nullable=True)
    cedula:Mapped[int]=mapped_column(unique=True)
    email: Mapped[str]=mapped_column(String(100), unique=True)
    telefono: Mapped[str]=mapped_column(String(7))
    cargo: Mapped[str]=mapped_column(String(20))
    
    empresa: Mapped["Enterprise"] = relationship(back_populates="tutores")
    
    def __repr__(self) -> str:
        return f"Tutores Empresariales {self.primer_nombre} {self.primer_apellido} CIV:{self.cedula}"

class Pasantia:
    __tablename__="pasantias"
    pass
    
if __name__=="__main__":
    if not database_exists(mysql_db_url):
        create_database(mysql_db_url)
    Base.metadata.create_all(engine)
