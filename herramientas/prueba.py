import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, 
                             QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QColor, QCursor
from plantilla_ui import cargar_ui
from CustomMain import CustomWindow
class ProBlueResizable(CustomWindow):
    def __init__(self):
        super().__init__()
        self.window=cargar_ui("UI/login.ui",self)
        self.layout_principal.addWidget(self.window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProBlueResizable()
    window.show()
    sys.exit(app.exec())