
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QListWidgetItem

from modelos.modulo import session,Student,Pasantia
from sqlalchemy import select
from sqlalchemy import or_,and_, cast, String
from getmac import get_mac_address as gma
from herramientas.widgets_personalizados import MiWidgetClickeable
from herramientas.plantilla_ui import cargar_ui
from herramientas.conversiones import null_string,calcular_edad,calcular_duracion_meses,convertir_pil_a_pixmap,formato_miles,guion_telefono
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent,QSize

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class StackPasante():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.current_pasante = None
        self.listaID=self.window.listPasanteID     
        self.conectar_eventos()
        self.window.stackedWidget.setCurrentIndex(1)
        self.window.stackedPasante.setCurrentIndex(0)
    
    def conectar_eventos(self):
        self.window.pasantes_btnSiguiente.clicked.connect(self.siguiente)
        self.window.pasantes_btnAnterior.clicked.connect(self.anterior)
        self.window.searchPasante.textChanged.connect(self.search)
        self.lista_pasantes()
    def siguiente(self):
        num=self.window.stackedPasante.currentIndex()
        self.window.stackedPasante.setCurrentIndex(num+1 if num<2 else 0)
    
    def anterior(self):
        num=self.window.stackedPasante.currentIndex()
        self.window.stackedPasante.setCurrentIndex(num-1 if num>0 else 2)
      
    def lista_pasantes(self):
        self.listaID.clear()
        pasantes=self.get_data()
        for id in pasantes:
            planilla=cargar_ui("UI/pasante_id.ui",self.main)
            item = QListWidgetItem()
            item.setSizeHint(QSize(150,94))
            self.listaID.addItem(item)
            self.listaID.setItemWidget(item, planilla)
            self.conectarWidget(planilla,id)
        
    def get_data(self):
        search_query=self.window.searchPasante.text()
        search_query = (search_query or "").strip()
        stmt = select(Pasantia).join(Pasantia.student)
        if search_query:
            # cedula is stored as int; cast to String to allow prefix searches
            stmt = stmt.where(cast(Student.cedula, String).ilike(f"{search_query}%"))
        results = session.scalars(stmt).all()
        return results
    
    def conectarWidget(self,widget,data:Pasantia):
        widget.nombre.setText(f"{data.student.primer_nombre} {data.student.primer_apellido}")
        widget.carrera.setText(data.carrera)
        widget.widget.clicked.connect(lambda: self.datos(data))
        
    def datos(self,data:Pasantia):
        estudiante=data.student
        tutorA=data.tutor_academico
        tutorB=data.tutor_empresarial
        empresa=data.empresa
        widget=self.window
        widget.pasantes_nombreC.setText(f"{estudiante.primer_nombre} {estudiante.primer_apellido}")
        widget.pasantes_carrera.setText(data.carrera)
        widget.pasantes_foto.setPixmap(convertir_pil_a_pixmap(estudiante.foto))
        widget.pasantes_sexo.setText(estudiante.sexo)
        widget.pasantes_cedula.setText(f"V-{formato_miles(estudiante.cedula)}")
        widget.pasantes_edad.setText(str(calcular_edad(estudiante.fecha_de_nacimiento)))
        widget.pasantes_telefono.setText(guion_telefono(estudiante.telefono))
        widget.pasantes_email.setText(estudiante.email)
        widget.pasantes_direccion.setText(estudiante.direccion)
        widget.pasantes_lapso.setText(data.lapso_academico)
        widget.pasantes_tutorA_nombreC.setText(f"{tutorA.primer_nombre} {tutorA.primer_apellido}")
        widget.pasantes_tutorB_nombreC.setText(f"{tutorB.primer_nombre} {tutorB.primer_apellido}")
        widget.pasantes_empresa_razon.setText(empresa.razon_social)
        widget.pasantes_inicio.setText(str(data.inicio_pasantias))
        widget.pasantes_final.setText(str(data.final_pasantias))
        widget.pasantes_titulo.setText(data.titulo_de_informe)
        widget.pasantes_departamento.setText(data.departamento)
        if data.sede:
            widget.pasantes_sedeSucursal_label.setText("Sede")
            widget.pasantes_empresa_direccion.setText(empresa.direccion)
        else:
            widget.pasantes_sedeSucursal_label.setText("Sucursal")
            widget.pasantes_empresa_direccion.setText(data.direccion)
        widget.pasantes_reprEmpresa.setText(data.jefe_de_carta)
        widget.pasantes_reprEmpresa_cargo.setText(data.cargo_jefe_de_carta)
        widget.pasantes_trabajo.setText(data.trabajo_asignado)
        widget.pasantes_plan.setText(data.plan_de_trabajo)
    
    def search(self):
        self.lista_pasantes()
        
        