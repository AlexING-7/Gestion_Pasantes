
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QHBoxLayout,QStyle,QLineEdit,QAbstractScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon
from modelos.modulo import session,Student,Tutor_Academico,Pasantia
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
from herramientas.conversiones import nombreCompleto,calcular_edad
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent

class StackTutorA():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.StackedTutorA.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.tabla_pasantes=self.window.tabla_PTA
        self.window.frame_tutorA.installEventFilter(main)
        self.conectar_eventos()
    
    def offset_count(self):
        return (self.numero_pagina - 1) * self.tamano_pagina
    
    def eventFilter(self,source,event):  
        if source == self.window.frame_tutorA and event.type() == QEvent.Type.Resize:
            height=self.window.tabla_TutorA.height()
            self.tamano_pagina=int(height/25.4)
            self.pag_tabla_tutorA()
            print("Ejecutando Tutores Academicos")                   
    def listas(self):
        self.window.comboEspecialidad.clear()
        especialidades=session.scalars(select(Tutor_Academico.especialidad)).all()
        self.window.comboEspecialidad.addItem('Todas las Especialidades',None)
        for i in set(especialidades):
            self.window.comboEspecialidad.addItem(i,i)       
    def conectar_eventos(self):
        self.listas()
        self.window.btnExportarTutorA.clicked.connect(self.exportar)
        self.window.btnNuevoTutorA.clicked.connect(self.open_newtutor)
        #self.window.regresarButton.clicked.connect(lambda :self.window.StackedEstudiantes.setCurrentIndex(0))
        self.window.btnAntTutorA.clicked.connect(lambda :self.change_table("Anterior"))
        self.window.btnSigTutorA.clicked.connect(lambda :self.change_table("Siguiente"))
        self.window.searchTutorA.textChanged.connect(self.search)
        self.window.comboEspecialidad.activated.connect(lambda: self.cambio_programa())

        
        
        if not self.window.searchTutorA.actions(): 
            icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "search.svg"
            
            if icon_path.exists():
                search_icon = QIcon(str(icon_path))
            else:
                # Fallback al icono estándar si no encuentra el archivo
                search_icon = self.window.searchTutorA.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            
            # Solo agregamos la acción si no existía ninguna
            self.search_icon = self.window.searchTutorA.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
    
    def indice(self):
        ind1=1+self.offset_count()
        ind2=self.numero_pagina*self.tamano_pagina
        self.window.btnIndTutorA.setText(f"{ind1}-{ind2 if ind2<self.all_data else self.all_data} de {self.all_data}")
                
    def cambio_programa(self):
        self.numero_pagina=1
        self.pag_tabla_tutorA()
    
    def header(self):
        
        header=self.window.tabla_TutorA.horizontalHeader()
        header_vertical = self.window.tabla_TutorA.verticalHeader()
        header_vertical.setDefaultSectionSize(30)
        #cedula
        self.window.tabla_TutorA.setColumnWidth(0, 80)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        #nombres
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        #email
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        #tlf
        self.window.tabla_TutorA.setColumnWidth(6, 100)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        #accion
        self.window.tabla_TutorA.setColumnWidth(7, 150)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        
        if self.window.tabla_TutorA.width()>1600:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        
        
        self.window.tabla_TutorA.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.window.tabla_TutorA.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def pag_tabla_tutorA(self):
        self.header()
        tutores = self.get_data()
        tabla=self.window.tabla_TutorA
        if not tutores and tabla.rowCount():
            QMessageBox.warning(self.window, "Aviso", "Busqueda no encontrada")
            return
        if (self.all_data-self.offset_count())<=self.tamano_pagina:
           self.window.btnSigTutorA.setEnabled(False)
        else:
            self.window.btnSigTutorA.setEnabled(True)

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
            tabla.setCellWidget(fila, 7, widget_contenedor)
        # Esto elimina todas las filas, pero DEJA los títulos de las columnas intactos.

    def get_data(self):
        search=self.window.searchTutorA.text()  
        self.all_data=len(self.get_data_all())   
        if not self.window.comboEspecialidad.currentData():
            stmt=select(Tutor_Academico).where(
                                        or_(
                                            Tutor_Academico.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Academico.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
        else:
            stmt=select(Tutor_Academico).where(
                                        and_(
                                        Tutor_Academico.especialidad==self.window.comboEspecialidad.currentData(),
                                        or_(
                                            Tutor_Academico.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Academico.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
                                        )
        return session.scalars(stmt.limit(self.tamano_pagina).offset(self.offset_count())).all()
            
    def get_data_all(self):
        search=self.window.searchTutorA.text()        
        if not self.window.comboEspecialidad.currentData():
            stmt=select(Tutor_Academico).where(
                                        or_(
                                            Tutor_Academico.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Academico.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
        else:
            stmt=select(Tutor_Academico).where(
                                        and_(
                                        Tutor_Academico.especialidad==self.window.comboEspecialidad.currentData(),
                                        or_(
                                            Tutor_Academico.primer_nombre.ilike(f"{search}%"),
                                            Tutor_Academico.primer_apellido.ilike(f"{search}%")
                                        )
                                        )
                                        )
        return session.scalars(stmt).all()


    def search(self):
        self.numero_pagina=1      
        self.pag_tabla_tutorA()
            
    def change_table(self,buttom):       
        if buttom.lower()=="anterior":
            self.numero_pagina=self.numero_pagina-1 if self.numero_pagina>1 else 1
        elif buttom.lower()=="siguiente":
            self.numero_pagina+=1
        self.pag_tabla_tutorA()
            
    def read_tutor(self,tutor:Tutor_Academico):
        self.window.nombre_completoA.clear()
        self.window.nombre_completoA.setText(nombreCompleto(tutor))
        self.window.cedulaA.clear()
        self.window.cedulaA.setText(str(tutor.cedula))
        self.window.sexEdadA.clear()
        self.window.sexEdadA.setText(str(tutor.sexo)+" • "+str(calcular_edad(tutor.fecha_de_nacimiento)))
        self.window.emailA.clear()
        self.window.emailA.setText(tutor.email)
        self.window.tlfA.clear()
        self.window.tlfA.setText(tutor.telefono)
        self.window.especialidadA.clear()
        self.window.especialidadA.setText(tutor.especialidad)
        self.window.fechaNA.clear()
        self.window.fechaNA.setText(tutor.fecha_de_nacimiento.isoformat())
        self.window.StackedTutorA.setCurrentIndex(1)
        
        self.window.perfil_A.setPixmap(convertir_pil_a_pixmap(tutor.foto))
        if self.main.user_authenticated.rol=="Coordinador":
            self.window.editarA.setHidden(True)
            self.window.EliminarA.setHidden(True)
        
        self.window.editarA.clicked.connect(lambda: self.edit_tutor(tutor))
        self.window.EliminarA.clicked.connect(lambda: self.delete_tutor(tutor))
        self.window.regresarButtonTA.clicked.connect(lambda: self.window.StackedTutorA.setCurrentIndex(0))
        
        self.window.NumLogs_3.setText("1")
        self.elementos_por_pagina=2
        self.window.SigLogs_3.clicked.connect(lambda:self.cambiar_pagina(1,tutor.pasantias))
        self.window.AntLogs_3.clicked.connect(lambda:self.cambiar_pagina(-1,tutor.pasantias))
        self.pag_tabla_pasantes(tutor.pasantias[0:self.elementos_por_pagina])
        
    def cambiar_pagina(self, direccion: int, lista_datos: list):
        """
        Controla la paginación y actualiza la tabla de pasantes.
        
        :param direccion: 1 para Siguiente, -1 para Anterior.
        :param lista_datos: La lista completa de tutores.pasantias.
        """
        self.pagina_actual=int(self.window.NumLogs_3.text())
        # 1. Calcular el total de páginas
        total_elementos = len(lista_datos)
        total_paginas = (total_elementos + self.elementos_por_pagina - 1) // self.elementos_por_pagina

        # 2. Actualizar el índice de página actual con validación
        nueva_pagina = self.pagina_actual + direccion
        
        if nueva_pagina < 1:
            nueva_pagina = 1
        elif nueva_pagina > total_paginas:
            nueva_pagina = total_paginas

        # Si la página no cambió realmente (ej. ya estás en la 1), no hacemos nada
        if nueva_pagina == self.pagina_actual and total_elementos > 0:
            return

        self.pagina_actual = nueva_pagina
        self.window.NumLogs_3.setText(str(self.pagina_actual))

        # 3. Calcular los índices de rebanado (slice) para la lista
        # Ejemplo: Página 1 -> inicio 0, fin 10
        inicio = (self.pagina_actual - 1) * self.elementos_por_pagina
        fin = min(inicio + self.elementos_por_pagina, total_elementos)

        # 4. Obtener el subconjunto de datos
        datos_paginados = lista_datos[inicio:fin]

        # 5. Llamar a tu función existente para renderizar la tabla
        # Pasamos la entidad (datos recortados), y los índices para referencia visual
        self.pag_tabla_pasantes(datos_paginados)  
          
    def pag_tabla_pasantes(self,entidad):
        header=self.tabla_pasantes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_pasantes.setRowCount(0)
        self.tabla_pasantes.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tabla_pasantes.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for fila,pasante in enumerate(entidad):
            pasante:Pasantia
            self.tabla_pasantes.insertRow(fila)
            
            self.tabla_pasantes.setItem(fila,0,QTableWidgetItem(str(nombreCompleto(pasante.student))))
            self.tabla_pasantes.setItem(fila,1,QTableWidgetItem(str(pasante.student.cedula)))
            self.tabla_pasantes.setItem(fila,2,QTableWidgetItem(str(pasante.carrera)))
            self.tabla_pasantes.setItem(fila,3,QTableWidgetItem(str(pasante.empresa.razon_social)))
            self.tabla_pasantes.setItem(fila,4,QTableWidgetItem(str(pasante.lapso_academico)))
            self.tabla_pasantes.setItem(fila,5,QTableWidgetItem(str(pasante.estado)))

            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 

            boton_ver=QPushButton("Ver")
            boton_ver.clicked.connect(lambda checked,x=pasante: read_pasante(x))
            boton_ver.setStyleSheet("background-color: #3d8ec9; color: white; font-weight: bold;") 
            
            layout_botones.addWidget(boton_ver)
            self.tabla_pasantes.setCellWidget(fila, 6, widget_contenedor)
        def read_pasante(pasante:Pasantia):
            if self.main.user_authenticated.rol=="Administrador":
                self.window.PasantiasButton.click()
                self.main.pasante.read_pasante(pasante)
            else:
                self.window.btnPasante.click()
                self.main.pasante.datos(pasante)
    
    def edit_tutor(self,tutor):
        from admin.nuevo_tutorA import NewTutorA
        self.newtutor_window=NewTutorA(tutor)
        self.newtutor_window.exec()
        self.pag_tabla_tutorA()
        
    def open_newtutor(self):
        from admin.nuevo_tutorA import NewTutorA
        self.newtutor_window=NewTutorA()
        self.newtutor_window.exec()
        self.pag_tabla_tutorA()

    def delete_tutor(self,tutor):
        msg = ModernMessageBox(
                title="Advertencia",
                text="<h3 style='color: #ff5555'>Eliminar Tutor</h3>",
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
            self.pag_tabla_tutorA()
            
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
                exportar_modelo_a_excel(self.get_data_all(),archivo,Tutor_Academico)
                
                QMessageBox.information(self.main, "Éxito", "La base de datos se exportó correctamente.")
            except Exception as e:
                QMessageBox.critical(self.main, "Error", f"No se pudo exportar: {str(e)}")



        
    