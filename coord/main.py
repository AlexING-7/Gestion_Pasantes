
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QMessageBox,QMainWindow, QLabel, QPushButton, QListWidgetItem, QHBoxLayout, QWidget
from PySide6.QtCore import QUrl,Qt
from PySide6.QtWebEngineCore import QWebEngineSettings,QWebEnginePage
from modelos.modulo import User,TSession,session

from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui

from dotenv import load_dotenv
from PySide6.QtCore import QSize, Qt # O PySide6.QtWidgets
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from coord.main_solicitud import StackedSolicitud
from coord.main_pasante import StackPasante
from herramientas.logs import registrar_log

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        load_dotenv()
        self.user_authenticated=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none().user
        self.window=cargar_ui("UI/dashboard.ui",self)
        self.setWindowTitle("Sistema")
        self.resize(1120, 700)
        self.conectar_eventos()
        

    def conectar_eventos(self):
        self.window.cerrar_sesionButton.clicked.connect(self.logout)
        self.window.btnGen.clicked.connect(self.change_widget)
        self.window.btnSolicitud.clicked.connect(self.change_widget)
        self.window.btnPasante.clicked.connect(self.change_widget)
        self.window.btnEstadistica.clicked.connect(self.change_widget)
        self.window.btnSolicitud.click()
        
    def change_widget(self):
        buttom=self.sender()
        if buttom.text().lower()=="Solicitudes".lower():
            StackedSolicitud(self)
           
        elif buttom.text().lower()=="pasantes".lower():
            StackPasante(self)
            

        elif buttom.text().lower()=="empresas".lower():
            self.window.stackedWidget.setCurrentIndex(2)

        
        elif buttom.text().lower()=="tutor academico".lower():
            self.window.stackedWidget.setCurrentIndex(3)
        
        elif buttom.text().lower()=="tutor empresarial".lower():
            self.window.stackedWidget.setCurrentIndex(4)

        
        elif buttom.text().lower()=="Generación de Docs".lower():
            self.window.stackedWidget.setCurrentIndex(5)
            self.window.listWidget.setCurrentRow(0)
            
            docs=("1. CARTA SOLICITUD DE PASANTIA","2.CARTA ACEPTACION DEL PASANTE","3.ACTA DE INICIO","4.ACTA DE INICIO DE EJECUCIÓN DE PASANTÍA","5.CONTRATO DEL PASANTE","6. INSCRIPCION DE PASANTIA","16.CARTA DE RESPUESTA A SOLICITUD DE EXTENSIÓN DE PASANTIAS")
            for i in docs:
            
                btn=cargar_ui("UI/generar_doc.ui",self)
                btn.label_Documento.setText(i)
                item = QListWidgetItem()
                item.setSizeHint(QSize(430,82))
                print(btn.sizeHint())
                self.window.listWidget.addItem(item)
                self.window.listWidget.setItemWidget(item, btn)
        elif buttom.text().lower()=="Estadisticas".lower():
            from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
            from PySide6.QtGui import QPainter, QColor
            from PySide6.QtCore import Qt
            self.window.stackedWidget.setCurrentIndex(6)
            carreras = ["Ing. Sistemas", "Administración", "Contaduría", "Diseño Gráfico", "Marketing"]
            cantidades = [14, 22, 10, 5, 8]
            set_pasantes = QBarSet("Pasantes Activos")
            set_pasantes.append(cantidades)
            
            # Opcional: Personalizar color de las barras
            set_pasantes.setColor(QColor(52, 152, 219)) # Azul "Peter River"

            # La 'QBarSeries' agrupa los sets (en este caso solo uno)
            series = QBarSeries()
            series.append(set_pasantes)
            series.setLabelsVisible(True) # Mostrar el número encima de la barra

            # ---------------------------------------------------------
            # 3. CREAR EL CHART (El Lienzo)
            # ---------------------------------------------------------
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Distribución de Pasantes por Carrera - 2024")
            chart.setAnimationOptions(QChart.SeriesAnimations) # Animación suave
            
            # Truco: Usar un tema predefinido para que se vea bonito rápido
            # chart.setTheme(QChart.ChartThemeLight) 

            # ---------------------------------------------------------
            # 4. CREAR Y CONFIGURAR EJES (Las Reglas)
            # ---------------------------------------------------------
            
            # Eje X: Categorías (Texto)
            axis_x = QBarCategoryAxis()
            axis_x.append(carreras) # Aquí van los nombres de las carreras
            chart.addAxis(axis_x, Qt.AlignBottom)
            series.attachAxis(axis_x) # IMPORTANTE: Atar eje a la serie

            # Eje Y: Valores (Números)
            axis_y = QValueAxis()
            axis_y.setRange(0, 30) # De 0 a un poco más del máximo (22)
            axis_y.setTitleText("Cantidad de Estudiantes")
            axis_y.setLabelFormat("%d") # Mostrar enteros (sin decimales)
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_y) # IMPORTANTE: Atar eje a la serie

            # ---------------------------------------------------------
            # 5. MOSTRAR EN LA VENTANA (El Marco)
            # ---------------------------------------------------------
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            
            chart_view = QChartView(chart) 
        
        # 4. INSERTAR EL QCHARTVIEW EN EL LAYOUT
        # Aquí es donde el gráfico se "pega" a la ventana
            self.window.verticalLayout_60.addWidget(chart_view)
      
                     
    def logout(self):
        sesion_mac=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none()
        if sesion_mac:
            session.delete(sesion_mac)
            session.commit()
        self.close()
        registrar_log(session=session,
                              usuario=self.user_authenticated.username,
                              accion="LOGOUT",
                              mensaje="Logout Rol Coordinador",
                              )
        from iniciar_sesion.login import Login
        self.login = Login()
        self.login.show()



        
    