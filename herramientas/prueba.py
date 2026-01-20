import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QListWidget, QListWidgetItem, 
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor

# --- 1. TU WIDGET PERSONALIZADO (LA TARJETA) ---
class TarjetaEstudiante(QWidget):
    def __init__(self, nombre, cedula, estado):
        super().__init__()
        
        # Diseño de la tarjeta (Borde y fondo)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 8px;
            }
            QLabel {
                border: none;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        # Layout vertical dentro de la tarjeta
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        # Datos del estudiante
        lbl_nombre = QLabel(f"👤 {nombre}")
        lbl_nombre.setStyleSheet("font-weight: bold; font-size: 14px; color: #1f2937;")
        
        lbl_cedula = QLabel(f"C.I: {cedula}")
        lbl_cedula.setStyleSheet("color: #6b7280; font-size: 12px;")

        lbl_estado = QLabel(f"Estado: {estado}")
        # Color dinámico según el estado (ejemplo simple)
        color_estado = "green" if estado == "Aprobado" else "#d97706"
        lbl_estado.setStyleSheet(f"color: {color_estado}; font-weight: bold; font-size: 12px;")

        # Botón de acción
        btn_ver = QPushButton("Ver Expediente")
        btn_ver.setCursor(Qt.PointingHandCursor)
        # Conectar botón (ejemplo)
        btn_ver.clicked.connect(lambda: print(f"Abriendo expediente de {nombre}"))

        # Añadir al layout
        layout_principal.addWidget(lbl_nombre)
        layout_principal.addWidget(lbl_cedula)
        layout_principal.addWidget(lbl_estado)
        layout_principal.addWidget(btn_ver)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Pasantías - Vista de Tarjetas")
        self.resize(900, 600)

        # --- 2. CONFIGURACIÓN DEL LIST WIDGET RESPONSIVE ---
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(15)
        
        # Modo Icono + Adjust para que sea Grid Responsive
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setMovement(QListWidget.Static) # Evitar arrastrar items
        
        # Color de fondo del área general
        self.list_widget.setStyleSheet("QListWidget { background-color: #f3f4f6; padding: 10px; }")

        self.setCentralWidget(self.list_widget)

        # Cargar datos
        self.agregar_tarjetas()

    def agregar_tarjetas(self):
        # Datos simulados (Bases de datos)
        estudiantes = [
            ("Maria Rodriguez", "28.123.456", "En Curso"),
            ("Jose Perez", "27.654.321", "Aprobado"),
            ("Ana Mendez", "30.111.222", "Pendiente"),
            ("Carlos Ruiz", "29.888.999", "En Curso"),
            ("Luisa Tovar", "26.555.444", "Aprobado"),
        ]

        for nombre, ci, estado in estudiantes:
            # A. Crear la instancia de TU widget
            widget_tarjeta = TarjetaEstudiante(nombre, ci, estado)

            # B. Crear el Item contenedor (El "Hueco" en la lista)
            item = QListWidgetItem()
            
            # C. IMPORTANTE: Definir el tamaño del hueco
            # Debe coincidir o ser ligeramente mayor al tamaño de tu widget
            item.setSizeHint(QSize(200, 140)) 

            # D. Añadir el item a la lista primero
            self.list_widget.addItem(item)

            # E. El paso final: Poner el widget visual ENCIMA del item
            self.list_widget.setItemWidget(item, widget_tarjeta)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())