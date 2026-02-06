import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QWidget,QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor

class MiWidgetClickeable(QWidget):
    # Creamos una señal personalizada
    clicked = Signal()

    def mousePressEvent(self, event):
        # Emitimos la señal cuando se hace clic
        self.clicked.emit()
        super().mousePressEvent(event)
        
class ShadowFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Crear el efecto de sombra
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)           
        self.shadow.setXOffset(0)               
        self.shadow.setYOffset(8)               
        self.shadow.setColor(QColor(0, 0, 0, 45)) 
        
        # Aplicar el efecto al widget
        self.setGraphicsEffect(self.shadow)
        
class ShadowWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Crear el efecto de sombra
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)           # Suavizado de la sombra
        self.shadow.setXOffset(0)               # Desplazamiento horizontal
        self.shadow.setYOffset(8)               # Desplazamiento vertical
        self.shadow.setColor(QColor(0, 0, 0, 45)) # Color y opacidad (RGBA)
        
        # Aplicar el efecto al widget
        self.setGraphicsEffect(self.shadow)