import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from sqlalchemy import select
from modelos.modulo import session,Pasantia,DocumentoAdjunto,Configuracion
from PySide6.QtWidgets import QMessageBox,QGraphicsDropShadowEffect, QLabel, QPushButton, QListWidgetItem, QFileDialog, QWidget
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor
from herramientas.plantilla_ui import cargar_ui
from herramientas.docs import reemplazar_texto,asignacion_pasantias
from herramientas.conversiones import jsonFormatos

class StackedDocumentos():

    def __init__(self,main) -> None:
        self.main=main
        self.window=main.window        
        self.listPasante=self.window.comboBox
        self.lista=self.window.listWidget
        
        self.formatos=jsonFormatos()
        self.formatos:dict
        self.pasante=None
        self.conectar_eventos()
        self.window.stackedWidget.setCurrentIndex(5)
    
    def conectar_eventos(self):
        self.lista_pasantes()
        self.lista_GenDocs()
    
    def lista_pasantes(self):
        for pasante in self.get_data():
            self.listPasante.addItem(f"{pasante.student.primer_nombre}  {pasante.student.primer_apellido} CIV:{pasante.student.cedula}",pasante)
    
    def find(self,pasante:Pasantia):
        index2=self.listPasante.findData(pasante)
        self.listPasante.setCurrentIndex(index2)
    
    def get_data(self):
        stmt=select(Pasantia)
        return session.scalars(stmt).all()
    
    def lista_GenDocs(self):
        self.lista.clear()
        docs=self.formatos.keys()
        for i in docs:
        
            btn=cargar_ui("UI/generar_doc.ui",self.main)
            btn.label_Documento.setText(i)
            item = QListWidgetItem()
            item.setSizeHint(QSize(430,82))
            self.window.listWidget.addItem(item)
            self.window.listWidget.setItemWidget(item, btn)
            self.conectarWidget(btn,i)
        else:
            btn=cargar_ui("UI/generar_doc.ui",self.main)
            btn.label_Documento.setText("Asignación de Pasantes")
            item = QListWidgetItem()
            item.setSizeHint(QSize(430,82))
            self.window.listWidget.addItem(item)
            self.window.listWidget.setItemWidget(item, btn)
            self.conectarWidget(btn,"lista")
            

    def conectarWidget(self,widget,doc):
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(25)           
        shadow.setXOffset(0)               
        shadow.setYOffset(8)               
        shadow.setColor(QColor(0, 0, 0, 20))
        widget.setGraphicsEffect(shadow) 
        widget.btn.clicked.connect(lambda: self.generar_doc(doc))
        
    def generar_doc(self,formato):
        # Validar que haya selección

        if formato=="lista":
            conf=session.query(Configuracion).all()
            dic_conf=dict((i.clave,i.valor) for i in conf)
            pasantes=session.query(Pasantia).where(Pasantia.lapso_academico==dic_conf["lapso_actual"]).all()
            asignacion_pasantias(pasantes)
            return
        if not self.listPasante.currentData():
            QMessageBox.warning(self.window, "Atención", "Seleccione un Pasante.")
            return
        
        self.pasante=self.listPasante.currentData()
        
        formatos=self.formatos

        template_path = formatos[formato]
        if not os.path.exists(template_path):
            QMessageBox.critical(self.window, "Error", f"No se encontró la plantilla: {template_path}")
            return

        suggested = f"{formato}.docx"
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

