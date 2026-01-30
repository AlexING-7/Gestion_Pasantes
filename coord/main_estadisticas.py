import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QListWidgetItem

from modelos.modulo import session,Student,Pasantia,Enterprise
from sqlalchemy import select
from sqlalchemy import or_,and_, cast, String
from getmac import get_mac_address as gma
from herramientas.widgets_personalizados import MiWidgetClickeable
from herramientas.plantilla_ui import cargar_ui
from herramientas.conversiones import null_string,calcular_edad,calcular_duracion_meses,convertir_pil_a_pixmap,formato_miles,guion_telefono
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent,QSize

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class StackEstadistica():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.current_pasante = None
         
        self.conectar_eventos()
        self.window.stackedWidget.setCurrentIndex(6)

    def get_empresas(self)->dict:
        try:
            empresas = session.scalars(select(Enterprise)).all()
            empresas = dict((str(e.razon_social),len(e.pasantias)) for e in empresas)
            return empresas if empresas else {"0":0}
        except Exception:
            return {"0":0}

    def conectar_eventos(self):
        self.estadistica1()
        self.estadistica2()
        self.estadistica3()
        self.estadistica4()
    
    def estadistica1(self):
        from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
        from PySide6.QtGui import QPainter, QColor
        from PySide6.QtCore import Qt
        
        self.window.stackedWidget.setCurrentIndex(6)
        carreras = ["hola","adios"]
        cantidades = [0] * len(carreras)
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
        self.window.verticalEst1.addWidget(chart_view)
        
    def estadistica2(self):
        from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
        from PySide6.QtGui import QPainter, QColor
        from PySide6.QtCore import Qt
        self.window.stackedWidget.setCurrentIndex(6)
        carreras = ["hola","adios"]
        cantidades = [0] * len(carreras)
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
        self.window.verticalEst2.addWidget(chart_view)
        
    def estadistica3(self):
        from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
        from PySide6.QtGui import QPainter, QColor
        from PySide6.QtCore import Qt
        self.window.stackedWidget.setCurrentIndex(6)
        carreras = ["hola","adios"]
        cantidades = [0] * len(carreras)
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
        self.window.verticalEst3.addWidget(chart_view)
        
    def estadistica4(self):
        from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
        from PySide6.QtGui import QPainter, QColor
        from PySide6.QtCore import Qt
        self.window.stackedWidget.setCurrentIndex(6)
        carreras = list(self.get_empresas().keys())
        cantidades = list(self.get_empresas().values())
        set_pasantes = QBarSet("Empresas Con Mas Pasantes")
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
        axis_y.setTitleText("Cantidad de Pasantes")
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
        self.window.verticalEst4.addWidget(chart_view)

    