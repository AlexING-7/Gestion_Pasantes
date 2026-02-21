
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
from coord.main_estadisticas import StackEstadistica
from coord.main_documentos import StackedDocumentos
from herramientas.logs import registrar_log
from herramientas.CustomMain import CustomWindow
from admin.main_empresa import StackEnterprise
from admin.main_tutor_academico import StackTutorA
from admin.main_tutor_empresarial import StackTutorE
class MainWindow(CustomWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        load_dotenv()
        self.user_authenticated=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none().user
        self.window=cargar_ui("UI/dashboard.ui",self)
        self.layout_principal.addWidget(self.window)
        self.title_label.setText("Sitema de Gestión de Pasantias-Coordinador")
        self.setMinimumSize(1175,800)
        self.resize(1200, 850)
        self.conectar_eventos()
        
    def eventFilter(self, source, event):
        # Evitar errores si `self.window` aún no fue asignado
        win = getattr(self, 'window', None)
        if win is None or not hasattr(win, 'stackedWidget'):
            return super().eventFilter(source, event)

        idx = win.stackedWidget.currentIndex()
        if idx==0 and hasattr(self, 'soli'):
            pass#self.log.eventFilter(source, event)
        if idx == 1 and hasattr(self, 'pasantes'):
            pass#self.student.eventFilter(source, event)
        elif idx == 2 and hasattr(self, 'empresa'):
            self.empresa.eventFilter(source, event)
        elif idx == 3 and hasattr(self, 'tutorA'):
            self.tutorA.eventFilter(source, event)
        elif idx == 4 and hasattr(self, 'tutorE'):
            self.tutorE.eventFilter(source, event)


        return super().eventFilter(source, event)        

    def conectar_eventos(self):
        self.window.stackedWidget.setCurrentIndex(0)
        self.window.usernameLabel.setText(self.user_authenticated.username)
        self.window.rolLabel.setText(self.user_authenticated.rol)
        self.window.cerrar_sesionButton.clicked.connect(self.logout)
        self.window.btnGen.clicked.connect(self.change_widget)
        self.window.btnSolicitud.clicked.connect(self.change_widget)
        self.window.btnPasante.clicked.connect(self.change_widget)
        self.window.btnEstadistica.clicked.connect(self.change_widget)
        self.window.btnEmpresa.clicked.connect(self.change_widget)
        self.window.btnTutorA.clicked.connect(self.change_widget)
        self.window.btnTutorE.clicked.connect(self.change_widget)
        self.window.btnSolicitud.click()
    
        
    def change_widget(self):
        buttom=self.sender()
        if buttom.text().lower()=="Solicitudes".lower():
            self.soli=StackedSolicitud(self)
            
        elif buttom.text().lower()=="pasantes".lower():
            self.pasante=StackPasante(self)   
            
        elif buttom.text().lower()=="empresas".lower():
            self.window.stackedWidget.setCurrentIndex(2)
            self.empresa=StackEnterprise(self)
            self.empresa.pag_tabla_empresa()
        elif buttom.text().lower()=="tutor academico".lower():
            self.window.stackedWidget.setCurrentIndex(3)
            self.tutorA=StackTutorA(self)
            self.tutorA.pag_tabla_tutorA()
        elif buttom.text().lower()=="tutor empresarial".lower():
            self.window.stackedWidget.setCurrentIndex(4)
            self.tutorE=StackTutorE(self)
            self.tutorE.pag_tabla_tutorE()
        elif buttom.text().lower()=="Generación de Docs".lower():
            self.docs=StackedDocumentos(self)
            
        elif buttom.text().lower()=="Estadisticas".lower():
            self.esta=StackEstadistica(self)
      
                     
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



        
    