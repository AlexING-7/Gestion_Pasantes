
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QHBoxLayout,QStyle,QLineEdit,QAbstractScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon
from PySide6.QtUiTools import QUiLoader

from modelos.modulo import session,Enterprise
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

class StackEnterprise():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.StackedEmpresas.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.window.frame_TablaEmpresa.installEventFilter(main)
        self.conectar_eventos()
    
    def eventFilter(self,source,event):
        
        if source == self.window.frame_TablaEmpresa and event.type() == QEvent.Type.Resize:
            self.header()
            height=self.window.tabla_Empresas.height()
            self.tamano_pagina=int(height/25.4)
            self.pag_tabla_empresa()
            print("Ejecutando Empresa")                   
            
    def conectar_eventos(self):
        self.window.btnExportarEmpr.clicked.connect(self.exportar)
        self.window.btnNuevaEmpr.clicked.connect(self.open_empresa)
        #self.window.regresarButton.clicked.connect(lambda :self.window.StackedEstudiantes.setCurrentIndex(0))
        self.window.btnAntEmpr.clicked.connect(lambda :self.change_table(self.window.btnAntEmpr.text()))
        self.window.btnSigEmpr.clicked.connect(lambda :self.change_table(self.window.btnSigEmpr.text()))
        self.window.searchEmpr.textChanged.connect(self.search)
        self.window.comboRubros.activated.connect(lambda: self.cambio_programa())
                
        if not self.window.searchEmpr.actions(): 
            icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "search.svg"
            if icon_path.exists():
                search_icon = QIcon(str(icon_path))
            else:
                search_icon = self.window.searchEmpr.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            self.search_icon = self.window.searchEmpr.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
                     
    def ver_estudiantes(self):
        self.window.StackedEmpresas.setCurrentIndex(1)
    
    def cambio_programa(self):
        self.numero_pagina=1
        self.window.btnIndEmpr.setText(str(self.numero_pagina))
        self.pag_tabla_empresa()
    
    def header(self):
        
        header=self.window.tabla_Empresas.horizontalHeader()
        #RIF
        self.window.tabla_Empresas.setColumnWidth(0, 80)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        #Razon social
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        #email
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        #tlf
        self.window.tabla_Empresas.setColumnWidth(3, 100)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        #accion
        self.window.tabla_Empresas.setColumnWidth(4, 150)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        
        if self.window.tabla_Empresas.width()>1600:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)       
        
        self.window.tabla_Empresas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.window.tabla_Empresas.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def pag_tabla_empresa(self,search=""):
        offset_count = (self.numero_pagina - 1) * self.tamano_pagina
        stmt = self.get_data(offset_count,search)
        empresas=session.scalars(stmt).all()
        tabla=self.window.tabla_Empresas
        if not empresas and tabla.rowCount():
            QMessageBox.warning(self.window, "Aviso", "Busqueda no encontrada")
            return
        if len(empresas)<15:
           self.window.btnSigEmpr.setEnabled(False)
        else:
            self.window.btnSigEmpr.setEnabled(True)
        tabla.setRowCount(0)
        for fila,empresa in enumerate(empresas):
            tabla.insertRow(fila)
            
            tabla.setItem(fila,0,QTableWidgetItem(str(empresa.rif)))
            tabla.setItem(fila,1,QTableWidgetItem(str(empresa.razon_social)))
            tabla.setItem(fila,2,QTableWidgetItem(str(empresa.email)))
            tabla.setItem(fila,3,QTableWidgetItem(str(empresa.telefono)))
                       
            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 

            boton_ver=QPushButton("Ver")
            #boton_ver.clicked.connect(lambda checked,x=estudiante: self.read_student(x))
            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(lambda checked,x=empresa: self.edit_empresa(x))
            btn_borrar = QPushButton("Borrar")
            btn_borrar.clicked.connect(lambda checked,x=empresa: self.delete_empresa(x))

            btn_editar.setStyleSheet("background-color: #4CAF50; color: white;") 
            btn_borrar.setStyleSheet("background-color: #f44336; color: white;")                 
            boton_ver.setStyleSheet("background-color: #3d8ec9; color: white; font-weight: bold;") 

            layout_botones.addWidget(boton_ver)
            layout_botones.addWidget(btn_editar)
            layout_botones.addWidget(btn_borrar)

            # 6. Insertar el contenedor en la celda
            tabla.setCellWidget(fila, 4, widget_contenedor)
        # Esto elimina todas las filas, pero DEJA los títulos de las columnas intactos.

    def get_data(self,offset_count,search=""):
             
        if self.window.comboRubros.currentText()=="Todos los Rubros":
            return select(Enterprise).where(
                                        or_(
                                            Enterprise.rif.ilike(f"{search}%"),
                                            Enterprise.razon_social.ilike(f"{search}%")
                                        )
                                        ).limit(self.tamano_pagina).offset(offset_count)
        else:
            return select(Enterprise).where(
                                        and_(
                                        Enterprise.rubro==self.window.comboRubros.currentText(),
                                        or_(
                                            Enterprise.rif.ilike(f"{search}%"),
                                            Enterprise.razon_social.ilike(f"{search}%")
                                        )
                                        )
                                        ).limit(self.tamano_pagina).offset(offset_count)
            
    def get_data_all(self,search=""):
             
        if self.window.comboRubros.currentText()=="Todos los Rubros":
            return select(Enterprise).where(
                                        or_(
                                            Enterprise.rif.ilike(f"{search}%"),
                                            Enterprise.razon_social.ilike(f"{search}%")
                                        )
                                        )
        else:
            return select(Enterprise).where(
                                        and_(
                                        Enterprise.rubro==self.window.comboRubros.currentText(),
                                        or_(
                                            Enterprise.rif.ilike(f"{search}%"),
                                            Enterprise.razon_social.ilike(f"{search}%")
                                        )
                                        )
                                        )

    def search(self):
        self.numero_pagina=1
        self.window.btnIndEmpr.setText(str(self.numero_pagina))
        search_query=self.window.searchEmpr.text()
        self.pag_tabla_empresa(search_query)
            
    def change_table(self,buttom):
        
        if buttom.lower()=="anterior":
            self.numero_pagina=self.numero_pagina-1 if self.numero_pagina>1 else 1
        elif buttom.lower()=="siguiente":
            self.numero_pagina+=1
        self.window.btnIndEmpr.setText(str(self.numero_pagina))
        search_query=self.window.searchEmpr.text()
        self.pag_tabla_empresa(search_query)
            
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
        self.window.pushButton.clicked.connect(lambda: reemplazar_texto(estudiante))
    """
    
    def edit_empresa(self,empresa):
        from admin.nuevo_empresa import NewEnterprise
        self.newempr_window=NewEnterprise(empresa)
        self.newempr_window.exec()
        self.pag_tabla_empresa()
        
    def open_empresa(self):
        from admin.nuevo_empresa import NewEnterprise
        self.newempr_window=NewEnterprise()
        self.newempr_window.exec()
        self.pag_tabla_empresa()

    def delete_empresa(self,dato):
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
            session.delete(dato)
            session.commit()
            self.pag_tabla_empresa()
            
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
                stmt=self.get_data_all(self.window.searchEmpr.text())
                exportar_modelo_a_excel(session.scalars(stmt).all(),archivo)
                
                QMessageBox.information(self.main, "Éxito", "La base de datos se exportó correctamente.")
            except Exception as e:
                QMessageBox.critical(self.main, "Error", f"No se pudo exportar: {str(e)}")



        
    