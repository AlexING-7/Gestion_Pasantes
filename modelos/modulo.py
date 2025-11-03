

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
    
    username: Mapped[str]=mapped_column(String(30))
    password: Mapped[str]=mapped_column(String(20))
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

if __name__=="__main__":
    if not database_exists(mysql_db_url):
        create_database(mysql_db_url)
    Base.metadata.create_all(engine)
