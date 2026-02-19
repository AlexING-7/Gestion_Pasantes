
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QHBoxLayout,QStyle,QLineEdit,QAbstractScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon
from PySide6.QtUiTools import QUiLoader

from modelos.modulo import session,Enterprise,Pasantia
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
from herramientas.conversiones import nombreCompleto
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent

class StackEnterprise():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.StackedEmpresas.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.tabla_pasantes=self.window.tabla_pasantes_activos_Emp
        self.window.frame_TablaEmpresa.installEventFilter(main)
        self.conectar_eventos()
    
    def offset_count(self):
        return (self.numero_pagina - 1) * self.tamano_pagina
    
    def eventFilter(self,source,event):
        
        if source == self.window.frame_TablaEmpresa and event.type() == QEvent.Type.Resize:
            height=self.window.tabla_Empresas.height()
            self.tamano_pagina=int(height/25.4)
            self.pag_tabla_empresa()
            print("Ejecutando Empresa")                   
    def listas(self):
        self.window.comboRubros.clear()
        rubros=session.scalars(select(Enterprise.rubro)).all()
        self.window.comboRubros.addItem('Todas los Rubros',None)
        for i in set(rubros):
            self.window.comboRubros.addItem(i,i)         
    def conectar_eventos(self):
        self.listas()
        self.window.btnExportarEmpr.clicked.connect(self.exportar)
        self.window.btnNuevaEmpr.clicked.connect(self.open_empresa)
        #self.window.regresarButton.clicked.connect(lambda :self.window.StackedEstudiantes.setCurrentIndex(0))
        self.window.btnAntEmpr.clicked.connect(lambda :self.change_table("Anterior"))
        self.window.btnSigEmpr.clicked.connect(lambda :self.change_table("Siguiente"))
        self.window.searchEmpr.textChanged.connect(self.search)
        self.window.comboRubros.activated.connect(lambda: self.cambio_programa())
                
        if not self.window.searchEmpr.actions(): 
            icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "search.svg"
            if icon_path.exists():
                search_icon = QIcon(str(icon_path))
            else:
                search_icon = self.window.searchEmpr.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            self.search_icon = self.window.searchEmpr.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
    def indice(self):
        ind1=1+self.offset_count()
        ind2=self.numero_pagina*self.tamano_pagina
        self.window.btnIndEmpr.setText(f"{ind1}-{ind2 if ind2<self.all_data else self.all_data} de {self.all_data}")
                        
    def cambio_programa(self):
        self.numero_pagina=1
        self.pag_tabla_empresa()
    
    def header(self):
        
        header=self.window.tabla_Empresas.horizontalHeader()
        header_vertical = self.window.tabla_Empresas.verticalHeader()
        header_vertical.setDefaultSectionSize(30)
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
        
    def pag_tabla_empresa(self):
        self.header()
        empresas=self.get_data()
        tabla=self.window.tabla_Empresas
        if not empresas and tabla.rowCount():
            QMessageBox.warning(self.window, "Aviso", "Busqueda no encontrada")
            return
        if (self.all_data-self.offset_count())<=self.tamano_pagina:
           self.window.btnSigEmpr.setEnabled(False)
        else:
            self.window.btnSigEmpr.setEnabled(True)

        self.indice()
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

            boton_ver=QPushButton("")
            boton_ver.clicked.connect(lambda checked,x=empresa: self.read_empresa(x))
            btn_editar = QPushButton("")
            btn_editar.clicked.connect(lambda checked,x=empresa: self.edit_empresa(x))
            btn_borrar = QPushButton("")
            btn_borrar.clicked.connect(lambda checked,x=empresa: self.delete_empresa(x))

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

            tabla.setCellWidget(fila, 4, widget_contenedor)
        

    def get_data(self):
        search=self.window.searchEmpr.text()
        self.all_data=len(self.get_data_all())
        if not self.window.comboRubros.currentData():
            stmt=select(Enterprise).where(
                                        or_(
                                            Enterprise.rif.ilike(f"{search}%"),
                                            Enterprise.razon_social.ilike(f"{search}%")
                                        )
                                        )
        else:
            stmt=select(Enterprise).where(
                                        and_(
                                        Enterprise.rubro==self.window.comboRubros.currentData(),
                                        or_(
                                            Enterprise.rif.ilike(f"{search}%"),
                                            Enterprise.razon_social.ilike(f"{search}%")
                                        )
                                        )
                                        )
        return session.scalars(stmt.limit(self.tamano_pagina).offset(self.offset_count())).all()
    def get_data_all(self):
        search=self.window.searchEmpr.text()     
        if not self.window.comboRubros.currentData():
            stmt=select(Enterprise).where(
                                        or_(
                                            Enterprise.rif.ilike(f"{search}%"),
                                            Enterprise.razon_social.ilike(f"{search}%")
                                        )
                                        )
        else:
            stmt=select(Enterprise).where(
                                        and_(
                                        Enterprise.rubro==self.window.comboRubros.currentData(),
                                        or_(
                                            Enterprise.rif.ilike(f"{search}%"),
                                            Enterprise.razon_social.ilike(f"{search}%")
                                        )
                                        )
                                        )
        return session.scalars(stmt).all()

    def search(self):
        self.numero_pagina=1
        self.pag_tabla_empresa()
            
    def change_table(self,buttom):
        
        if buttom.lower()=="anterior":
            self.numero_pagina=self.numero_pagina-1 if self.numero_pagina>1 else 1
        elif buttom.lower()=="siguiente":
            self.numero_pagina+=1
        self.pag_tabla_empresa()
            
    def read_empresa(self,empresa:Enterprise):
        self.window.rif_Emp.clear()
        self.window.rif_Emp.setText(str(empresa.rif))
        self.window.razon_Emp.clear()
        self.window.razon_Emp.setText(empresa.razon_social)
        self.window.rubro_Emp.clear()
        self.window.rubro_Emp.setText(str(empresa.rubro))
        self.window.email_Emp.clear()
        self.window.email_Emp.setText(empresa.email)
        self.window.tlf_Emp.clear()
        self.window.tlf_Emp.setText(empresa.telefono)
        self.window.direccion_Emp.setText(str(empresa.direccion))
        self.window.StackedEmpresas.setCurrentIndex(1)
        if self.main.user_authenticated.rol=="Coordinador":
            self.window.editarEmp.setHidden(True)
            self.window.EliminarEmp.setHidden(True)
        self.window.editarEmp.clicked.connect(lambda: self.edit_empresa(empresa))
        self.window.EliminarEmp.clicked.connect(lambda: self.delete_empresa(empresa))
        self.window.regresarButtonEmp.clicked.connect(lambda: self.window.StackedEmpresas.setCurrentIndex(0))
        self.window.NumPasanteEmpr.setText("1")
        self.window.SigPasanteEmpr.clicked.connect(lambda:self.cambiar_pagina(1,empresa.pasantias))
        self.window.AntPasanteEmpr.clicked.connect(lambda:self.cambiar_pagina(-1,empresa.pasantias))
        self.pag_tabla_pasantes(empresa.pasantias[0:4])
        
    def cambiar_pagina(self, direccion: int, lista_datos: list):
        """
        Controla la paginación y actualiza la tabla de pasantes.
        
        :param direccion: 1 para Siguiente, -1 para Anterior.
        :param lista_datos: La lista completa de tutores.pasantias.
        """
        self.pagina_actual=int(self.window.NumPasanteEmpr.text())
        self.elementos_por_pagina=4
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
        self.window.NumPasanteEmpr.setText(str(self.pagina_actual))

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

        indice=self.window.NumPasanteEmpr

        header=self.tabla_pasantes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        self.tabla_pasantes.setRowCount(0)
        self.tabla_pasantes.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tabla_pasantes.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for fila,pasante in enumerate(entidad):
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
                parent=self.main
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
                exportar_modelo_a_excel(self.get_data_all(),archivo,Enterprise)
                
                QMessageBox.information(self.main, "Éxito", "La base de datos se exportó correctamente.")
            except Exception as e:
                QMessageBox.critical(self.main, "Error", f"No se pudo exportar: {str(e)}")



        
    