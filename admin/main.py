
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QMessageBox,QMainWindow
from PySide6.QtCore import QUrl,Qt
from PySide6.QtWebEngineCore import QWebEngineSettings,QWebEnginePage
from modelos.modulo import User,TSession,session

from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui

from dotenv import load_dotenv
from admin.main_estudiantes import StackStudent
from admin.main_empresa import StackEnterprise
from admin.main_tutor_academico import StackTutorA
from admin.main_tutor_empresarial import StackTutorE
from admin.main_pasante import StackPasante


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        load_dotenv()
        self.user_authenticated=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none().user
        self.window=cargar_ui("UI/menu.ui",self)
        self.setWindowTitle("menu")
        self.resize(1120, 680)
        self.conectar_eventos()
        #self.web()
        
        

        
    
    def eventFilter(self, source, event):
        if self.window.stackedWidget.currentIndex()==2:
            self.student.eventFilter(source,event)
        elif self.window.stackedWidget.currentIndex()==3:
            self.enterprise.eventFilter(source,event)
        elif self.window.stackedWidget.currentIndex()==4:
            self.tutorA.eventFilter(source,event)
        elif self.window.stackedWidget.currentIndex()==5:
            self.tutorE.eventFilter(source,event)
        elif self.window.stackedWidget.currentIndex()==6:
            self.pasante.eventFilter(source,event)
            
        return super().eventFilter(source, event) 
    
    def conectar_eventos(self):
        #realizar una clase de usuario autenticado
        self.window.stackedWidget.setCurrentIndex(0)
        self.window.cerrar_sesionButton.clicked.connect(self.logout)
        self.window.usernameLabel.setText(self.user_authenticated.username)
        self.window.rolLabel.setText(self.user_authenticated.rol)
        self.window.InicioButton.clicked.connect(self.change_widget)
        self.window.UsuariosButton.clicked.connect(self.change_widget)
        self.window.EmpresasButton.clicked.connect(self.change_widget)
        self.window.EstudiantesButton.clicked.connect(self.change_widget)
        self.window.TutoresButton.clicked.connect(self.change_widget)
        self.window.TutoresEButton.clicked.connect(self.change_widget)
        self.window.PasantiasButton.clicked.connect(self.change_widget)
        self.window.confButton.clicked.connect(self.change_widget)
        
        
        
    def change_widget(self):
        buttom=self.sender()
        if buttom.text().lower()=="inicio":
            self.window.stackedWidget.setCurrentIndex(0)
        elif buttom.text().lower()=="usuarios":
            self.window.stackedWidget.setCurrentIndex(1)
        elif buttom.text().lower()=="estudiantes":
            self.student=StackStudent(self)
            self.window.stackedWidget.setCurrentIndex(2)          
        elif buttom.text().lower()=="empresas":
            self.enterprise=StackEnterprise(self)
            self.window.stackedWidget.setCurrentIndex(3)
        elif buttom.text().lower()=="tutores acad.":
            self.tutorA=StackTutorA(self)
            self.window.stackedWidget.setCurrentIndex(4)        
        elif buttom.text().lower()=="tutores empr.":
            self.tutorE=StackTutorE(self)
            self.window.stackedWidget.setCurrentIndex(5)
        elif buttom.text().lower()=="pasantias":
            self.pasante=StackPasante(self)
            self.window.stackedWidget.setCurrentIndex(6)
        elif buttom.text().lower()=="configuración":
            self.window.stackedWidget.setCurrentIndex(7)          
                     
    def logout(self):
        sesion_mac=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none()
        if sesion_mac:
            session.delete(sesion_mac)
            session.commit()
        self.close()
        from iniciar_sesion.login import Login
        self.login = Login()
        self.login.show()



        
    