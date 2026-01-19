import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QLineEdit,  QVBoxLayout
from PySide6.QtGui import QFont

class DockerInputStyle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulación UI")
        self.resize(500, 150)
        
        # 1. Configurar el fondo de la ventana para que sea oscuro
        self.setStyleSheet("background-color: #12151B;") 

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 20)

        # 2. Crear el componente personalizado
        self.input_group = self.create_styled_input("Docker subnet", "192.168.65.0/24")
        
        layout.addWidget(self.input_group)
        layout.addStretch() # Empuja el widget hacia arriba
        self.setLayout(layout)

    def create_styled_input(self, title_text, value_text):
        # El QGroupBox actúa como el contenedor con borde y título
        group_box = QGroupBox(title_text)
        
        # El QLineEdit es el texto editable dentro
        line_edit = QLineEdit(value_text)
        
        # Layout interno para el QGroupBox
        gb_layout = QVBoxLayout()
        gb_layout.addWidget(line_edit)
        gb_layout.setContentsMargins(10, 10, 10, 5) # Márgenes internos
        group_box.setLayout(gb_layout)

        # --- ESTILOS (QSS) ---
        # Definimos los estilos CSS para imitar la imagen
        style_sheet = """
            QGroupBox {
                /* Borde gris azulado delgado */
                border: 1px solid #3E434C; 
                border-radius: 4px;
                
                /* Margen superior para que el título no choque */
                margin-top: 8px; 
                
                /* Fuente del título */
                font-family: "Segoe UI", sans-serif;
                font-size: 12px;
            }

            /* Pseudo-elemento para el título "Docker subnet" */
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                left: 10px; /* Distancia desde la izquierda */
                
                /* Color del texto del título (gris azulado) */
                color: #69788C; 
                
                /* IMPORTANTE: El fondo debe ser igual al de la ventana 
                   para dar la ilusión de que corta el borde */
                background-color: #12151B; 
            }

            QLineEdit {
                /* Quitamos el borde nativo del input */
                border: none;
                background: transparent;
                
                /* Estilo del texto IP (blanco y negrita) */
                color: white;
                font-size: 14px;
                font-weight: bold;
                font-family: "Consolas", "Courier New", monospace;
            }
        """
        group_box.setStyleSheet(style_sheet)
        
        return group_box

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DockerInputStyle()
    window.show()
    sys.exit(app.exec())