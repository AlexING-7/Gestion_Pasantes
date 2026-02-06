
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
        self.setMinimumSize(1150,750)
        self.resize(1200, 850)
        self.conectar_eventos()
        

    def conectar_eventos(self):
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
            StackedSolicitud(self)
           
        elif buttom.text().lower()=="pasantes".lower():
            StackPasante(self)
            

        elif buttom.text().lower()=="empresas".lower():
            self.window.stackedWidget.setCurrentIndex(2)
            self.empresa=StackEnterprise(self)
        
        elif buttom.text().lower()=="tutor academico".lower():
            self.window.stackedWidget.setCurrentIndex(3)
            self.tutorA=StackTutorA(self)
        
        elif buttom.text().lower()=="tutor empresarial".lower():
            self.window.stackedWidget.setCurrentIndex(4)
            self.TutorE=StackTutorE(self)
        
        elif buttom.text().lower()=="Generación de Docs".lower():
            self.docs=StackedDocumentos(self)
        elif buttom.text().lower()=="Estadisticas".lower():
            StackEstadistica(self)
      
                     
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



        
    