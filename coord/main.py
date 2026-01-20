
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
from admin.main_estudiantes import StackStudent
from admin.main_empresa import StackEnterprise
from admin.main_tutor_academico import StackTutorA
from admin.main_tutor_empresarial import StackTutorE
from admin.main_pasante import StackPasante
from PySide6.QtWidgets import QHeaderView  # O PySide6.QtWidgets

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        load_dotenv()
        self.user_authenticated=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none().user
        self.window=cargar_ui("UI/dashboard.ui",self)
        self.setWindowTitle("menu")
        self.resize(1120, 680)
        self.conectar_eventos()
        

    def conectar_eventos(self):
        #realizar una clase de usuario autenticado
        pass
        
    def change_widget(self):
        buttom=self.sender()
        if buttom.text().lower()=="Solicitudes".lower():
            self.window.stackedWidget.setCurrentIndex(1)
            
        elif buttom.text().lower()=="Generación de Docs".lower():
            self.window.stackedWidget.setCurrentIndex(0)
            self.window.listWidget.setCurrentRow(0)
            
            # Create the custom widget
            widget = QWidget()
            widget.setStyleSheet("background-color: white;")
            layout = QHBoxLayout(widget)
            label = QLabel("documento")
            layout.addWidget(label)
            button = QPushButton("generar")
            button.setStyleSheet("background-color: blue; color: white;")
            layout.addWidget(button)
            
            # Create list item
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.window.listWidget.addItem(item)
            self.window.listWidget.setItemWidget(item, widget)


      
                     
    def logout(self):
        sesion_mac=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none()
        if sesion_mac:
            session.delete(sesion_mac)
            session.commit()
        self.close()
        from iniciar_sesion.login import Login
        self.login = Login()
        self.login.show()



        
    