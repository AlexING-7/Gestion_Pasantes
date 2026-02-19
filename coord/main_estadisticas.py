import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QListWidgetItem

from modelos.modulo import session,Evaluacion,Pasantia,Enterprise,Tutor_Academico
from sqlalchemy import select,func
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
         
        
        self.window.stackedWidget.setCurrentIndex(6)
        self.window.stackedEst.setCurrentIndex(0)
        self.conectar_eventos()

    def ir_a_siguiente(self):
        indice_actual = self.window.stackedEst.currentIndex()
        total_paginas = self.window.stackedEst.count()
        proximo_indice = (indice_actual + 1) % total_paginas
        self.window.stackedEst.setCurrentIndex(proximo_indice)
        
    def ir_a_anterior(self):
        indice_actual = self.window.stackedEst.currentIndex()
        total_paginas = self.window.stackedEst.count()
        indice_anterior = (indice_actual - 1 + total_paginas) % total_paginas
        self.window.stackedEst.setCurrentIndex(indice_anterior)


    def get_empresas(self)->dict:
        try:
            empresas = session.scalars(select(Enterprise)).all()
            empresas = dict((str(e.razon_social),len(e.pasantias)) for e in empresas)
            return empresas if empresas else {"0":0}
        except Exception:
            return {"0":0}

    def get_notas(self):
        try:
            stmt=select(Pasantia.lapso_academico,func.round(func.avg(Evaluacion.nota_tutor_aca),2).label("promedioA"),func.round(func.avg(Evaluacion.nota_tutor_emp),2).label("promedioB")).join(Evaluacion.pasantia).group_by(Pasantia.lapso_academico)
            notas=session.execute(stmt).all()
            return notas
        except Exception as e:
            return e
        
    def get_carrera(self):
        stmt=select(Pasantia.carrera,func.count(Pasantia.id).label("cantidad")).group_by(Pasantia.carrera) 
        carreras=session.execute(stmt).all()
        return carreras
    def get_cargaAcad(self):
        stmt=select(Tutor_Academico.primer_nombre,Tutor_Academico.primer_apellido,func.count(Pasantia.id).label("pasantes")).join(Tutor_Academico.pasantias).group_by(Tutor_Academico.primer_nombre,Tutor_Academico.primer_apellido).limit(5)
        tutores=session.execute(stmt).all()
        return tutores
    def conectar_eventos(self):
        self.window.btnAntEst.clicked.connect(self.ir_a_anterior)
        self.window.btnSigEst.clicked.connect(self.ir_a_siguiente)
        self.estadistica1()
        self.estadistica2()
        self.estadistica3()
        self.estadistica4()
    
    def estadistica1(self):
        from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
        from PySide6.QtGui import QPainter, QColor
        from PySide6.QtCore import Qt

        notas=self.get_notas()
        
        lapsos = [i.lapso_academico for i in notas]
        cantidades1 = [i.promedioA for i in notas]
        cantidades2=[i.promedioB for i in notas]
        set_notaAcad = QBarSet("Notas Academicas")
        set_notaEmpr = QBarSet("Notas Empresariales")
        set_notaAcad.append(cantidades1)
        set_notaEmpr.append(cantidades2)
        
        # Opcional: Personalizar color de las barras
        set_notaAcad.setColor(QColor(52, 152, 219)) # Azul "Peter River"
        set_notaEmpr.setColor(QColor(87, 174, 209)) 
        # La 'QBarSeries' agrupa los sets (en este caso solo uno)
        series = QBarSeries()
        series.append(set_notaAcad)
        series.append(set_notaEmpr)
        #series.setLabelsVisible(True) # Mostrar el número encima de la barra

        # ---------------------------------------------------------
        # 3. CREAR EL CHART (El Lienzo)
        # ---------------------------------------------------------
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Acad vs Empr")
        chart.setAnimationOptions(QChart.SeriesAnimations) # Animación suave
        
        # Truco: Usar un tema predefinido para que se vea bonito rápido
        # chart.setTheme(QChart.ChartThemeLight) 

        # ---------------------------------------------------------
        # 4. CREAR Y CONFIGURAR EJES (Las Reglas)
        # ---------------------------------------------------------
        
        # Eje X: Categorías (Texto)
        axis_x = QBarCategoryAxis()
        axis_x.append(lapsos) # Aquí van los nombres de las carreras
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x) # IMPORTANTE: Atar eje a la serie

        # Eje Y: Valores (Números)
        axis_y = QValueAxis()
        axis_y.setRange(0, 20) # De 0 a un poco más del máximo (22)
        axis_y.setTitleText("Promedio")
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

        dato=self.get_carrera()
        carreras = [i.carrera for i in dato]
        cantidades = [i.cantidad for i in dato]
        set_pasantes = QBarSet("Cantidad de Pasantes")
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
        from PySide6.QtCharts import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
        from PySide6.QtGui import QPainter, QColor
        from PySide6.QtCore import Qt

        dato=self.get_cargaAcad()
        tutores = [f"{i.primer_nombre[0]}. {i.primer_apellido}" for i in dato]
        cantidades = [i.pasantes for i in dato]
        set_pasantes = QBarSet("Cantidad de Pasantes")
        set_pasantes.append(cantidades)
        
        # Opcional: Personalizar color de las barras
        set_pasantes.setColor(QColor(52, 152, 219)) # Azul "Peter River"

        # La 'QBarSeries' agrupa los sets (en este caso solo uno)
        series = QHorizontalBarSeries()
        series.append(set_pasantes)
        series.setLabelsVisible(True) # Mostrar el número encima de la barra

        # ---------------------------------------------------------
        # 3. CREAR EL CHART (El Lienzo)
        # ---------------------------------------------------------
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Distribución de Carga Academica por Tutor Academico")
        chart.setAnimationOptions(QChart.SeriesAnimations) # Animación suave
        
        # Truco: Usar un tema predefinido para que se vea bonito rápido
        # chart.setTheme(QChart.ChartThemeLight) 

        # ---------------------------------------------------------
        # 4. CREAR Y CONFIGURAR EJES (Las Reglas)
        # ---------------------------------------------------------
        
        # Eje Y: Categorías (Texto)
        axis_y = QBarCategoryAxis()
        axis_y.append(tutores) # Aquí van los nombres de las carreras
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y) # IMPORTANTE: Atar eje a la serie

        # Eje X: Valores (Números)
        axis_x = QValueAxis()
        axis_x.setRange(0, 10) # De 0 a un poco más del máximo (22)
        axis_x.setTitleText("Cantidad de Estudiantes")
        axis_x.setLabelFormat("%d") # Mostrar enteros (sin decimales)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x) # IMPORTANTE: Atar eje a la serie

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
        axis_y.setRange(0, 20) # De 0 a un poco más del máximo (22)
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

if __name__=="__main__":
        stmt=select(Tutor_Academico.primer_nombre,Tutor_Academico.primer_apellido,func.count(Pasantia.id).label("pasantes")).join(Tutor_Academico.pasantias).group_by(Tutor_Academico.primer_nombre,Tutor_Academico.primer_apellido)
        tutores=session.execute(stmt).all()
        print(tutores)