import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from PySide6.QtCore import QUrl,Qt
from PySide6.QtWebEngineCore import QWebEngineSettings
from herramientas.plantilla_ui import cargar_ui
from PySide6.QtWidgets import QMessageBox
from modelos.modulo import DocumentoAdjunto,session


class WebViewDoc():
    
    def __init__(self,documento):
        self.window=cargar_ui("UI/documento.ui")
        self.documento=documento
        self.window.btnAprobar.clicked.connect(self.Aprobar)
        self.window.btnRechazar.clicked.connect(self.Rechazar)
        self.window.btnCerrar.clicked.connect(self.close)
        self.web()
        
    def exec(self):
        self.window.exec()
        
    def close(self):
        self.window.close() 
        
    def web(self):
        self.window.web_view:QWebEnginePage
        self.window.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.window.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.window.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        #self.disable_features()
        # Cargar el PDF desde fichero local y pedir al visualizador que abra sin la sidebar
        # Añadimos el fragmento 'pagemode=none' (y opcional 'toolbar=0') para cerrar la barra lateral
        file_path = Path(self.documento.ruta).resolve()
        if file_path:
            url = QUrl.fromLocalFile(file_path)
            # Establecer fragmento para controlar la vista del PDF (p.ej. cerrar sidebar)
            # Algunos visores (Chromium) respetan '#pagemode=none' para ocultar miniaturas/bookmarks
            url.setFragment("pagemode=none&toolbar=0")
            self.window.web_view.load(url)
        else:
            QMessageBox.warning(self, "Archivo no encontrado", "No se encontró la ruta al PDF en la variable de entorno 'prueba'.")

    def disable_features(self):
        """Desactivar características específicas del WebEngine"""
        # Desactivar JavaScript si no es necesario
        self.window.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        
        # Desactivar enlaces externos
        #self.window.web_view.page().setLinkDelegationPolicy(QWebEnginePage.DelegateAllLinks)
        
        # Desactivar más características
        #self.window.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.window.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, False) 
        
    def Aprobar(self):
        self.documento:DocumentoAdjunto
        self.documento.estado="aprobado"
        session.commit()
        QMessageBox.information(self.window, "Éxito", "Archivo Aprobado correctamente.")
        self.close()
        
    def Rechazar(self):
        self.documento
        self.documento.estado="rechazado"
        session.commit()
        QMessageBox.information(self.window, "Éxito", "Archivo Rechazado correctamente.")
        self.close()
        
        