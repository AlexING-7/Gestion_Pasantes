import sys
import os
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings

class PDFWebViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui()
        
    def load_ui(self):
        """Cargar la interfaz UI"""
        loader = QUiLoader()
        file = QFile("logincopy.ui")
        
        if file.open(QFile.OpenModeFlag.ReadOnly):
            self.ui = loader.load(file, self)
            file.close()
            
            # Configurar WebEngineView
            self.web_view = QWebEngineView()
            self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
            self.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
            
            # Reemplazar el widget placeholder con el WebEngineView
            layout = self.ui.findChild(QVBoxLayout, "verticalLayout")
            if layout:
                # Remover widget placeholder si existe
                placeholder = self.ui.findChild(QWidget, "widgetPlaceholder")
                if placeholder:
                    placeholder.deleteLater()
                
                # Agregar WebEngineView
                layout.insertWidget(0, self.web_view)
            
            self.setup_connections()
        else:
            self.setup_ui_programmatically()
    
    def setup_ui_programmatically(self):
        """Crear interfaz programáticamente"""
        layout = QVBoxLayout(self)
        
        # WebView para PDF
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        
        # Botón para cargar PDF
        self.btn_cargar = QPushButton("Cargar PDF")
        
        layout.addWidget(self.web_view)
        layout.addWidget(self.btn_cargar)
        
        self.setup_connections()
    
    def setup_connections(self):
        """Conectar señales"""
        # Encontrar el botón en la UI cargada
        btn = self.findChild(QPushButton, "btnCargarPDF")
        if btn:
            btn.clicked.connect(self.cargar_pdf)
        elif hasattr(self, 'btn_cargar'):
            self.btn_cargar.clicked.connect(self.cargar_pdf)
    
    def cargar_pdf(self):
        """Cargar archivo PDF"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar PDF", 
            "", 
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.mostrar_pdf(file_path)
    
    def mostrar_pdf(self, pdf_path):
        """Mostrar PDF en el WebEngineView"""
        url = QUrl.fromLocalFile(pdf_path)
        self.web_view.load(url)
        
def main():
    app = QApplication(sys.argv)
    
    # Para usar WebEngine necesitas instalar:
    # pip install PySide6-Essentials
    
    viewer = PDFWebViewer()
    viewer.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()