
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QHBoxLayout,QStyle,QLineEdit,QAbstractScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings,QWebEnginePage
from modelos.modulo import session,Evaluacion,Pasantia
from sqlalchemy import select
from sqlalchemy import or_,and_
from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from herramientas.modern_messagebox import ModernMessageBox
from herramientas.exports import exportar_modelo_a_excel
from herramientas.variables import semestre
from dotenv import load_dotenv
from herramientas.docs import reemplazar_texto
from herramientas.img_py import convertir_pil_a_pixmap
from herramientas.conversiones import null_string,calcular_edad,calcular_duracion_meses
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent
from admin.main_pasante_adjuntos import show_documentos
from admin.evaluacion import show_evaluar


class StackPasante():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.current_pasante = None
        self.window.StackedPsa.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.window.frame_Psa.installEventFilter(main)
        self.conectar_eventos()
    
    def eventFilter(self,source,event):
        
        if source == self.window.frame_Psa and event.type() == QEvent.Type.Resize:
            self.header()
            height=self.window.tabla_Psa.height()
            self.tamano_pagina=int(height/25.4)
            self.pag_tabla_Psa()
            print("Ejecutando Pasantia")                   
            
    def conectar_eventos(self):
        self.window.btnExportarPsa.clicked.connect(self.exportar)
        self.window.btnNuevoPsa.clicked.connect(self.open_newpasante)
        #self.window.regresarButton.clicked.connect(lambda :self.window.StackedEstudiantes.setCurrentIndex(0))
        self.window.btnAntPsa.clicked.connect(lambda :self.change_table(self.window.btnAntPsa.text()))
        self.window.btnSigPsa.clicked.connect(lambda :self.change_table(self.window.btnSigPsa.text()))
        self.window.searchPsa.textChanged.connect(self.search)
        self.window.comboEstados.activated.connect(lambda: self.cambio_programa())

        # Conectar el botón de ver documentos una sola vez; usará `self.current_pasante`
        self.window.btnviewDocumentos.clicked.connect(self._on_view_documentos)

        self.window.btnEvaluacion.clicked.connect(self._on_view_evaluacion)
        self.window.btnEditarEvaluacion.clicked.connect(self._on_view_evaluacion)
        
        if not self.window.searchPsa.actions(): 
            icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "search.svg"
            
            if icon_path.exists():
                search_icon = QIcon(str(icon_path))
            else:
                # Fallback al icono estándar si no encuentra el archivo
                search_icon = self.window.searchPsa.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            
            # Solo agregamos la acción si no existía ninguna
            self.search_icon = self.window.searchPsa.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
                     
    def ver_estudiantes(self):
        self.window.StackedTutorA.setCurrentIndex(1)
    
    def cambio_programa(self):
        self.numero_pagina=1
        self.window.btnIndPsa.setText(str(self.numero_pagina))
        self.pag_tabla_Psa()
    
    def header(self):
        
        header=self.window.tabla_Psa.horizontalHeader()
        
        #nombres
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        #cedula
        self.window.tabla_Psa.setColumnWidth(1, 80)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        #empresa
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        #lapso
        self.window.tabla_Psa.setColumnWidth(3, 100)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        #estado
        self.window.tabla_Psa.setColumnWidth(4, 100)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        #accion
        self.window.tabla_Psa.setColumnWidth(5, 150)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        
        if self.window.tabla_Psa.width()>1600:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        
        
        self.window.tabla_Psa.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.window.tabla_Psa.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def pag_tabla_Psa(self,search=""):
        offset_count = (self.numero_pagina - 1) * self.tamano_pagina
        stmt = self.get_data(offset_count,search)
        pasantes=session.scalars(stmt).all()
        tabla=self.window.tabla_Psa
        if not pasantes and tabla.rowCount():
            QMessageBox.warning(self.window, "Aviso", "Busqueda no encontrada")
            return
        if len(pasantes)<15:
           self.window.btnSigPsa.setEnabled(False)
        else:
            self.window.btnSigPsa.setEnabled(True)
        
        tabla.setRowCount(0)
        for fila,pasante in enumerate(pasantes):
            tabla.insertRow(fila)
            
            tabla.setItem(fila,0,QTableWidgetItem(pasante.student.primer_nombre+" "+pasante.student.primer_apellido))
            tabla.setItem(fila,1,QTableWidgetItem(str(pasante.student.cedula)))
            tabla.setItem(fila,2,QTableWidgetItem(str(pasante.empresa.razon_social if pasante.empresa else "No Asignada")))
            tabla.setItem(fila,3,QTableWidgetItem(str(pasante.lapso_academico)))
            tabla.setItem(fila,4,QTableWidgetItem(pasante.estado))
                       
            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 

            boton_ver=QPushButton("Ver")
            boton_ver.clicked.connect(lambda checked,x=pasante: self.read_pasante(x))
            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(lambda checked,x=pasante: self.edit_pasante(x))
            btn_borrar = QPushButton("Borrar")
            btn_borrar.clicked.connect(lambda checked,x=pasante: self.delete_pasante(x))

            btn_editar.setStyleSheet("background-color: #4CAF50; color: white;") 
            btn_borrar.setStyleSheet("background-color: #f44336; color: white;")                 
            boton_ver.setStyleSheet("background-color: #3d8ec9; color: white; font-weight: bold;") 

            layout_botones.addWidget(boton_ver)
            layout_botones.addWidget(btn_editar)
            layout_botones.addWidget(btn_borrar)

            # 6. Insertar el contenedor en la celda
            tabla.setCellWidget(fila, 5, widget_contenedor)
        # Esto elimina todas las filas, pero DEJA los títulos de las columnas intactos.

    def get_data(self,offset_count,search=""):
             
        if not self.window.comboEstados.currentData():
            return select(Pasantia).where(
                                        or_(
                                            Pasantia.lapso_academico.ilike(f"{search}%"),
                                            Pasantia.lapso_academico.ilike(f"{search}%")
                                        )
                                        ).limit(self.tamano_pagina).offset(offset_count)
        else:
            return select(Pasantia).where(
                                        and_(
                                        Pasantia.estado==self.window.comboEstados.currentText(),
                                        or_(
                                            Pasantia.lapso_academico.ilike(f"{search}%"),
                                            Pasantia.lapso_academico.ilike(f"{search}%")
                                        )
                                        )
                                        ).limit(self.tamano_pagina).offset(offset_count)
            
    def get_data_all(self,search=""):
             
        if not self.window.comboEstados.currentData():
            return select(Pasantia).where(
                                        or_(
                                            Pasantia.lapso_academico.ilike(f"{search}%"),
                                            Pasantia.lapso_academico.ilike(f"{search}%")
                                        )
                                        )
        else:
            return select(Pasantia).where(
                                        and_(
                                        Pasantia.estado==self.window.comboEstados.currentText(),
                                        or_(
                                            Pasantia.lapso_academico.ilike(f"{search}%"),
                                            Pasantia.lapso_academico.ilike(f"{search}%")
                                        )
                                        )
                                        )

    def search(self):
        self.numero_pagina=1
        self.window.btnIndPsa.setText(str(self.numero_pagina))
        search_query=self.window.searchPsa.text()
        self.pag_tabla_Psa(search_query)
            
    def change_table(self,buttom):
        
        if buttom.lower()=="anterior":
            self.numero_pagina=self.numero_pagina-1 if self.numero_pagina>1 else 1
        elif buttom.lower()=="siguiente":
            self.numero_pagina+=1
        self.window.btnIndPsa.setText(str(self.numero_pagina))
        search_query=self.window.searchPsa.text()
        self.pag_tabla_Psa(search_query)
            
    def read_pasante(self,pasante:Pasantia):
        #Estudiante
        estudiante=pasante.student
        self.window.nombresP.clear()
        self.window.nombresP.setText(estudiante.primer_nombre+" "+null_string(estudiante.segundo_nombre) )
        self.window.apellidosP.clear()
        self.window.apellidosP.setText(estudiante.primer_apellido+" "+null_string(estudiante.segundo_apellido) )
        self.window.cedP.clear()
        self.window.cedP.setText(str(estudiante.cedula))
        self.window.sexEdadP.clear()
        self.window.sexEdadP.setText(str(estudiante.sexo)+" • "+str(calcular_edad(estudiante.fecha_de_nacimiento)))
        self.window.carreraP.clear()
        self.window.carreraP.setText(str(pasante.carrera))
        self.window.semestreP.clear()
        self.window.semestreP.setText(str(pasante.semestre))
        
        #Empresa
        empresa=pasante.empresa
        if empresa:
            self.window.razonP.clear()
            self.window.razonP.setText(empresa.razon_social)
            self.window.rifP.clear()
            self.window.rifP.setText(str(empresa.rif))
            self.window.rubroP.clear()
            self.window.rubroP.setText(empresa.rubro)
            self.window.deparP.clear()
            self.window.deparP.setText(pasante.departamento)
            self.window.trabajoP.clear()
            self.window.trabajoP.setText(pasante.trabajo_asignado)
        else:
            self.window.razonP.clear()
            self.window.razonP.setText("-----------------")
            self.window.rifP.clear()
            self.window.rifP.setText("-----------------")
            self.window.rubroP.clear()
            self.window.rubroP.setText("-----------------")
            self.window.deparP.clear()
            self.window.deparP.setText("-----------------")
            self.window.trabajoP.clear()
            self.window.trabajoP.setText("-----------------")
        
        #pasantia
        self.window.lapsoP.clear()
        self.window.lapsoP.setText(pasante.lapso_academico)
        self.window.inicioP.clear()
        inicio_txt = str(pasante.inicio_pasantias) if pasante.inicio_pasantias else "N/D"
        final_txt = str(pasante.final_pasantias) if pasante.final_pasantias else "N/D"
        self.window.inicioP.setText(f"{inicio_txt} - {final_txt}")
        # Calcular duración en meses entre inicio_pasantias y final_pasantias
        meses = calcular_duracion_meses(pasante.inicio_pasantias, pasante.final_pasantias)
        duracion_txt = f"{meses} meses" if meses is not None else "N/D"
        self.window.duracionP.clear()
        self.window.duracionP.setText(duracion_txt)
        self.window.tituloP.clear()
        self.window.tituloP.setText(pasante.titulo_de_informe)
        self.window.estadoP.clear()
        self.window.estadoP.setText(pasante.estado)
        
        #tutor academico
        tutor_acad=pasante.tutor_academico
        if tutor_acad:
            self.window.tutorAP.clear()
            self.window.tutorAP.setText(tutor_acad.primer_nombre+" "+null_string(tutor_acad.segundo_nombre)+" "+tutor_acad.primer_apellido+" "+null_string(tutor_acad.segundo_apellido))
            self.window.cedulaAP.clear()
            self.window.cedulaAP.setText(str(tutor_acad.cedula))
            self.window.sexEdadAP.clear()
            self.window.sexEdadAP.setText(str(tutor_acad.sexo)+" • "+str(calcular_edad(tutor_acad.fecha_de_nacimiento)))
            self.window.especialidadP.clear()
            self.window.especialidadP.setText(tutor_acad.especialidad)
        else:
            self.window.tutorAP.clear()
            self.window.tutorAP.setText("-----------------")
            self.window.cedulaAP.clear()
            self.window.cedulaAP.setText("-----------------")
            self.window.sexEdadAP.clear()
            self.window.sexEdadAP.setText("-----------------")
            self.window.especialidadP.clear()
            self.window.especialidadP.setText("-----------------")    
        
        #tutor empresarial
        tutor_emp=pasante.tutor_empresarial
        if tutor_emp:
            self.window.tutorEP.clear()
            self.window.tutorEP.setText(tutor_emp.primer_nombre+" "+null_string(tutor_emp.segundo_nombre)+" "+tutor_emp.primer_apellido+" "+null_string(tutor_emp.segundo_apellido))
            self.window.cedulaEP.clear()
            self.window.cedulaEP.setText(str(tutor_emp.cedula))
            self.window.sexEdadEP.clear()
            self.window.sexEdadEP.setText(str(tutor_emp.sexo)+" • "+str(calcular_edad(tutor_emp.fecha_de_nacimiento)))
            self.window.cargoP.clear()
            self.window.cargoP.setText(tutor_emp.cargo)
        else:
            self.window.tutorEP.clear()
            self.window.tutorEP.setText("-----------------")
            self.window.cedulaEP.clear()
            self.window.cedulaEP.setText("-----------------")
            self.window.sexEdadEP.clear()
            self.window.sexEdadEP.setText("-----------------")
            self.window.cargoP.clear()
            self.window.cargoP.setText("-----------------")
            
        self.evaFrame(pasante.evaluacion)
        self.window.StackedPsa.setCurrentIndex(1)
        self.window.regresarButtonP.clicked.connect(lambda: self.window.StackedPsa.setCurrentIndex(0),)
        # Guardamos el pasante actual; el botón ya está conectado a `_on_view_documentos`
        self.current_pasante = pasante
           
    def edit_pasante(self,pasante):
        from admin.nuevo_pasante import NewPasante
        self.newpasante_window=NewPasante(pasante)
        self.newpasante_window.exec()
        self.pag_tabla_Psa()

    def _on_view_documentos(self, checked=False):
        if not getattr(self, 'current_pasante', None):
            return
        show_documentos(self.window, self.current_pasante)
        
    def _on_view_evaluacion(self, checked=False):
        if not getattr(self, 'current_pasante', None):
            return
        show_evaluar(self.current_pasante).exec()
        self.evaFrame(self.current_pasante.evaluacion)
        
    def open_newpasante(self):
        from admin.nuevo_pasante import NewPasante
        self.newpasante_window=NewPasante()
        self.newpasante_window.exec()
        self.pag_tabla_Psa()

    def delete_pasante(self,pasante):
        msg = ModernMessageBox(
                title="Advertencia",
                text="<h3 style='color: #ff5555'>Eliminar Estudiante</h3>",
                informative_text="¿Esta seguro de eliminar esta información?",
                parent=self.main
            )

        btn_save, btn_cancel = msg.add_custom_buttons()
            
            # Ejecutamos el diálogo (Modal loop)
        msg.exec()

        # Verificamos qué botón fue presionado
        clicked = msg.clickedButton()
        
        if clicked == btn_save:
            session.delete(pasante)
            session.commit()
            self.pag_tabla_Psa()
    
    def evaFrame(self,eva:Evaluacion):
        if eva:
            self.window.frameEva1.setHidden(True)
            self.window.frameEva2.setHidden(False)
            
            self.window.nota_tutor_aca.setText(str(eva.nota_tutor_aca))
            self.window.nota_tutor_emp.setText(str(eva.nota_tutor_emp))
            self.window.exposicion.setText(str(eva.exposicion))
            self.window.taller_induccion.setText(str(eva.taller_induccion))
            self.window.total.setText(str(eva.total))
        else:
            self.window.frameEva1.setHidden(False)
            self.window.frameEva2.setHidden(True)
    
            
    def exportar(self):
         # Abrir diálogo para guardar archivo
        archivo, _ = QFileDialog.getSaveFileName(
            self.main, 
            "Guardar Reporte", 
            "", 
            "Archivos de Excel (*.xlsx)"
        )
        
        if archivo:
            if not archivo.endswith('.xlsx'):
                archivo += '.xlsx'
                
            try:
                
                # Llamas a tu función de exportación aquí (Estrategia A o B)
                stmt=self.get_data_all(self.window.searchTutorA.text())
                exportar_modelo_a_excel(session.scalars(stmt).all(),archivo)
                
                QMessageBox.information(self.main, "Éxito", "La base de datos se exportó correctamente.")
            except Exception as e:
                QMessageBox.critical(self.main, "Error", f"No se pudo exportar: {str(e)}")



        
    