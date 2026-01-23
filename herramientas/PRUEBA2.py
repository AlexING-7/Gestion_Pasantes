from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QFrame, QMessageBox, QFileDialog
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
import sys


class GeneradorDocumentosPasantias(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Documentos de Pasantías")
        self.showMaximized()
        self.setStyleSheet("background-color: #f8fafc;")

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
            "Acta de Inicio de Pasantía",
        ]

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Header
        header = QLabel("Generador de Documentos de Pasantías")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            "background-color: #003366; color: white; padding: 20px;"
        )
        header.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(header)

        # Contenido principal
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Panel izquierdo - Datos del pasante
        left_panel = QFrame()
        left_panel.setStyleSheet("background: white; border-radius: 12px;")
        left_panel.setFixedWidth(320)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignTop)

        # Foto del estudiante
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(180, 180)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet(
            "border: 2px dashed #003366; border-radius: 90px; color: #64748b;"
        )
        self.photo_label.setText("Sin foto")
        left_layout.addWidget(self.photo_label, alignment=Qt.AlignCenter)

        btn_photo = QPushButton("Cargar foto")
        btn_photo.clicked.connect(self.cargar_foto)
        btn_photo.setStyleSheet(self.btn_style())
        left_layout.addWidget(btn_photo)

        left_layout.addSpacing(20)

        lbl_pasante = QLabel("Seleccionar pasante")
        lbl_pasante.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(lbl_pasante)

        self.combo_pasantes = QComboBox()
        self.combo_pasantes.addItems([
            "Carlos Ruiz - V-12345678",
            "María López - V-87654321",
            "José Fernández - V-11223344",
        ])
        left_layout.addWidget(self.combo_pasantes)

        content_layout.addWidget(left_panel)

        # Panel derecho - formatos
        right_panel = QFrame()
        right_panel.setStyleSheet("background: white; border-radius: 12px;")
        right_layout = QVBoxLayout(right_panel)

        title = QLabel("Formatos disponibles")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        right_layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        grid = QGridLayout(scroll_content)

        for i, formato in enumerate(self.formatos):
            card = QFrame()
            card.setStyleSheet(
                "border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px;"
            )
            card_layout = QVBoxLayout(card)

            lbl = QLabel(formato)
            lbl.setFont(QFont("Arial", 10, QFont.Bold))
            card_layout.addWidget(lbl)

            btn = QPushButton("Generar documento")
            btn.setStyleSheet(self.btn_style())
            btn.clicked.connect(lambda _, f=formato: self.generar_documento(f))
            card_layout.addWidget(btn)

            grid.addWidget(card, i // 3, i % 3)

        scroll.setWidget(scroll_content)
        right_layout.addWidget(scroll)

        content_layout.addWidget(right_panel)

    def btn_style(self):
        return (
            "QPushButton {"
            "background-color: #003366; color: white; padding: 8px;"
            "border-radius: 6px;}"
            "QPushButton:hover { background-color: #002244; }"
        )

    def cargar_foto(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar foto", "", "Imágenes (*.png *.jpg *.jpeg)"
        )
        if file:
            pixmap = QPixmap(file).scaled(
                180, 180, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            self.photo_label.setPixmap(pixmap)
            self.photo_label.setStyleSheet("border-radius: 90px;")

    def generar_documento(self, formato):
        pasante = self.combo_pasantes.currentText()
        QMessageBox.information(
            self,
            "Documento generado",
            f"Se ha generado el formato:\n\n{formato}\n\nPara el pasante:\n{pasante}",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneradorDocumentosPasantias()
    window.show()
    sys.exit(app.exec())
