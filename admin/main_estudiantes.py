
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
from modelos.modulo import User,TSession,session,Student,Pasantia
from sqlalchemy import select
from sqlalchemy import or_,and_
from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from herramientas.modern_messagebox import ModernMessageBox
from herramientas.exports import exportar_modelo_a_excel
from herramientas.variables import semestre
from herramientas.conversiones import null_string,convertir_pil_a_pixmap
from dotenv import load_dotenv
from herramientas.docs import reemplazar_texto
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent,QSize

class StackStudent():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.StackedEstudiantes.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.window.frame_TablaStudent.installEventFilter(main)
        self.conectar_eventos()
    
    def eventFilter(self,source,event):
        
        if source == self.window.frame_TablaStudent and event.type() == QEvent.Type.Resize:
            self.header()
            height=self.window.tabla_estudiantes.height()
            self.tamano_pagina=int(height/25.4)
            self.pag_tabla_estudiantes()
            print("Ejecutando Estudiante")                   
            
    def conectar_eventos(self):
        self.window.btnExportar.clicked.connect(self.exportar)
        self.window.nuevostudentButton.clicked.connect(self.open_newstudent)
        self.window.btnAnt.clicked.connect(lambda :self.change_table("Anterior"))
        self.window.btnSig.clicked.connect(lambda :self.change_table("Siguiente"))
        self.window.searchStudent.textChanged.connect(self.search)
        self.window.comboCarreras.activated.connect(lambda: self.cambio_programa())
        
        
        if not self.window.searchStudent.actions(): 
            icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "search.svg"
            
            if icon_path.exists():
                search_icon = QIcon(str(icon_path))
            else:
                # Fallback al icono estándar si no encuentra el archivo
                search_icon = self.window.searchStudent.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            
            # Solo agregamos la acción si no existía ninguna
            self.search_icon = self.window.searchStudent.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
                     
   
    def cambio_programa(self):
        self.numero_pagina=1
        self.window.btnInd.setText(str(self.numero_pagina))
        self.pag_tabla_estudiantes()
    
    def header(self):
        
        header=self.window.tabla_estudiantes.horizontalHeader()
        header_vertical = self.window.tabla_estudiantes.verticalHeader()
        header_vertical.setDefaultSectionSize(30)
        #cedula
        self.window.tabla_estudiantes.setColumnWidth(0, 80)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        #nombres
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        #email
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        #tlf
        self.window.tabla_estudiantes.setColumnWidth(6, 100)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        #accion
        self.window.tabla_estudiantes.setColumnWidth(7, 300)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        
        if self.window.tabla_estudiantes.width()>1600:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        
        
        self.window.tabla_estudiantes.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.window.tabla_estudiantes.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def pag_tabla_estudiantes(self,search=""):
        offset_count = (self.numero_pagina - 1) * self.tamano_pagina
        stmt = self.get_data_students(offset_count,search)
        estudiantes=session.scalars(stmt).all()
        
        tabla=self.window.tabla_estudiantes
        if not estudiantes and tabla.rowCount():
            QMessageBox.warning(self.window, "Aviso", "Busqueda no encontrada")
            return
        if len(estudiantes)<15:
           self.window.btnSig.setEnabled(False)
        else:
            self.window.btnSig.setEnabled(True)
        tabla.setRowCount(0)
        for fila,estudiante in enumerate(estudiantes):
            tabla.insertRow(fila)
            
            tabla.setItem(fila,0,QTableWidgetItem(str(estudiante.cedula)))
            tabla.setItem(fila,1,QTableWidgetItem(str(estudiante.primer_nombre)))
            tabla.setItem(fila,2,QTableWidgetItem(str(estudiante.segundo_nombre if estudiante.segundo_nombre else "")))
            tabla.setItem(fila,3,QTableWidgetItem(str(estudiante.primer_apellido)))
            tabla.setItem(fila,4,QTableWidgetItem(estudiante.segundo_apellido if estudiante.segundo_apellido else ""))
            tabla.setItem(fila,5,QTableWidgetItem(str(estudiante.email)))
            tabla.setItem(fila,6,QTableWidgetItem(str(estudiante.telefono)))
                       
            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 

            boton_ver=QPushButton("Ver")
            boton_ver.setIcon(QIcon("resources/images/read-svgrepo-com.svg"))
            boton_ver.setIconSize(QSize(15, 15))
            boton_ver.clicked.connect(lambda checked,x=estudiante: self.read_student(x))
            btn_editar = QPushButton("Editar")
            btn_editar.setIcon(QIcon("resources/images/edit-2-svgrepo-com.svg"))
            btn_editar.setIconSize(QSize(15, 15))
            btn_editar.clicked.connect(lambda checked,x=estudiante: self.edit_student(x))
            btn_borrar = QPushButton("Eliminar")
            btn_borrar.setIcon(QIcon("resources/images/delete-1487-svgrepo-com.svg"))
            btn_borrar.setIconSize(QSize(15, 15))
            btn_borrar.clicked.connect(lambda checked,x=estudiante: self.delete_student(x))

            btn_editar.setStyleSheet("background-color: #4CAF50; color: white;") 
            btn_borrar.setStyleSheet("background-color: #f44336; color: white;")                 
            boton_ver.setStyleSheet("background-color: #3d8ec9; color: white; font-weight: bold;") 

            layout_botones.addWidget(boton_ver)
            layout_botones.addWidget(btn_editar)
            layout_botones.addWidget(btn_borrar)

            # 6. Insertar el contenedor en la celda
            tabla.setCellWidget(fila, 7, widget_contenedor)
        # Esto elimina todas las filas, pero DEJA los títulos de las columnas intactos.

    def get_data_students(self,offset_count,search=""):
             
        if self.window.comboCarreras.currentText()=="Todas las Carreras":
            return select(Student).where(
                                        or_(
                                            Student.primer_nombre.ilike(f"{search}%"),
                                            Student.primer_apellido.ilike(f"{search}%")
                                        )
                                        ).distinct().limit(self.tamano_pagina).offset(offset_count)
        else:
            return select(Student).join(
                                        Student.pasantias).where(
                                        Student.primer_nombre.ilike(f"%{search}%")).where(      
                                        Pasantia.carrera == self.window.comboCarreras.currentText()).distinct().limit(self.tamano_pagina).offset(offset_count)
            
    def get_data_students_all(self,search=""):
             
        if self.window.comboCarreras.currentText()=="Todas las Carreras" :
            return select(Student).where(
                                        or_(
                                            Student.primer_nombre.ilike(f"{search}%"),
                                            Student.primer_apellido.ilike(f"{search}%")
                                        )
                                        ).distinct()
        else:
            return select(Student).join(
                                        Student.pasantias).where(
                                        Student.primer_nombre.ilike(f"%{search}%")).where(      
                                        Pasantia.carrera == self.window.comboCarreras.currentText()).distinct()

    def search(self):
        self.numero_pagina=1
        self.window.btnInd.setText(str(self.numero_pagina))
        search_query=self.window.searchStudent.text()
        self.pag_tabla_estudiantes(search_query)
            
    def change_table(self,buttom):
        
        if buttom.lower()=="anterior":
            self.numero_pagina=self.numero_pagina-1 if self.numero_pagina>1 else 1
        elif buttom.lower()=="siguiente":
            self.numero_pagina+=1
        self.window.btnInd.setText(str(self.numero_pagina))
        search_query=self.window.searchStudent.text()
        self.pag_tabla_estudiantes(search_query)
            
    def read_student(self,estudiante:Student):
        self.window.nombresLabel.clear()
        self.window.nombresLabel.setText(estudiante.primer_nombre+" "+null_string(estudiante.segundo_nombre)+" "+estudiante.primer_apellido+" "+null_string(estudiante.segundo_apellido))
        self.window.sexoLabelSt.clear()
        self.window.sexoLabelSt.setText(estudiante.sexo)
        self.window.cedulaSt_input.clear()
        self.window.cedulaSt_input.setText(estudiante.sexo)
        self.window.cedulaSt_input.clear()
        self.window.cedulaSt_input.setText(str(estudiante.cedula))
        self.window.fnacimientoSt.clear()
        self.window.fnacimientoSt.setText(str(estudiante.fecha_de_nacimiento))
        self.window.telefonoInput.clear()
        self.window.telefonoInput.setText(str(estudiante.telefono))
        self.window.emailSt.clear()
        self.window.emailSt.setText(estudiante.email)
        self.window.direccionSt.clear()
        self.window.direccionSt.setText(estudiante.direccion)
        self.window.perfil_St_input.setPixmap(convertir_pil_a_pixmap(estudiante.foto))
        self.tabla_Stpasantia(estudiante)
        self.window.StackedEstudiantes.setCurrentIndex(1)
        self.window.EliminarSt.clicked.connect(lambda: self.delete_student(estudiante))
        self.window.editarSt.clicked.connect(lambda: self.edit_student(estudiante))
        self.window.regresarButtonSt.clicked.connect(lambda: self.window.StackedEstudiantes.setCurrentIndex(0))
    
    def tabla_Stpasantia(self,estudiante:Student):
        pasantia=estudiante.pasantias
        tabla=self.window.tableStPasantia
        header=tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        tabla.setRowCount(0)
        for fila,pasante in enumerate(pasantia):
            tabla.insertRow(fila)
            
            tabla.setItem(fila,0,QTableWidgetItem(str(pasante.carrera)))
            tabla.setItem(fila,1,QTableWidgetItem(str(pasante.semestre)))
            tabla.setItem(fila,2,QTableWidgetItem(str(pasante.lapso_academico)))
            tabla.setItem(fila,3,QTableWidgetItem(str(pasante.estado)))

        
        
    
    def edit_student(self,estudiante):
        from admin.nuevo_estudiante import NewStudent
        self.newstudent_window=NewStudent(self.main.user_authenticated,estudiante)
        self.newstudent_window.exec()
        self.pag_tabla_estudiantes()
        
    def open_newstudent(self):
        from admin.nuevo_estudiante import NewStudent
        self.newstudent_window=NewStudent(self.main.user_authenticated)
        self.newstudent_window.exec()
        self.pag_tabla_estudiantes()

    def delete_student(self,estudiante):
        msg = ModernMessageBox(
                title="Advertencia",
                text="<h3 style='color: #ff5555'>Eliminar Estudiante</h3>",
                informative_text="¿Esta seguro de eliminar esta información?",
                parent=self.window
            )

        btn_save, btn_cancel = msg.add_custom_buttons()
            
            # Ejecutamos el diálogo (Modal loop)
        msg.exec()

        # Verificamos qué botón fue presionado
        clicked = msg.clickedButton()
        
        if clicked == btn_save:
            session.delete(estudiante)
            session.commit()
            self.pag_tabla_estudiantes()
            
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
                stmt=self.get_data_students_all(self.window.searchStudent.text())
                exportar_modelo_a_excel(session.scalars(stmt).all(),archivo)
                
                QMessageBox.information(self.main, "Éxito", "La base de datos se exportó correctamente.")
            except Exception as e:
                QMessageBox.critical(self.main, "Error", f"No se pudo exportar: {str(e)}")



        
    