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
            if not self._resizing and not self.drag_pos:
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
                    self.drag_pos = event.position().toPoint()
                return

            edge = self._get_edge(event.position())
            if edge:
                self._resizing = True
                self._resize_edge = edge
            elif self.title_bar.underMouse():
                self.drag_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        gp = event.globalPosition().toPoint()

        # 1. GESTIÓN DEL CURSOR (Solo si no estamos redimensionando ni moviendo)
        if not self._resizing and not self.drag_pos:
            edge = self._get_edge(pos)
            if edge:
                if edge in ['left', 'right']: self.setCursor(Qt.SizeHorCursor)
                elif edge in ['top', 'bottom']: self.setCursor(Qt.SizeVerCursor)
                elif edge in ['top_left', 'bottom_right']: self.setCursor(Qt.SizeFDiagCursor)
                elif edge in ['top_right', 'bottom_left']: self.setCursor(Qt.SizeBDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        # 2. LÓGICA DE REDIMENSIONADO (Solo si no está maximizada)
        if self._resizing and not self.isMaximized():
            rect = self.geometry()
            if 'left' in self._resize_edge: rect.setLeft(gp.x())
            if 'right' in self._resize_edge: rect.setRight(gp.x())
            if 'top' in self._resize_edge: rect.setTop(gp.y())
            if 'bottom' in self._resize_edge: rect.setBottom(gp.y())
            
            if rect.width() > 300 and rect.height() > 200:
                self.setGeometry(rect)
            return # Finalizar aquí si estamos redimensionando

        # 3. LÓGICA DE ARRASTRE (DRAG) Y DESPEGUE

        # 3. LÓGICA DE ARRASTRE (DRAG) Y DESPEGUE
        elif self.drag_pos:
            if self.isMaximized():
                # 1. Guardar la posición global actual del ratón
                current_global_pos = gp
                
                # 2. Calcular qué porcentaje del ancho total representa el click original
                # (Ej: si hiciste clic a la mitad, el factor es 0.5)
                prev_width = self.width()
                factor = self.drag_pos.x() / prev_width
                
                # 3. Restaurar la ventana (esto cambia el tamaño a 'normal')
                self._toggle_maximize() 
                
                # 4. Calcular el nuevo punto X relativo al nuevo tamaño de ventana
                # Para que el cursor siga en el mismo lugar proporcional
                new_local_x = int(self.width() * factor)
                new_local_y = self.title_bar.height() // 2 # Centramos verticalmente en la barra
                
                # 5. Mover la ventana para que el cursor coincida con el punto local calculado
                self.move(current_global_pos.x() - new_local_x, 
                          current_global_pos.y() - new_local_y)
                
                # 6. ACTUALIZACIÓN CRUCIAL: Redefinir drag_pos con la nueva escala
                # Sin esto, en el siguiente píxel de movimiento, la ventana "saltará"
                self.drag_pos = QPoint(new_local_x, new_local_y)
                
            else:
                # Arrastre normal: mover la ventana la distancia que se movió el ratón
                # usando la diferencia entre la posición global y el anclaje local original
                self.move(gp - self.drag_pos)

                
    def mouseReleaseEvent(self, event):
        self._resizing = False
        self.drag_pos = None 
        self.setCursor(Qt.ArrowCursor)  
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())