
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
from modelos.modulo import session,Tutor_Empresarial,Enterprise
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
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent

class StackTutorE():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.StackedTutorA.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.window.frame_TutorE.installEventFilter(main)
        self.conectar_eventos()
    
    def eventFilter(self,source,event):
        
        if source == self.window.frame_TutorE and event.type() == QEvent.Type.Resize:
            self.header()
            height=self.window.tabla_TutorE.height()
            self.tamano_pagina=int(height/25.4)
            self.pag_tabla_tutorE()
            print("Ejecutando Tutores Empresariales")                   
            
    def conectar_eventos(self):
        self.window.btnExportarTutorE.clicked.connect(self.exportar)
        self.window.btnNuevoTutorE.clicked.connect(self.open_newtutor)
        #self.window.regresarButton.clicked.connect(lambda :self.window.StackedEstudiantes.setCurrentIndex(0))
        self.window.btnAntTutorE.clicked.connect(lambda :self.change_table(self.window.btnAntTutorE.text()))
        self.window.btnSigTutorE.clicked.connect(lambda :self.change_table(self.window.btnSigTutorE.text()))
        self.window.searchTutorE.textChanged.connect(self.search)
        self.window.comboEmpresas.activated.connect(lambda: self.cambio_programa())

        
        
        if not self.window.searchTutorE.actions(): 
            icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "search.svg"
            
            if icon_path.exists():
                search_icon = QIcon(str(icon_path))
            else:
                # Fallback al icono estándar si no encuentra el archivo
                search_icon = self.window.searchTutorE.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            
            # Solo agregamos la acción si no existía ninguna
            self.search_icon = self.window.searchTutorE.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
                     
    def ver_estudiantes(self):
        self.window.StackedTutorE.setCurrentIndex(1)
    
    def cambio_programa(self):
        self.numero_pagina=1
        self.window.btnIndTutorE.setText(str(self.numero_pagina))
        self.pag_tabla_tutorE()
    
    def header(self):
        
        header=self.window.tabla_TutorE.horizontalHeader()
        #cedula
        self.window.tabla_TutorE.setColumnWidth(0, 80)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        #nombres
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        #email
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        #tlf
        self.window.tabla_TutorE.setColumnWidth(6, 100)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        #accion
        self.window.tabla_TutorE.setColumnWidth(8, 150)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        
        if self.window.tabla_TutorE.width()>1600:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        
        
        self.window.tabla_TutorE.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.window.tabla_TutorE.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def pag_tabla_tutorE(self,search=""):
        offset_count = (self.numero_pagina - 1) * self.tamano_pagina
        stmt = self.get_data(offset_count,search)
        tutores=session.scalars(stmt).all()
        tabla=self.window.tabla_TutorE
        if not tutores and tabla.rowCount():
            QMessageBox.warning(self.window, "Aviso", "Busqueda no encontrada")
            return
        if len(tutores)<15:
           self.window.btnSigTutorE.setEnabled(False)
        else:
            self.window.btnSigTutorE.setEnabled(True)
        
        tabla.setRowCount(0)
        for fila,tutores in enumerate(tutores):
            tabla.insertRow(fila)
            
            tabla.setItem(fila,0,QTableWidgetItem(str(tutores.cedula)))
            tabla.setItem(fila,1,QTableWidgetItem(str(tutores.primer_nombre)))
            tabla.setItem(fila,2,QTableWidgetItem(str(tutores.segundo_nombre if tutores.segundo_nombre else "")))
            tabla.setItem(fila,3,QTableWidgetItem(str(tutores.primer_apellido)))
            tabla.setItem(fila,4,QTableWidgetItem(tutores.segundo_apellido if tutores.segundo_apellido else ""))
            tabla.setItem(fila,5,QTableWidgetItem(str(tutores.email)))
            tabla.setItem(fila,6,QTableWidgetItem(str(tutores.telefono)))
            tabla.setItem(fila,7,QTableWidgetItem(str(tutores.cargo)))
                       
            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 

            boton_ver=QPushButton("Ver")
            #boton_ver.clicked.connect(lambda checked,x=tutores: self.read_student(x))
            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(lambda checked,x=tutores: self.edit_student(x))
            btn_borrar = QPushButton("Borrar")
            btn_borrar.clicked.connect(lambda checked,x=tutores: self.delete_student(x))

            btn_editar.setStyleSheet("background-color: #4CAF50; color: white;") 
            btn_borrar.setStyleSheet("background-color: #f44336; color: white;")                 
            boton_ver.setStyleSheet("background-color: #3d8ec9; color: white; font-weight: bold;") 

            layout_botones.addWidget(boton_ver)
            layout_botones.addWidget(btn_editar)
            layout_botones.addWidget(btn_borrar)

            # 6. Insertar el contenedor en la celda
            tabla.setCellWidget(fila, 8, widget_contenedor)
        # Esto elimina todas las filas, pero DEJA los títulos de las columnas intactos.

    def get_data(self,offset_count,search=""):
             
        if self.window.comboEmpresas.currentText()=="Todas las Empresas":
            return select(Tutor_Empresarial).where(
                                        or_(
                                            Tutor_Empresarial.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Empresarial.primer_apellido.ilike(f"{search}%")
                                        )
                                        ).limit(self.tamano_pagina).offset(offset_count)
        else:
            return select(Tutor_Empresarial).where(
                                        and_(
                                        Tutor_Empresarial.empresa.razon_social==self.window.comboEmpresas.currentText(),
                                        or_(
                                            Tutor_Empresarial.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Empresarial.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
                                        ).limit(self.tamano_pagina).offset(offset_count)
            
    def get_data_all(self,search=""):
             
        if self.window.comboEmpresas.currentText()=="Todas las Empresas":
            return select(Tutor_Empresarial).where(
                                        or_(
                                            Tutor_Empresarial.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Empresarial.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
        else:
            return select(Tutor_Empresarial).where(
                                        and_(
                                        Tutor_Empresarial.empresa.razon_social==self.window.comboEmpresas.currentText(),
                                        or_(
                                            Tutor_Empresarial.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Empresarial.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
                                        )

    def search(self):
        self.numero_pagina=1
        self.window.btnIndTutorE.setText(str(self.numero_pagina))
        search_query=self.window.searchTutorE.text()
        self.pag_tabla_tutorE(search_query)
            
    def change_table(self,buttom):
        
        if buttom.lower()=="anterior":
            self.numero_pagina=self.numero_pagina-1 if self.numero_pagina>1 else 1
        elif buttom.lower()=="siguiente":
            self.numero_pagina+=1
        self.window.btnIndTutorE.setText(str(self.numero_pagina))
        search_query=self.window.searchTutorA.text()
        self.pag_tabla_tutorE(search_query)
            
    """def read_student(self,estudiante):
        self.window.nombresLabel.clear()
        self.window.nombresLabel.setText(estudiante.primer_nombre+" "+estudiante.segundo_nombre if estudiante.segundo_nombre else estudiante.primer_nombre)
        self.window.apellidosLabel.clear()
        self.window.apellidosLabel.setText(estudiante.primer_apellido+" "+estudiante.segundo_apellido if estudiante.segundo_apellido else estudiante.primer_apellido)
        self.window.cedulaInput.clear()
        self.window.cedulaInput.setText(str(estudiante.cedula))
        self.window.telefonoInput.clear()
        self.window.telefonoInput.setText(str(estudiante.telefono))
        self.window.direccionInput.setPlainText(str(estudiante.direccion))
        self.window.StackedEstudiantes.setCurrentIndex(1)
        self.window.perfil_input.setPixmap(convertir_pil_a_pixmap(estudiante.foto))
        self.window.pushButton.clicked.connect(lambda: reemplazar_texto(estudiante))"""
    
    def edit_student(self,tutor):
        from admin.nuevo_tutorE import NewTutorE
        self.newtutor_window=NewTutorE(tutor)
        self.newtutor_window.exec()
        self.pag_tabla_tutorE()
        
    def open_newtutor(self):
        from admin.nuevo_tutorE import NewTutorE
        self.newtutor_window=NewTutorE()
        self.newtutor_window.exec()
        self.pag_tabla_tutorE()

    def delete_student(self,tutor):
        msg = ModernMessageBox(
                title="Advertencia",
                text="<h3 style='color: #ff5555'>Eliminar Estudiante</h3>",
                informative_text="¿Esta seguro de eliminar esta información?",
                parent=self
            )

        btn_save, btn_cancel = msg.add_custom_buttons()
            
            # Ejecutamos el diálogo (Modal loop)
        msg.exec()

        # Verificamos qué botón fue presionado
        clicked = msg.clickedButton()
        
        if clicked == btn_save:
            session.delete(tutor)
            session.commit()
            self.pag_tabla_tutorE()
            
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
                stmt=self.get_data_all(self.window.searchTutorE.text())
                exportar_modelo_a_excel(session.scalars(stmt).all(),archivo)
                
                QMessageBox.information(self.main, "Éxito", "La base de datos se exportó correctamente.")
            except Exception as e:
                QMessageBox.critical(self.main, "Error", f"No se pudo exportar: {str(e)}")



        
    