
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



        
    