
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QMainWindow,QTableWidgetItem,QHBoxLayout
from PySide6.QtCore import QFile, QIODevice,QUrl,Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings,QWebEnginePage
from modelos.modulo import User,TSession,session,Student
from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from dotenv import load_dotenv


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        load_dotenv()
        self.user_authenticated=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none().user
        self.window=cargar_ui("UI/menu.ui",self)
        self.conectar_eventos()
        self.web()
        self.pag_tabla_estudiantes()
    
    def web(self):
        
        self.window.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.window.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.window.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        #self.disable_features()
        # Cargar el PDF desde fichero local y pedir al visualizador que abra sin la sidebar
        # Añadimos el fragmento 'pagemode=none' (y opcional 'toolbar=0') para cerrar la barra lateral
        file_path = os.getenv('prueba')
        if file_path:
            url = QUrl.fromLocalFile(file_path)
            # Establecer fragmento para controlar la vista del PDF (p.ej. cerrar sidebar)
            # Algunos visores (Chromium) respetan '#pagemode=none' para ocultar miniaturas/bookmarks
            url.setFragment("pagemode=none&toolbar=0")
            self.window.web_view.load(url)
        else:
            QMessageBox.warning(self, "Archivo no encontrado", "No se encontró la ruta al PDF en la variable de entorno 'prueba'.")

    def disable_features(self):
        """Desactivar características específicas del WebEngine"""
        # Desactivar JavaScript si no es necesario
        self.window.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        
        # Desactivar enlaces externos
        #self.window.web_view.page().setLinkDelegationPolicy(QWebEnginePage.DelegateAllLinks)
        
        # Desactivar más características
        #self.window.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.window.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, False)    
    
    def conectar_eventos(self):
        #realizar una clase de usuario autenticado
        self.window.cerrar_sesionButton.clicked.connect(self.logout)
        self.window.usernameLabel.setText(self.user_authenticated.username)
        self.window.rolLabel.setText(self.user_authenticated.rol)
        self.window.InicioButton.clicked.connect(self.change_widget)
        self.window.UsuariosButton.clicked.connect(self.change_widget)
        self.window.EmpresasButton.clicked.connect(self.change_widget)
        self.window.EstudiantesButton.clicked.connect(self.change_widget)
        self.window.TutoresButton.clicked.connect(self.change_widget)
        self.window.nuevostudentButton.clicked.connect(self.open_newstudent)
        self.window.regresarButton.clicked.connect(lambda :self.window.StackedEstudiantes.setCurrentIndex(0))

    def change_widget(self):
        buttom=self.sender()
        if buttom.text().lower()=="inicio":
            self.window.stackedWidget.setCurrentIndex(0)
        elif buttom.text().lower()=="usuarios":
            self.window.stackedWidget.setCurrentIndex(1)
            self.window.StackedEstudiantes.setCurrentIndex(0)
        elif buttom.text().lower()=="estudiantes":
            self.window.stackedWidget.setCurrentIndex(2)
        elif buttom.text().lower()=="tutores":
            self.window.stackedWidget.setCurrentIndex(3)
        elif buttom.text().lower()=="empresas":
            self.window.stackedWidget.setCurrentIndex(4)          
            
    def ver_estudiantes(self):
        self.window.StackedEstudiantes.setCurrentIndex(1)
    
    def pag_tabla_estudiantes(self):
        estudiantes=session.query(Student).all()
        tabla=self.window.tabla_estudiantes
        tabla.setRowCount(0)
        for fila,estudiante in enumerate(estudiantes):
            tabla.insertRow(fila)
            
            tabla.setItem(fila,0,QTableWidgetItem(str(estudiante.cedula)))
            tabla.setItem(fila,1,QTableWidgetItem(str(estudiante.primer_nombre)))
            tabla.setItem(fila,2,QTableWidgetItem(str(estudiante.segundo_nombre if estudiante.segundo_nombre else "")))
            tabla.setItem(fila,3,QTableWidgetItem(str(estudiante.primer_apellido)))
            tabla.setItem(fila,4,QTableWidgetItem(estudiante.segundo_apellido))
            tabla.setItem(fila,5,QTableWidgetItem(str(estudiante.email)))
            tabla.setItem(fila,6,QTableWidgetItem(str(estudiante.carrera)))
            tabla.setItem(fila,7,QTableWidgetItem(str(estudiante.telefono)))
                       
            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 

            boton_ver=QPushButton("Ver")
            boton_ver.clicked.connect(lambda : self.window.StackedEstudiantes.setCurrentIndex(1))
            btn_editar = QPushButton("Editar")
            btn_borrar = QPushButton("Borrar")

            btn_editar.setStyleSheet("background-color: #4CAF50; color: white;") 
            btn_borrar.setStyleSheet("background-color: #f44336; color: white;")                 
            boton_ver.setStyleSheet("background-color: #3d8ec9; color: white; font-weight: bold;") 

            layout_botones.addWidget(boton_ver)
            layout_botones.addWidget(btn_editar)
            layout_botones.addWidget(btn_borrar)

            # 6. Insertar el contenedor en la celda
            tabla.setCellWidget(fila, 8, widget_contenedor)
        # Esto elimina todas las filas, pero DEJA los títulos de las columnas intactos.
        
    
    def open_newstudent(self):
        from admin.nuevo_estudiante import NewStudent
        self.newstudent_window=NewStudent()
        self.newstudent_window.exec()
        self.pag_tabla_estudiantes()
        

    def logout(self):
        sesion_mac=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none()
        if sesion_mac:
            session.delete(sesion_mac)
            session.commit()
        self.close()
        from iniciar_sesion.login import Login
        self.login = Login()
        self.login.show()



        
    