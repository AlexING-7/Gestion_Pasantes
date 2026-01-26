import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

class MiWidgetClickeable(QWidget):
    # Creamos una señal personalizada
    clicked = Signal()

    def mousePressEvent(self, event):
        # Emitimos la señal cuando se hace clic
        self.clicked.emit()
        super().mousePressEvent(event)
        