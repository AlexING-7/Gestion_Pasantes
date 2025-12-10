import sys
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

class ModernMessageBox(QMessageBox):
    def __init__(self, title, text, informative_text="", detailed_text="", parent=None):
        super().__init__(parent)
        
        # 1. Configuración Básica
        self.setWindowTitle(title)
        self.setText(text)
        self.setInformativeText(informative_text)
        
        # 2. Icono Personalizado (Evitamos los iconos nativos feos)
        # Usamos un icono del sistema o cargamos un PNG propio
        # self.setIconPixmap(QPixmap("alert.png")) 
        self.setIcon(QMessageBox.Warning) 
        
        # 3. Texto Detallado (Solo si existe)
        if detailed_text:
            self.setDetailedText(detailed_text)
            
        # 4. Estilos (QSS inyectado directamente para portabilidad)
        self.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D30;
            }
            QMessageBox QLabel {
                color: #DDDDDD;
                font-family: "Segoe UI";
                font-size: 13px;
            }
            /* El texto principal suele ser un label específico, pero difícil de aislar sin objectName. 
               Qt le pone estilos inline a veces. */
               
            QMessageBox QPushButton {
                background-color: #3E3E42;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #505055;
                border: 1px solid #007ACC;
            }
            /* Estilo para el área de texto detallado (logs) */
            QTextEdit {
                background-color: #1E1E1E;
                color: #FF8080; /* Rojo suave */
                font-family: "Consolas";
                border: 1px solid #3E3E42;
            }
        """)

    def add_custom_buttons(self):
        """Añade botones traducidos y retorna referencias a ellos."""
        # Role: AcceptRole (Enter), RejectRole (Esc), DestructiveRole
        btn_save = self.addButton("Aceptar", QMessageBox.AcceptRole)
        btn_cancel = self.addButton("Cancelar", QMessageBox.RejectRole)
        
        return btn_save, btn_cancel

# --- EJEMPLO DE USO EN UNA VENTANA ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de QMessageBox")
        self.resize(400, 200)

        container = QWidget()
        layout = QVBoxLayout(container)
        
        btn = QPushButton("Simular Error Crítico")
        btn.clicked.connect(self.show_expert_message)
        layout.addWidget(btn)
        
        self.setCentralWidget(container)

    def show_expert_message(self):
        try:
            # Simulamos un error real para obtener un traceback
            x = 1 / 0
        except Exception:
            # Capturamos el error como string
            error_trace = traceback.format_exc()

            # Instanciamos nuestra clase experta
            msg = ModernMessageBox(
                title="Error de Cálculo",
                text="<h3 style='color: #ff5555'>Ha ocurrido una excepción crítica</h3>",
                informative_text="El sistema no puede dividir por cero. ¿Deseas guardar un reporte antes de cerrar?",
                detailed_text=error_trace, # Aquí va el log técnico
                parent=self
            )
            
            # Añadimos botones personalizados
            btn_accept, btn_cancel = msg.add_custom_buttons()
            
            # Ejecutamos el diálogo (Modal loop)
            msg.exec()

            # Verificamos qué botón fue presionado
            clicked = msg.clickedButton()
            
            if clicked == btn_accept:
                print("Lógica: Guardando reporte...")
            elif clicked == btn_cancel:
                print("Lógica: Cancelado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())