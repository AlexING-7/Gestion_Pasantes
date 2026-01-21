from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QGridLayout, QLineEdit, QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys

# Ventana especializada para generar documentos de pasantías
# Adaptación del módulo "Generador de Documentos de Pasantías" a PySide6

class GeneradorDocumentosPasantias(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Documentos de Pasantías")
        self.showMaximized()

        # ===== Colores institucionales =====
        self.brand_color = "#003366"

        # ===== Widget central =====
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # ===== Header =====
        header = QFrame()
        header.setStyleSheet(f"background-color:{self.brand_color};")
        header_layout = QVBoxLayout(header)

        title = QLabel("Generador de Documentos de Pasantías")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color:white;")

        subtitle = QLabel("Seleccione un pasante y genere documentos institucionales automáticamente")
        subtitle.setStyleSheet("color:#e0e0e0;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header)

        # ===== Selector de pasante =====
        selector_frame = QFrame()
        selector_frame.setStyleSheet("background:white; border-radius:12px;")
        selector_layout = QHBoxLayout(selector_frame)

        lbl_pasante = QLabel("Pasante:")
        lbl_pasante.setFont(QFont("Arial", 11, QFont.Bold))

        self.combo_pasantes = QComboBox()
        self.combo_pasantes.addItems([
            "Seleccione un pasante",
            "Juan Pérez - V-12345678",
            "María Gómez - V-87654321",
            "Carlos Ruiz - V-11223344"
        ])

        selector_layout.addWidget(lbl_pasante)
        selector_layout.addWidget(self.combo_pasantes)
        main_layout.addWidget(selector_frame)

        # ===== Área de formatos =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        formatos_container = QWidget()
        grid = QGridLayout(formatos_container)
        grid.setSpacing(15)

        self.formatos = [
            "Carta de Presentación",
            "Carta de Aceptación",
            "Carta de Postulación",
            "Constancia de Pasantía",
            "Carta de Culminación",
            "Plan de Trabajo",
            "Informe Parcial",
            "Informe Final",
            "Evaluación Tutor Académico",
            "Evaluación Tutor Empresarial",
            "Acta de Inicio de Pasantía"
        ]

        row = col = 0
        for formato in self.formatos:
            card = self.crear_card_formato(formato)
            grid.addWidget(card, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        scroll.setWidget(formatos_container)
        main_layout.addWidget(scroll)

        # ===== Añadir nuevo formato =====
        add_frame = QFrame()
        add_layout = QHBoxLayout(add_frame)

        self.input_nuevo_formato = QLineEdit()
        self.input_nuevo_formato.setPlaceholderText("Nombre del nuevo formato")

        btn_add = QPushButton("Añadir formato")
        btn_add.clicked.connect(self.agregar_formato)
        btn_add.setStyleSheet(f"background:{self.brand_color}; color:white; padding:6px 12px; border-radius:8px;")

        add_layout.addWidget(self.input_nuevo_formato)
        add_layout.addWidget(btn_add)
        main_layout.addWidget(add_frame)

    def crear_card_formato(self, nombre):
        frame = QFrame()
        frame.setStyleSheet("background:#f8fafc; border-radius:14px; padding:10px;")
        layout = QHBoxLayout(frame)

        lbl = QLabel(nombre)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFont(QFont("Arial", 10, QFont.Bold))

        btn = QPushButton("Generar documento")
        btn.setStyleSheet(f"background:{self.brand_color}; color:white; padding:6px; border-radius:8px;")
        btn.clicked.connect(lambda: self.generar_documento(nombre))

        layout.addWidget(lbl)
        layout.addWidget(btn)
        return frame

    def generar_documento(self, formato):
        pasante = self.combo_pasantes.currentText()
        if pasante == "Seleccione un pasante":
            print("Debe seleccionar un pasante")
            return
        print(f"Generando '{formato}' para {pasante}")
        # Aquí se integraría la generación real de PDF/DOCX

    def agregar_formato(self):
        nombre = self.input_nuevo_formato.text().strip()
        if nombre:
            print(f"Nuevo formato agregado: {nombre}")
            self.input_nuevo_formato.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GeneradorDocumentosPasantias()
    window.show()
    sys.exit(app.exec())
