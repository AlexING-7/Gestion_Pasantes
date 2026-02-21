import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from sqlalchemy import select,desc
from sqlalchemy.orm import selectinload
from modelos.modulo import session,Pasantia,DocumentoAdjunto
from PySide6.QtWidgets import QMessageBox,QMainWindow, QLabel, QPushButton, QListWidgetItem, QHBoxLayout, QWidget
from PySide6.QtCore import QSize, Qt
from herramientas.plantilla_ui import cargar_ui
from datetime import datetime,timedelta
from herramientas.conversiones import formatear_hora


class StackedSolicitud():

    def __init__(self,main) -> None:
        self.main=main
        self.window=main.window        
        self.lista=self.window.listSolicitudes
        
        # configuración para paginación / carga por lotes
        self.batch_size = 30
        self.offset = 0
        self.loading = False

        self.window.stackedWidget.setCurrentIndex(0)
        self.comboEstado=self.window.comboSoliEstado
        self.comboTiempo=self.window.comboSoliTiempo
        self.conectar_eventos()
    
    def conectar_eventos(self):
        
        self.comboEstado.activated.connect(lambda: self.lista_solicitudes())
        self.comboTiempo.activated.connect(lambda: self.lista_solicitudes())
        # detectar scroll para cargar más items cuando el usuario llegue al final
        try:
            self.lista.verticalScrollBar().valueChanged.connect(self.on_scroll)
        except Exception:
            pass
        self.combos()
        self.lista_solicitudes()
    
    def combos(self):
        self.comboEstado.clear()
        self.comboTiempo.clear()
        estados=["revision","aprobado","rechazado"]
        ahora = datetime.now()
        opciones = {
            "cualquier momento": None,
            "hace una hora": ahora - timedelta(hours=1),
            "pasadas 24 horas": ahora - timedelta(days=1),
            "ultima semana": ahora - timedelta(weeks=1),
            "ultimo mes": ahora - timedelta(days=30),
            "ultimo año": ahora - timedelta(days=365) 
        }
        for i in estados:
            self.comboEstado.addItem(i.upper(),i)
        for x,y in opciones.items():
            self.comboTiempo.addItem(x.upper(),y)
        self.comboEstado.setCurrentIndex(0)
        self.comboTiempo.setCurrentIndex(0)
        
    
    def lista_solicitudes(self):
        # resetear y cargar el primer lote
        self.lista.clear()
        self.offset = 0
        self.loading = False
        self.lista_solicitudes_batch()

    def lista_solicitudes_batch(self):
        if self.loading:
            return
        self.loading = True
        solicitudes = self.get_data(limit=self.batch_size, offset=self.offset)
        for soli in solicitudes:
            planilla=cargar_ui("UI/solicitud.ui",self.main)
            item = QListWidgetItem()
            item.setSizeHint(QSize(327,80))
            self.lista.addItem(item)
            self.lista.setItemWidget(item, planilla)
            self.conectarWidget(planilla,soli)
        # si recibimos lote completo, permitir siguiente carga
        if len(solicitudes) == self.batch_size:
            self.offset += self.batch_size
            self.loading = False
        else:
            # no hay más datos
            self.loading = True

    def on_scroll(self, value):
        sb = self.lista.verticalScrollBar()
        # si el scroll está en el máximo, cargar siguiente lote
        if value >= sb.maximum():
            self.lista_solicitudes_batch()
        
    def get_data(self, limit=None, offset=0):
        # usar eager loading para evitar N+1 (cargar pasantia y student)
        stmt=select(DocumentoAdjunto).options(
            selectinload(DocumentoAdjunto.pasantia).selectinload(Pasantia.student)
        )
        fecha_limite=self.comboTiempo.currentData()

        if fecha_limite:
            stmt=stmt.where(DocumentoAdjunto.fecha_subida >= fecha_limite)

        stmt=stmt.where(DocumentoAdjunto.estado==self.comboEstado.currentData()).order_by(desc(DocumentoAdjunto.fecha_subida))
        if limit:
            stmt = stmt.limit(limit).offset(offset)
        result = session.execute(stmt)
        return result.scalars().all()
    
    def conectarWidget(self,widget,data:DocumentoAdjunto):
        estados={"revision":"Pendiente","aprobado":"Aprobado","rechazado":"Rechazado"}
        widget.fecha.setText(f"{data.fecha_subida.day}-{data.fecha_subida.month}-{data.fecha_subida.year}")
        widget.Hora.setText(f"{formatear_hora(data.fecha_subida)}")
        widget.nombre.setText(f"{data.pasantia.student.primer_nombre} {data.pasantia.student.primer_apellido}")
        widget.descripcion.setText(f"{data.tipo_de_documento}")
        widget.estado.setProperty("estado", data.estado)
        widget.estado.setText(estados[data.estado])
        widget.estado.style().unpolish(widget.estado)
        widget.estado.style().polish(widget.estado)
        widget.btnVerDetalles.clicked.connect(lambda: self.ver_documento(data))
        
    def ver_documento(self,doc):
        from coord.ver_documento import WebViewDoc
        self.ver=WebViewDoc(doc)
        self.ver.exec()
        self.lista_solicitudes()
    
