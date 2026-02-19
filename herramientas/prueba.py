import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from PySide6.QtWidgets import (QApplication, QTableWidget, QHeaderView, 
                             QMenu, QVBoxLayout, QWidget, QStyle, QStyleOptionButton)
from PySide6.QtWidgets import (QLineEdit, QListWidget, QListWidgetItem, 
                             QWidgetAction, QVBoxLayout, QFrame)
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter

class ExcelHeader(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        # Guardamos qué columna tiene el filtro activo (opcional)
        self.filter_column = -1 

    def paintSection(self, painter, rect, logicalIndex):
        # 1. Dibujar el encabezado normal primero
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.restore()

        # 2. Dibujar la flechita del filtro (estilo botón de combo)
        option = QStyleOptionButton()
        # Definimos el área del botón (lado derecho del encabezado)
        button_size = 16
        option.rect = QRect(rect.right() - button_size - 2, 
                            rect.center().y() - (button_size // 2), 
                            button_size, button_size)
        option.state = QStyle.State_Enabled | QStyle.State_Active
        
        # Dibujamos el indicador de flecha usando el estilo nativo del sistema
        self.style().drawPrimitive(QStyle.PE_IndicatorArrowDown, option, painter)

    def mousePressEvent(self, event):
        # 1. Obtenemos la columna (usamos position().toPoint() para PySide6 moderno)
        logicalIndex = self.logicalIndexAt(event.position().toPoint())
        
        if logicalIndex != -1:
            x_pos = self.sectionPosition(logicalIndex)
            width = self.sectionSize(logicalIndex)
            height = self.height()
            
            # 2. Definir la zona del botón (los últimos 25 píxeles)
            button_rect = QRect(x_pos + width - 25, 0, 25, height)

            # 3. CAMBIO CLAVE: Usamos event.position().toPoint()
            # Esto convierte la posición QPointF (float) a QPoint (int) para el QRect
            if button_rect.contains(event.position().toPoint()):
                self.show_filter_menu(logicalIndex, event.globalPosition().toPoint())
                return 

        super().mousePressEvent(event)
    def show_filter_menu(self, index, position):
        menu = QMenu(self)
        
        # 1. Opciones básicas de ordenamiento
        menu.addAction("🔼 Ordenar de A a Z")
        menu.addAction("🔽 Ordenar de Z a A")
        menu.addSeparator()

        # 2. SECCIÓN DE BÚSQUEDA Y LISTA (Estilo Excel)
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Buscador
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Buscar...")
        layout.addWidget(search_bar)
        
        # Lista de Checkboxes
        list_widget = QListWidget()
        list_widget.setMaximumHeight(150)
        
        # Ejemplo de items (en la vida real, sacarías esto de los datos de la tabla)
        items = ["(Seleccionar todo)", "Elemento A", "Elemento B", "Elemento C"]
        for text in items:
            item = QListWidgetItem(text)
            item.setCheckState(Qt.Unchecked) # O Qt.Checked
            list_widget.addItem(item)
            
        layout.addWidget(list_widget)

        # Empaquetar el widget en el menú
        action = QWidgetAction(menu)
        action.setDefaultWidget(container)
        menu.addAction(action)
        
        menu.addSeparator()
        menu.addAction("Aceptar").triggered.connect(lambda: print("Filtrando..."))
        menu.addAction("Cancelar")

        menu.exec(position)

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Style Filter - PySide6")
        self.resize(600, 400)

        self.tabla = QTableWidget(10, 3)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Fecha", "Estado"])
        
        # Aplicamos nuestro encabezado personalizado
        nuevo_header = ExcelHeader(Qt.Horizontal, self.tabla)
        self.tabla.setHorizontalHeader(nuevo_header)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabla)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())