
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QHBoxLayout,QStyle,QLineEdit,QAbstractScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon
from PySide6.QtUiTools import QUiLoader
from modelos.modulo import session,Tutor_Empresarial,Enterprise,Pasantia
from sqlalchemy import select
from sqlalchemy import or_,and_
from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from herramientas.modern_messagebox import ModernMessageBox
from herramientas.exports import exportar_modelo_a_excel
from herramientas.variables import semestre
from dotenv import load_dotenv
from herramientas.docs import reemplazar_texto
from herramientas.conversiones import convertir_pil_a_pixmap
from herramientas.conversiones import calcular_edad,nombreCompleto
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent

class StackTutorE():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.StackedTutorA.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.window.tabla_TutorE.installEventFilter(main)
        self.tabla_pasantes=self.window.tabla_PTE
        self.conectar_eventos()
    
    def offset_count(self):
        return (self.numero_pagina - 1) * self.tamano_pagina
        
    def eventFilter(self,source,event):
        
        if source == self.window.tabla_TutorE and event.type() == QEvent.Type.Resize:
            height=self.window.tabla_TutorE.height()
            self.tamano_pagina=int(height/25.4)
            self.pag_tabla_tutorE()
            print("Ejecutando Tutores Empresariales")                   
    def listas(self):
        self.window.comboEmpresas.clear()
        empresas=session.scalars(select(Enterprise)).all()
        self.window.comboEmpresas.addItem('Todas las Empresas',None)
        for i in empresas:
            self.window.comboEmpresas.addItem(i.razon_social,i.id)    
    
            
    def conectar_eventos(self):
        self.listas()
        self.window.btnExportarTutorE.clicked.connect(self.exportar)
        self.window.btnNuevoTutorE.clicked.connect(self.open_newtutor)
        self.window.btnAntTutorE.clicked.connect(lambda :self.change_table("Anterior"))
        self.window.btnSigTutorE.clicked.connect(lambda :self.change_table("Siguiente"))
        self.window.searchTutorE.textChanged.connect(self.search)
        self.window.comboEmpresas.activated.connect(lambda: self.cambio_programa())
   
        if not self.window.searchTutorE.actions(): 
            icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "search.svg"
            
            if icon_path.exists():
                search_icon = QIcon(str(icon_path))
            else:
              
                search_icon = self.window.searchTutorE.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            
            self.search_icon = self.window.searchTutorE.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)

    def indice(self):
        ind1=1+self.offset_count()
        ind2=self.numero_pagina*self.tamano_pagina
        self.window.btnIndTutorE.setText(f"{ind1}-{ind2 if ind2<self.all_data else self.all_data} de {self.all_data}")
                         
    def cambio_programa(self):
        self.numero_pagina=1
        self.pag_tabla_tutorE()
    
    def header(self):
        
        header=self.window.tabla_TutorE.horizontalHeader()
        header_vertical = self.window.tabla_TutorE.verticalHeader()
        header_vertical.setDefaultSectionSize(30)
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
        
    def pag_tabla_tutorE(self):
        self.header()
        tutores=self.get_data()
        tabla=self.window.tabla_TutorE
        if not tutores and tabla.rowCount():
            QMessageBox.warning(self.window, "Aviso", "Busqueda no encontrada")
            return
        if (self.all_data-self.offset_count())<=self.tamano_pagina:
           self.window.btnSigTutorE.setEnabled(False)
        else:
            self.window.btnSigTutorE.setEnabled(True)

        self.indice()
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

            boton_ver=QPushButton("")
            boton_ver.clicked.connect(lambda checked,x=tutores: self.read_tutor(x))
            btn_editar = QPushButton("")
            btn_editar.clicked.connect(lambda checked,x=tutores: self.edit_tutor(x))
            btn_borrar = QPushButton("")
            btn_borrar.clicked.connect(lambda checked,x=tutores: self.delete_tutor(x))

            btn_editar.setStyleSheet("""QPushButton{background-color: transparent;
                                        border:none;
                                        qproperty-icon: url(resources/images/edit-2-svgrepo-com-blue.svg);
                                        qproperty-iconSize: 20px 20px;}
                                        
                                        QPushButton:hover{
                                        background-color: #808080;
                                        }""") 
            btn_borrar.setStyleSheet("""QPushButton{background-color: transparent;
                                        border:none;
                                        qproperty-icon: url(resources/images/delete-1487-svgrepo-comR.svg);
                                        qproperty-iconSize: 20px 20px;}
                                        
                                        QPushButton:hover{
                                        
                                        background-color: #808080;
                                        }""")                 
            boton_ver.setStyleSheet("""QPushButton{background-color: transparent;
                                        border:none;
                                        qproperty-icon: url(resources/images/read-svgrepo-com.svg);
                                        qproperty-iconSize: 20px 20px;}
                                        
                                        QPushButton:hover{
                                        background-color: #808080;
                                        }""") 

            layout_botones.addWidget(boton_ver)
            if self.main.user_authenticated.rol=="Administrador":
                layout_botones.addWidget(btn_editar)
                layout_botones.addWidget(btn_borrar)

            # 6. Insertar el contenedor en la celda
            tabla.setCellWidget(fila, 8, widget_contenedor)
        # Esto elimina todas las filas, pero DEJA los títulos de las columnas intactos.

    def get_data(self):
        search=self.window.searchTutorE.text()
        self.all_data=len(self.get_data_all())      
        if not self.window.comboEmpresas.currentData():
            stmt=select(Tutor_Empresarial).where(
                                        or_(
                                            Tutor_Empresarial.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Empresarial.primer_apellido.ilike(f"{search}%")
                                        )
                                        )#.limit(self.tamano_pagina).offset(offset_count)
        else:
            stmt=select(Tutor_Empresarial).where(
                                        and_(
                                        Tutor_Empresarial.id_empresa==self.window.comboEmpresas.currentData(),
                                        or_(
                                            Tutor_Empresarial.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Empresarial.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
                                        )#.limit(self.tamano_pagina).offset(offset_count)
        return session.scalars(stmt.limit(self.tamano_pagina).offset(self.offset_count())).all()
            
    def get_data_all(self):
        search=self.window.searchTutorE.text()
        if not self.window.comboEmpresas.currentData():
            stmt=select(Tutor_Empresarial).where(
                                        or_(
                                            Tutor_Empresarial.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Empresarial.primer_apellido.ilike(f"{search}%")
                                        )
                                        )#.limit(self.tamano_pagina).offset(offset_count)
        else:
            stmt=select(Tutor_Empresarial).where(
                                        and_(
                                        Tutor_Empresarial.id_empresa==self.window.comboEmpresas.currentData(),
                                        or_(
                                            Tutor_Empresarial.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Empresarial.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
                                        )#.limit(self.tamano_pagina).offset(offset_count)
        return session.scalars(stmt).all()

    def search(self):
        self.numero_pagina=1
        self.pag_tabla_tutorE()
            
    def change_table(self,buttom):
        
        if buttom.lower()=="anterior":
            self.numero_pagina=self.numero_pagina-1 if self.numero_pagina>1 else 1
        elif buttom.lower()=="siguiente":
            self.numero_pagina+=1
        self.pag_tabla_tutorE()
            
    def read_tutor(self,tutor:Tutor_Empresarial):
        self.window.empresaE.clear()
        self.window.empresaE.setText(tutor.empresa.razon_social)
        self.window.nombre_completoE.clear()
        self.window.nombre_completoE.setText(nombreCompleto(tutor))
        self.window.cedulaE.clear()
        self.window.cedulaE.setText(str(tutor.cedula))
        self.window.sexEdadE.clear()
        self.window.sexEdadE.setText(str(tutor.sexo)+" • "+str(calcular_edad(tutor.fecha_de_nacimiento)))
        self.window.emailE.clear()
        self.window.emailE.setText(tutor.email)
        self.window.tlfE.clear()
        self.window.tlfE.setText(tutor.telefono)
        self.window.cargoE.clear()
        self.window.cargoE.setText(tutor.cargo)
        self.window.fechaNE.clear()
        self.window.fechaNE.setText(tutor.fecha_de_nacimiento.isoformat())
        self.window.StackedTutorE.setCurrentIndex(1)
        self.window.perfil_E.setPixmap(convertir_pil_a_pixmap(tutor.foto))
        if self.main.user_authenticated.rol=="Coordinador":
            self.window.editarE.setHidden(True)
            self.window.EliminarE.setHidden(True)
        self.window.editarE.clicked.connect(lambda: self.edit_tutor(tutor))
        self.window.EliminarE.clicked.connect(lambda: self.delete_tutor(tutor))
        self.window.regresarButtonTE.clicked.connect(lambda: self.window.StackedTutorE.setCurrentIndex(0))
        self.pag_tabla_pasantes(tutor.pasantias)

   
    def pag_tabla_pasantes(self,entidad):
        header=self.tabla_pasantes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_pasantes.setRowCount(0)
        self.tabla_pasantes.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tabla_pasantes.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for fila,pasante in enumerate(entidad[inicio:final]):
            pasante:Pasantia
            self.tabla_pasantes.insertRow(fila)
            
            self.tabla_pasantes.setItem(fila,0,QTableWidgetItem(str(nombreCompleto(pasante.student))))
            self.tabla_pasantes.setItem(fila,1,QTableWidgetItem(str(pasante.student.cedula)))
            self.tabla_pasantes.setItem(fila,2,QTableWidgetItem(str(pasante.carrera)))
            self.tabla_pasantes.setItem(fila,3,QTableWidgetItem(str(pasante.lapso_academico)))
            self.tabla_pasantes.setItem(fila,4,QTableWidgetItem(str(pasante.estado)))
            
            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 

            boton_ver=QPushButton("Ver")
            boton_ver.clicked.connect(lambda checked,x=pasante: read_pasante(x))
            boton_ver.setStyleSheet("background-color: #3d8ec9; color: white; font-weight: bold;") 
            
            layout_botones.addWidget(boton_ver)
            self.tabla_pasantes.setCellWidget(fila, 5, widget_contenedor)
        def read_pasante(pasante:Pasantia):
            if self.main.user_authenticated.rol=="Administrador":
                self.window.PasantiasButton.click()
                self.main.pasante.read_pasante(pasante)
            else:
                self.window.btnPasante.click()
                self.main.pasante.datos(pasante)
                
        
    def edit_tutor(self,tutor):
        from admin.nuevo_tutorE import NewTutorE
        self.newtutor_window=NewTutorE(tutor)
        self.newtutor_window.exec()
        self.pag_tabla_tutorE()
        
    def open_newtutor(self):
        from admin.nuevo_tutorE import NewTutorE
        self.newtutor_window=NewTutorE()
        self.newtutor_window.exec()
        self.pag_tabla_tutorE()

    def delete_tutor(self,tutor):
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
                exportar_modelo_a_excel(self.get_data_all(),archivo,Tutor_Empresarial)
                
                QMessageBox.information(self.main, "Éxito", "La base de datos se exportó correctamente.")
            except Exception as e:
                QMessageBox.critical(self.main, "Error", f"No se pudo exportar: {str(e)}")



        
    