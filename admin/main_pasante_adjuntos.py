import os
import sys
from datetime import datetime
from pathlib import Path
from PySide6.QtGui import  QIcon
from modelos.modulo import Pasantia
from PySide6.QtWidgets import QWidget,QHBoxLayout, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QTableWidget,QStyle,QLineEdit,QAbstractScrollArea
import shutil
from herramientas.docs import reemplazar_texto
from modelos.modulo import DocumentoAdjunto,session
from PySide6.QtWidgets import QHeaderView

class show_documentos():
    
    def __init__(self,window,pasante:Pasantia) -> None:
        self.pasante=pasante
        self.window=window
        self.comboDoc=window.comboDoc
        self.comboDoc_2=window.comboDoc_2
        self.comboDoc_2.clear()
        self.comboDoc.setCurrentIndex(-1)
        self.lineRuta=window.lineRuta
        self.lineRuta.clear()
        self.file_path=None
        self.btnSubirDoc=window.btnSubirDoc
        self.btnGenDoc=window.btnGenDoc
        self.tabla_documentos=window.tabla_documentos
        self.regresarButtonP_2=self.window.regresarButtonP_2
        self.window.StackedPsa.setCurrentIndex(2)
        self.conectar_eventos()

    def list_formats(self):
        formatos={
            "Carta de Solicitud de Pasantia":"formatos/1. CARTA SOLICITUD DE PASANTIA.docx",
            "Carta de Aceptacion del Pasante":"formatos/2.CARTA ACEPTACION DEL PASANTE.docx",
            "Acto de Inicio":"formatos/3.ACTA DE INICIO.docx",
            "Acto de Inicio de Ejecucion de Pasantia":"formatos/4.ACTA DE INICIO DE EJECUCIÓN DE PASANTÍA.docx",
            "Contrato del Pasante":"formatos/5.CONTRATO DEL PASANTE.docx",
            "Inscripción de Pasantía":"formatos/6. INSCRIPCION DE PASANTIA.docx"
        }
        for text,data in formatos.items():
            self.comboDoc_2.addItem(text,data)
    def pag_tabla(self):
        self.tabla_documentos:QTableWidget
        header=self.tabla_documentos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.tabla_documentos.setRowCount(0)
        for fila,doc in enumerate(self.pasante.documentos):
            self.tabla_documentos.insertRow(fila)
            ruta=doc.ruta.split("/")
            self.tabla_documentos.setItem(fila,0,QTableWidgetItem(str(doc.tipo_de_documento)))
            self.tabla_documentos.setItem(fila,1,QTableWidgetItem(str(ruta[-1])))
            self.tabla_documentos.setItem(fila,2,QTableWidgetItem(str(doc.fecha_subida)))
            self.tabla_documentos.setItem(fila,3,QTableWidgetItem(str(doc.estado)))
            
            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 

            boton_ver=QPushButton("Ver")
            boton_ver.clicked.connect(lambda checked,x=doc: self.ver_documento(x))
            btn_borrar = QPushButton("Borrar")
            #btn_borrar.clicked.connect(lambda checked,x=empresa: self.delete_empresa(x))

            btn_borrar.setStyleSheet("background-color: #f44336; color: white;")                 
            boton_ver.setStyleSheet("background-color: #3d8ec9; color: white; font-weight: bold;") 

            layout_botones.addWidget(boton_ver)
            layout_botones.addWidget(btn_borrar)

            # 6. Insertar el contenedor en la celda
            self.tabla_documentos.setCellWidget(fila, 4, widget_contenedor)

    def conectar_eventos(self):
        self.regresarButtonP_2.clicked.connect(lambda: self.window.StackedPsa.setCurrentIndex(1))
        lista_acciones = self.lineRuta.actions()
        for accion in lista_acciones:
            self.lineRuta.removeAction(accion)

        icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "upload.svg"
        
        if icon_path.exists():
            icon = QIcon(str(icon_path))
        else:
            # Fallback al icono estándar si no encuentra el archivo
            icon = self.lineRuta.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
        
        # Solo agregamos la acción si no existía ninguna
        self.icon = self.lineRuta.addAction(icon, QLineEdit.ActionPosition.LeadingPosition)
            
        try:
            self.btnSubirDoc.clicked.disconnect()
            self.btnGenDoc.clicked.disconnect()
        except Exception:
            pass
        self.btnSubirDoc.clicked.connect(self.subir_documento)
        self.icon.triggered.connect(self.path_file)
        self.btnGenDoc.clicked.connect(self.generar_doc)
        self.pag_tabla()
        self.list_formats()
    
    def path_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self.window, "Seleccionar Archivo", "", "Archivos (*.pdf *.doc *.docx)"
        )
        self.lineRuta.setText(self.file_path)
        
    
    def subir_documento(self):

        if self.file_path:
            # 2. Crear carpeta de destino si no existe
            destino_dir = f"resources/documentos/{self.pasante.carrera}/{self.pasante.student.cedula}"
            if not os.path.exists(destino_dir):
                os.makedirs(destino_dir)
            
            # 3. Generar un nombre único para evitar duplicados
            extension = os.path.splitext(self.file_path)[1]
            nombre_archivo = f"{self.comboDoc.currentText()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
            self.ruta_final = os.path.join(destino_dir, nombre_archivo).replace("\\","/")
        else:
            QMessageBox.critical(self.window, "Error", f"Seleccione el Archivo")
            return
        
        documento=DocumentoAdjunto(tipo_de_documento=self.comboDoc.currentText(),
                                   ruta=self.ruta_final
                                   )
        
        self.pasante.documentos.append(documento)
        session.commit()
        self.guardar_archivo()
        QMessageBox.information(self.window, "Éxito", "Archivo Guardado correctamente.")
        self.pag_tabla()
        
            
    def guardar_archivo(self):
        try:
            shutil.copy(self.file_path, self.ruta_final)
             # Guardamos la ruta en una variable
                
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"No se pudo copiar el archivo: {e}")         
    
    def ver_documento(self,doc):
        from admin.ver_documento import WebViewDoc
        self.ver=WebViewDoc(doc)
        self.ver.exec()
        self.pag_tabla()
    
    def eliminar_documento(self):
        pass
        
    def generar_doc(self):
        # Validar que haya selección
        if not self.comboDoc_2.currentData():
            QMessageBox.warning(self.window, "Atención", "Seleccione un formato de documento.")
            return

        formatos={
            "Carta de Solicitud de Pasantia":"formatos/1. CARTA SOLICITUD DE PASANTIA.docx",
            "Carta de Aceptacion del Pasante":"formatos/2.CARTA ACEPTACION DEL PASANTE.docx",
            "Acto de Inicio":"formatos/3.ACTA DE INICIO.docx",
            "Acto de Inicio de Ejecucion de Pasantia":"formatos/4.ACTA DE INICIO DE EJECUCIÓN DE PASANTÍA.docx",
            "Contrato del Pasante":"formatos/5.CONTRATO DEL PASANTE.docx",
            "Inscripción de Pasantía":"formatos/6. INSCRIPCION DE PASANTIA.docx"
        }

        doc_key = self.comboDoc_2.currentText()
        if doc_key not in formatos:
            QMessageBox.critical(self.window, "Error", f"Formato desconocido: {doc_key}")
            return

        template_path = self.comboDoc_2.currentData()
        if not os.path.exists(template_path):
            QMessageBox.critical(self.window, "Error", f"No se encontró la plantilla: {template_path}")
            return

        suggested = f"{doc_key}.docx"
        save_path, _ = QFileDialog.getSaveFileName(self.window, "Guardar Documento", suggested, "Documento (*.docx)")
        if not save_path:
            # El usuario canceló
            return

        # Asegurar extensión .docx
        if not save_path.lower().endswith('.docx'):
            save_path = save_path + '.docx'

        try:
            reemplazar_texto(self.pasante, template_path, save_path)
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"No se pudo generar el documento: {e}")
            return

        QMessageBox.information(self.window, "Éxito", f"Documento generado: {save_path}")