import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from sqlalchemy import select,desc
from modelos.modulo import session,Pasantia,DocumentoAdjunto
from PySide6.QtWidgets import QMessageBox,QMainWindow, QLabel, QPushButton, QListWidgetItem, QHBoxLayout, QWidget
from PySide6.QtCore import QSize, Qt
from herramientas.plantilla_ui import cargar_ui


class StackedSolicitud():

    def __init__(self,main) -> None:
        self.main=main
        self.window=main.window        
        self.lista=self.window.listSolicitudes
        self.conectar_eventos()
        self.window.stackedWidget.setCurrentIndex(0)
    
    def conectar_eventos(self):
        self.lista_solicitudes()
    
    def lista_solicitudes(self):
        self.lista.clear()
        solicitudes=self.get_data()
        for soli in solicitudes:
            planilla=cargar_ui("UI/solicitud.ui",self.main)
            item = QListWidgetItem()
            item.setSizeHint(QSize(327,80))
            self.lista.addItem(item)
            self.lista.setItemWidget(item, planilla)
            self.conectarWidget(planilla,soli)
        
    def get_data(self):
        stmt=select(DocumentoAdjunto).where(DocumentoAdjunto.estado=="revision").order_by(desc(DocumentoAdjunto.fecha_subida))
        return session.scalars(stmt).all()
    
    def conectarWidget(self,widget,data:DocumentoAdjunto):
        widget.fecha.setText(str(data.pasantia.inicio_pasantias))
        widget.nombre.setText(f"{data.pasantia.student.primer_nombre} {data.pasantia.student.primer_apellido}")
        widget.descripcion.setText(f"{data.tipo_de_documento}")
        widget.btnVerDetalles.clicked.connect(lambda: self.ver_documento(data))
        
    def ver_documento(self,doc):
        from coord.ver_documento import WebViewDoc
        self.ver=WebViewDoc(doc)
        self.ver.exec()
        self.lista_solicitudes()
 
