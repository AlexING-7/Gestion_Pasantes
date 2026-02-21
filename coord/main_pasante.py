
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QListWidgetItem

from modelos.modulo import session,Student,Pasantia,DocumentoAdjunto
from sqlalchemy import select
from sqlalchemy import or_,and_, cast, String,func, case,desc,Integer
from getmac import get_mac_address as gma
from herramientas.widgets_personalizados import MiWidgetClickeable
from herramientas.plantilla_ui import cargar_ui
from herramientas.modern_messagebox import ModernMessageBox
from herramientas.conversiones import nombreCompleto,calcular_edad,calcular_duracion_meses,convertir_pil_a_pixmap,formato_miles,guion_telefono
from PySide6.QtWidgets import QHeaderView,QMessageBox
from PySide6.QtCore import QEvent,QSize
from coord.main_documentos import StackedDocumentos



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class StackPasante():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.current_pasante = None
        self.listaID=self.window.listPasanteID     
        self.conectar_eventos()
        self.window.stackedWidget.setCurrentIndex(1)
        self.window.btnSalirDocs.click()
    
    def conectar_eventos(self):
        self.window.pasantes_btnSiguiente.clicked.connect(self.siguiente)
        self.window.pasantes_btnAnterior.clicked.connect(self.anterior)
        self.window.searchPasante.textChanged.connect(self.search)
        self.window.btnVerDocs.clicked.connect(lambda:self.cambio(False))
        self.window.btnSalirDocs.clicked.connect(lambda: self.cambio(True))
        
        self.lista_pasantes()
        item = self.listaID.item(0)
        wid = self.listaID.itemWidget(item)
        wid.widget.click()
    
    def cambio(self,bool):
        if bool:
            self.window.stackedPasante.setCurrentIndex(1)
            self.window.pasantes_btnGen.setHidden(True)
            self.window.pasantes_btnSiguiente.setHidden(False)
            self.window.pasantes_btnAnterior.setHidden(False)
        else:
            self.window.stackedPasante.setCurrentIndex(0)
            self.window.pasantes_btnGen.setHidden(False)
            self.window.pasantes_btnSiguiente.setHidden(True)
            self.window.pasantes_btnAnterior.setHidden(True)
    
    def siguiente(self):
        indice_actual = self.window.stackedPasante.currentIndex()
        total_paginas = self.window.stackedPasante.count()
        
        nuevo_indice = indice_actual + 1
        
        if nuevo_indice >= total_paginas:
            nuevo_indice = 1
            
        self.window.stackedPasante.setCurrentIndex(nuevo_indice)
        
    def anterior(self):
        indice_actual = self.window.stackedPasante.currentIndex()
        total_paginas = self.window.stackedPasante.count()
        if total_paginas <= 1:
            return
        nuevo_indice = indice_actual - 1
        if nuevo_indice < 1:
            nuevo_indice = total_paginas - 1
        self.window.stackedPasante.setCurrentIndex(nuevo_indice)
        
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
        stmt = stmt.order_by(
                # 1. Ordenar por el año (Primeros 4 caracteres)
                desc(func.substr(Pasantia.lapso_academico, 1, 4)),
        
                # 2. Ordenar por el número del lapso (Convertido a Entero)
                # Tomamos desde el carácter 6 hasta el final y lo hacemos número
                desc(cast(func.substr(Pasantia.lapso_academico, 6), Integer))
                )
        
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
        self.current_pasante=data
        estudiante=data.student
        tutorA=data.tutor_academico
        tutorB=data.tutor_empresarial
        empresa=data.empresa
        widget=self.window
        widget.pasantes_nombreC.setText(f"{estudiante.primer_nombre} {estudiante.primer_apellido}")
        widget.pasantes_carrera.setText(data.carrera)
        #widget.pasantes_nombresA.setText(nombreCompleto(estudiante))
        widget.pasantes_fechaN.setText(str(estudiante.fecha_de_nacimiento))
        widget.pasantes_foto.setPixmap(convertir_pil_a_pixmap(estudiante.foto,160,160))
        widget.pasantes_sexo.setText(estudiante.sexo)
        widget.pasantes_cedula.setText(f"V-{formato_miles(estudiante.cedula)}")
        widget.pasantes_edad.setText(str(calcular_edad(estudiante.fecha_de_nacimiento)))
        widget.pasantes_telefono.setText(guion_telefono(estudiante.telefono))
        widget.pasantes_email.setText(estudiante.email)
        widget.pasantes_direccion.setText(estudiante.direccion)
        widget.pasantes_lapso.setText(data.lapso_academico)
        widget.pasantes_tutorA_nombreC.setText(f"{getattr(tutorA,"primer_nombre","No")} {getattr(tutorA,"primer_apellido","fue Asignado Tutor Academico")}")
        widget.pasantes_tutorE_nombreC.setText(f"{getattr(tutorB,"primer_nombre","No")} {getattr(tutorB,"primer_apellido","fue Asignado Empresarial")}")
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
        try:
            widget.btnAsignarTutor.clicked.disconnect()
            self.window.pasantes_btnGen.clicked.disconnect()
            widget.btnEditarPasante.clicked.disconnect()
            self.window.btnEvaluar.clicked.disconnect()
        except TypeError:
            pass
        self.ver_documentos()
        widget.btnAsignarTutor.clicked.connect(lambda: self.asignarTutorA(data))
        widget.btnEditarPasante.clicked.connect(lambda: self.editar())
        self.window.pasantes_btnGen.clicked.connect(lambda: self.irGenerar(data))
        self.window.btnEvaluar.clicked.connect(lambda: self.evaluar())
    
    def irGenerar(self,dato):
        self.docs=StackedDocumentos(self.main)
        self.docs.find(dato)
    
    
    def search(self):
        self.lista_pasantes()
        
    def asignarTutorA(self,pasante:Pasantia):
        from coord.asignar_tutor import NewAsignar
        asignar=NewAsignar(pasante)
        asignar.exec()
    
    def editar(self):
        from coord.nuevo_pasante import NewPasante
        
        self.VentanaPasante=NewPasante(self.current_pasante)
        self.VentanaPasante.exec()
        self.datos(self.current_pasante)
        self.lista_pasantes()
        
    
    def ver_documentos(self):
        if not hasattr(self,"current_pasante"):
            return
        
        self.window.listDocsPasante.clear()
        #pasantes=self.get_data()
        for id in self.current_pasante.documentos:
            planilla=cargar_ui("UI/documento_pasantes.ui",self.main)
            item = QListWidgetItem()
            item.setSizeHint(QSize(125,175))
            self.window.listDocsPasante.addItem(item)
            self.window.listDocsPasante.setItemWidget(item, planilla)
            self.conectarDocsWidget(planilla,id)
        else:
            planilla=cargar_ui("UI/documento_pasantes - Copy.ui",self.main)
            item = QListWidgetItem()
            item.setSizeHint(QSize(125,125))
            self.window.listDocsPasante.addItem(item)
            self.window.listDocsPasante.setItemWidget(item, planilla)
            planilla.frame.clicked.connect(lambda:self.subir())
    
    def subir(self):
        from coord.subirdocs import NewDoc
        doc=NewDoc(self.current_pasante)
        doc.exec()
        self.ver_documentos()
    
    def conectarDocsWidget(self,widget,id:DocumentoAdjunto):
        widget.nombre.setText(f"{id.tipo_de_documento}")
        widget.btnVer.clicked.connect(lambda:self.ver_documento(id))
        widget.btnBorrar.clicked.connect(lambda: self.borrarDoc(id))
        
    def ver_documento(self,doc):
        from coord.ver_documento import WebViewDoc
        self.ver=WebViewDoc(doc)
        self.ver.exec()
        self.window.btnVerDocs.clicked.connect(self.ver_documentos)
    
    def borrarDoc(self,tutor):
        msg = ModernMessageBox(
                title="Advertencia",
                text="<h3 style='color: #ff5555'>Eliminar Documento</h3>",
                informative_text="¿Esta seguro de eliminar esta información?",
                parent=self.main
            )

        btn_save, btn_cancel = msg.add_custom_buttons()
            
            # Ejecutamos el diálogo (Modal loop)
        msg.exec()

        # Verificamos qué botón fue presionado
        clicked = msg.clickedButton()
        
        if clicked == btn_save:
            session.delete(tutor)
            session.commit()
            self.ver_documentos()
    
    def evaluar(self):
        from admin.evaluacion import show_evaluar
        session.commit()
        if self.current_pasante.estado!="finalizada":
            if QMessageBox.question(self.main, "Pasante Evaluacion", "El pasante no ha terminado la pasantais para evaluar ¿Deseas Continuar?") == QMessageBox.StandardButton.Yes:
                show_evaluar(self.current_pasante).exec()
        else:
            show_evaluar(self.current_pasante,True).exec()
        
        
        