import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QWidget,QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QTableWidget, QHeaderView, QMenu, 
                             QLineEdit, QListWidget, QListWidgetItem, 
                             QWidgetAction, QVBoxLayout,  QStyle, QStyleOptionButton)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QAction

class MiWidgetClickeable(QWidget):
    # Creamos la señal personalizada
    clicked = Signal()

    def click(self):
        """Permite simular el clic programáticamente."""
        if self.isEnabled():
            self.clicked.emit()

    def mousePressEvent(self, event):
        # Emitimos la señal cuando el usuario hace clic físicamente
        self.click()
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
        
class ExcelHeader(QHeaderView):
    # Señal personalizada para avisar qué columna y qué acción se activó
    filterClicked = Signal(int, str) 

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.restore()

        # Dibujar la flecha de filtro
        option = QStyleOptionButton()
        btn_size = 16
        option.rect = QRect(rect.right() - btn_size - 4, 
                            rect.center().y() - (btn_size // 2), 
                            btn_size, btn_size)
        option.state = QStyle.State_Enabled | QStyle.State_Active
        self.style().drawPrimitive(QStyle.PE_IndicatorArrowDown, option, painter)

    def mousePressEvent(self, event):
        logicalIndex = self.logicalIndexAt(event.position().toPoint())
        if logicalIndex != -1:
            x_pos = self.sectionPosition(logicalIndex)
            width = self.sectionSize(logicalIndex)
            button_rect = QRect(x_pos + width - 25, 0, 25, self.height())

            if button_rect.contains(event.position().toPoint()):
                self.show_filter_menu(logicalIndex, event.globalPosition().toPoint())
                return 
        super().mousePressEvent(event)

    def show_filter_menu(self, index, position):
        menu = QMenu(self)
        
        # Acciones de ejemplo
        sort_az = menu.addAction("🔼 Ordenar A-Z")
        sort_za = menu.addAction("🔽 Ordenar Z-A")
        menu.addSeparator()

        # Buscador y Lista
        container = QWidget()
        layout = QVBoxLayout(container)
        search = QLineEdit()
        search.setPlaceholderText(f"Filtrar Columna {index}...")
        layout.addWidget(search)
        
        lw = QListWidget()
        lw.setMaximumHeight(100)
        # Aquí podrías llenar con datos reales de la columna 'index'
        lw.addItem("(Seleccionar todo)")
        
        action_widget = QWidgetAction(menu)
        action_widget.setDefaultWidget(container)
        menu.addAction(action_widget)

        # Ejecutar menú y capturar qué acción se eligió
        selected_action = menu.exec(position)
        
        if selected_action == sort_az:
            self.filterClicked.emit(index, "SORT_ASC")
        elif selected_action == sort_za:
            self.filterClicked.emit(index, "SORT_DESC")

# ESTA ES LA CLASE QUE PROMOVERÁS EN QT DESIGNER
class FilterTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_header = ExcelHeader(Qt.Horizontal, self)
        self.setHorizontalHeader(self.custom_header)