
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox,QMainWindow,QFileDialog
from PySide6.QtCore import QFile, QIODevice,QUrl,Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings,QWebEnginePage
import modelos.modulo as db
from getmac import get_mac_address as gma
from plantilla_ui import cargar_ui

User=db.User
TSession=db.TSession
session=db.session

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        self.user_authenticated=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none().user
        self.window=cargar_ui("dashboard.ui",self)
        self.conectar_eventos()
        self.web()
    
    def web(self):
        
        self.window.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.window.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.window.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        #self.disable_features()
        url = QUrl.fromLocalFile("C:Users/HP/Desktop/Gestion_Pasantes/prueba.pdf")
        self.window.web_view.load(url)

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
    
    def logout(self):
        sesion_mac=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none()
        if sesion_mac:
            session.delete(sesion_mac)
            session.commit()
        self.close()
        from login import Login
        self.login = Login()
        self.login.show()



        
    