import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, 
                             QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QColor, QCursor

class ProBlueFinal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(950, 650)
        
        # Ajustes de sensibilidad
        self.shadow_size = 15
        self.edge_margin = 5 
        self._resizing = False
        self._resize_edge = None
        self.drag_pos = None

        # 1. Contenedor Raíz (Invisible, para la sombra)
        self.root_widget = QWidget()
        self.setCentralWidget(self.root_widget)
        self.root_layout = QVBoxLayout(self.root_widget)
        self.root_layout.setContentsMargins(self.shadow_size, self.shadow_size, self.shadow_size, self.shadow_size)

        # 2. El Contenedor Visual (Azul/Gris)
        self.main_frame = QFrame()
        self.main_frame.setStyleSheet("""
            QFrame { 
                background-color: #f5f5f5; 
                border-radius: 10px; 
                border: 1px solid #003366;
            }
        """)
        self.root_layout.addWidget(self.main_frame)

        # Aplicar Sombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.main_frame.setGraphicsEffect(shadow)

        # Layout del frame principal
        self.content_layout = QVBoxLayout(self.main_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # 3. Barra de Título
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("background-color: #003366; border-top-left-radius: 9px; border-top-right-radius: 9px; border: none;")
        
        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_label = QLabel("PROYECTO FINAL | AZUL")
        self.title_label.setStyleSheet("color: white; font-weight: bold; margin-left: 10px;")
        
        self.btn_min = self._create_btn("-")
        self.btn_max = self._create_btn("□")
        self.btn_close = self._create_btn("✕", True)

        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.btn_min)
        self.title_layout.addWidget(self.btn_max)
        self.title_layout.addWidget(self.btn_close)

        self.content_layout.addWidget(self.title_bar)
        self.content_layout.addStretch()

        # Conexiones
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self._toggle_maximize)
        self.btn_close.clicked.connect(self.close)

        # IMPORTANTE: Habilitar tracking en TODO
        self.setMouseTracking(True)
        self.root_widget.setMouseTracking(True)
        self.main_frame.setMouseTracking(True)
        self.title_bar.setMouseTracking(True)

    def _create_btn(self, text, is_close=False):
        btn = QPushButton(text)
        btn.setFixedSize(45, 40)
        hover = "#e81123" if is_close else "#004488"
        btn.setStyleSheet(f"QPushButton{{background:transparent;color:white;border:none;}} QPushButton:hover{{background:{hover};}}")
        return btn

    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.btn_max.setText("□")
            self.root_layout.setContentsMargins(self.shadow_size, self.shadow_size, self.shadow_size, self.shadow_size)
            self.main_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 10px; border: 1px solid #003366;")
        else:
            self.showMaximized()
            self.btn_max.setText("❐")
            self.root_layout.setContentsMargins(0, 0, 0, 0)
            self.main_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 0px; border: none;")

    def _get_edge(self, pos):
        # Usamos coordenadas relativas a la ventana completa
        w, h = self.width(), self.height()
        x, y = pos.x(), pos.y()
        m = self.edge_margin + self.shadow_size

        # Esquinas
        if x < m and y < m: return 'top_left'
        if x > w - m and y < m: return 'top_right'
        if x < m and y > h - m: return 'bottom_left'
        if x > w - m and y > h - m: return 'bottom_right'
        # Bordes
        if x < m: return 'left'
        if x > w - m: return 'right'
        if y < m: return 'top'
        if y > h - m: return 'bottom'
        return None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edge = self._get_edge(event.pos())
            if edge:
                self._resizing = True
                self._resize_edge = edge
            elif self.title_bar.underMouse():
                self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        # Actualizar cursor
        if not self._resizing:
            edge = self._get_edge(event.pos())
            if edge:
                if edge in ['left', 'right']: self.setCursor(Qt.SizeHorCursor)
                elif edge in ['top', 'bottom']: self.setCursor(Qt.SizeVerCursor)
                elif edge in ['top_left', 'bottom_right']: self.setCursor(Qt.SizeFDiagCursor)
                elif edge in ['top_right', 'bottom_left']: self.setCursor(Qt.SizeBDiagCursor)
            else:
                # CORRECCIÓN: Si no hay borde, forzar flecha
                self.setCursor(Qt.ArrowCursor)

        # Lógica Resize
        if self._resizing:
            rect = self.geometry()
            gp = event.globalPosition().toPoint()
            if 'left' in self._resize_edge: rect.setLeft(gp.x())
            if 'right' in self._resize_edge: rect.setRight(gp.x())
            if 'top' in self._resize_edge: rect.setTop(gp.y())
            if 'bottom' in self._resize_edge: rect.setBottom(gp.y())
            
            if rect.width() > 300 and rect.height() > 200:
                self.setGeometry(rect)
        
        # Lógica Move
        elif self.drag_pos:
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.pos() + delta)
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self.drag_pos = None
        self.setCursor(Qt.ArrowCursor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProBlueFinal()
    window.show()
    sys.exit(app.exec())