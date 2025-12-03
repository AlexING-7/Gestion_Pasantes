import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox,QMainWindow
# from PySide6.QtCore import QFile, QIODevice
# from PySide6.QtUiTools import QUiLoader
import modelos.modulo as db
# from getmac import get_mac_address as gma
from iniciar_sesion.plantilla_ui import cargar_ui

from dotenv import load_dotenv

User=db.User
TSession=db.TSession
session=db.session

class NewStudent(QMainWindow):
    
    def __init__(self):
        load_dotenv()
        self.window=cargar_ui("new_student.ui",self)
    

    
    


    

    



        
    