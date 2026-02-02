import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from herramientas.FormatoMain import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QGraphicsDropShadowEffect,QApplication
from PySide6.QtCore import Qt, QPoint, QRect,QSize,QEvent
from PySide6.QtGui import QColor, QCursor,QIcon

class CustomWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.shadow_width = 15
        self.edge_margin = 5  
        self.margin = 5         
        self.drag_pos = None
        self._resizing = False
        self._resize_edge = None
        
        self.wrapper_layout.setContentsMargins(self.shadow_width, self.shadow_width, 
                                             self.shadow_width, self.shadow_width)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(0, 0, 0, 160))
        self.main_container.setGraphicsEffect(self.shadow)
        
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        #self.layout_principal.addStretch()
        
        
        # Conexiones
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self._toggle_maximize)
        self.btn_close.clicked.connect(self.close)

        # Activar tracking
        self.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)
        self.main_container.setMouseTracking(True)
        self.title_bar.setMouseTracking(True)
        
        QApplication.instance().installEventFilter(self)
    
    def eventFilter(self, obj, event):
    # Verificamos si el evento es de tipo MouseMove de forma segura
        if event.type() == QEvent.MouseMove:
            # Si NO estamos redimensionando y NO estamos en un borde
            if not self._resizing:
                pos = self.mapFromGlobal(QCursor.pos()) # Posición relativa a la ventana
                if not self._get_edge(pos):
                    if self.cursor().shape() != Qt.ArrowCursor:
                        self.setCursor(Qt.ArrowCursor)
        
        # IMPORTANTE: Siempre retornar el super() para que los widgets 
        # sigan recibiendo sus eventos normales (clics, teclado, etc.)
        return super().eventFilter(obj, event)
    
    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            # Cambiar a icono de Maximizar
            self.btn_max.setIcon(QIcon("./resources/images/window-maximize-symbolic-svgrepo-com.svg"))
            self.btn_max.setIconSize(QSize(25, 25)) 
            # Restaurar diseño con sombra y bordes
            self.wrapper_layout.setContentsMargins(self.shadow_width, self.shadow_width, 
                                                 self.shadow_width, self.shadow_width)
            self.main_container.setStyleSheet("""
                #main_container { 
                    background-color: #fff; 
                    border-radius: 10px; 
                    border: 1px solid #003366;
                }
            """)
            
            self.btn_close.setStyleSheet("""
                QPushButton { 
                    background-color: transparent;
                    border:none;
                    border-top-right-radius:9px;
                }
                QPushButton::hover{
                    background-color: rgb(232, 17, 35);
                }
            """)
            
            self.title_bar.setStyleSheet(u"QFrame{\n"
                "	background-color: #004080; \n"
                "	padding:0px;\n"
                "}\n"
                "#title_bar{\n"
                "	border-top-right-radius:9px; \n"
                "	border-top-left-radius:9px;\n"
                "\n"
                "}")
        else:
            self.showMaximized()
            # Cambiar a icono de Restaurar
            self.btn_max.setIcon(QIcon("./resources/images/window-restore-symbolic-svgrepo-com.svg"))
            self.btn_max.setIconSize(QSize(25, 25))
            
            # Eliminar márgenes y bordes para que ocupe toda la pantalla limpia
            self.wrapper_layout.setContentsMargins(0, 0, 0, 0)
            self.main_container.setStyleSheet("""
                #main_container { 
                    background-color: #fff; 
                    border-radius: 0px; 
                    border: none;
                }
            """)
            self.btn_close.setStyleSheet("""
                QPushButton { 
                    background-color: transparent;
                    border-radius: 0px;
                    border:none;
                }
                QPushButton::hover{
                    background-color: rgb(232, 17, 35);
                }
            """)
            
            self.title_bar.setStyleSheet(u"QFrame{\n"
                "	background-color: #004080; \n"
                "	padding:0px;\n"
                "}\n"
                "#title_bar{\n"
                "	border-radius:0px; \n"
                "\n"
                "}")

    # --- LÓGICA DE REDIMENSIONADO ---
    def _get_edge(self, pos):
        # No permitir redimensionar cuando la ventana esté maximizada
        if self.isMaximized():
            return None
        w, h = self.width(), self.height()
        x, y = pos.x(), pos.y()
        m = self.margin + self.shadow_width
        #ESQUINAS
        if x < m and y < m: return 'top_left'
        if x > w - m and y < m: return 'top_right'
        if x < m and y > h - m: return 'bottom_left'
        if x > w - m and y > h - m: return 'bottom_right'
        #BORDES
        if x < m: return 'left'
        if x > w - m: return 'right'
        if y < m: return 'top'
        if y > h - m: return 'bottom'
        return None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Si está maximizada, no iniciar redimensionado
            if self.isMaximized():
                if self.title_bar.underMouse():
                    self.drag_pos = event.globalPosition().toPoint()
                return

            edge = self._get_edge(event.position())
            if edge:
                self._resizing = True
                self._resize_edge = edge
            elif self.title_bar.underMouse():
                self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):

        # Si la ventana está maximizada, no procesar redimensionado
        if self.isMaximized():
            # Asegurar que no quedemos en modo redimensionado accidentalmente
            if self._resizing:
                self._resizing = False
                self._resize_edge = None
            return

        if not self._resizing:
            edge = self._get_edge(event.position())
            if edge:

                if edge in ['left', 'right']: self.setCursor(Qt.SizeHorCursor)
                elif edge in ['top', 'bottom']: self.setCursor(Qt.SizeVerCursor)
                elif edge in ['top_left', 'bottom_right']: self.setCursor(Qt.SizeFDiagCursor)
                elif edge in ['top_right', 'bottom_left']: self.setCursor(Qt.SizeBDiagCursor)
            else: 
                self.setCursor(Qt.ArrowCursor)

        if self._resizing:
            rect = self.geometry()
            gp = event.globalPosition().toPoint()
            if 'left' in self._resize_edge: rect.setLeft(gp.x())
            if 'right' in self._resize_edge: rect.setRight(gp.x())
            if 'top' in self._resize_edge: rect.setTop(gp.y())
            if 'bottom' in self._resize_edge: rect.setBottom(gp.y())
            
            if rect.width() > 300 and rect.height() > 200:
                self.setGeometry(rect)
        elif self.drag_pos:
            diff = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.pos() + diff)
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self.drag_pos = None 
        self.setCursor(Qt.ArrowCursor)  
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())