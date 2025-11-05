
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
# from PySide6.QtWidgets import QWidget, QLabel, QMessageBox
# from PySide6.QtCore import QFile, QIODevice
# from PySide6.QtUiTools import QUiLoader
# import modelos.modulo as db
# from getmac import get_mac_address as gma
from plantilla_ui import cargar_ui

# User=db.User
# TSession=db.TSession
# session=db.session

class RecoveryWindow:
    
    def __init__(self):
        self.window=cargar_ui("recovery.ui")
        self.conectar_eventos()
    
    def show(self):
        self.window.show()
    
    def close(self):
        self.window.close()    
    
    def conectar_eventos(self):
        #realizar una clase de usuario autenticado
        pass
    
    



        
    