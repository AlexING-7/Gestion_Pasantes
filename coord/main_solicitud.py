import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from sqlalchemy import select
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
            item.setSizeHint(QSize(327,230))
            self.lista.addItem(item)
            self.lista.setItemWidget(item, planilla)
            self.conectarWidget(planilla,soli)
        
    def get_data(self):
        stmt=select(Pasantia).where(Pasantia.estado=="solicitada")
        return session.scalars(stmt).all()
    
    def conectarWidget(self,widget,data:Pasantia):
        widget.fecha.setText(str(data.inicio_pasantias))
        widget.nombre.setText(f"{data.student.primer_nombre} {data.student.primer_apellido}")
