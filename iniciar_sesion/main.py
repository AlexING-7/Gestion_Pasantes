
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
import modelos.modulo as db
from getmac import get_mac_address as gma
from plantilla_ui import cargar_ui

User=db.User
TSession=db.TSession
session=db.session

class MainWindow:
    
    def __init__(self):
        self.user_authenticated=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none().user
        self.window=cargar_ui("dashboard.ui")
        self.conectar_eventos()
    
    def show(self):
        self.window.show()
    
    def close(self):
        self.window.close()    
    
    def conectar_eventos(self):
        #realizar una clase de usuario autenticado
        self.window.cerrar_sesionButton.clicked.connect(self.logout)
        self.window.usernameLabel.setText(self.user_authenticated.username)
        self.window.rolLabel.setText(self.user_authenticated.rol)
    
    def logout(self):
        sesion_mac=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none()
        if sesion_mac:
            session.delete(sesion_mac)
            session.commit()
        self.close()
        from login import Login
        self.login = Login()
        self.login.show()



        
    