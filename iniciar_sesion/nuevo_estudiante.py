import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox,QMainWindow
# from PySide6.QtCore import QFile, QIODevice
# from PySide6.QtUiTools import QUiLoader
from modelos.modulo import Student,session
# from getmac import get_mac_address as gma
from iniciar_sesion.plantilla_ui import cargar_ui

from dotenv import load_dotenv


class NewStudent:
    
    def __init__(self):
        load_dotenv()
        self.window=cargar_ui("new_student.ui")
        self.conectar_eventos()
    
    def exec(self):
        self.window.exec()
    
    def close(self):
        self.window.close()   
    
    def registrar(self):

        estudiante=Student(primer_nombre=self.window.primernombre_input.text(),
                           segundo_nombre=self.window.segundonombre_input.text(),
                           primer_apellido=self.window.primerapellido_input.text(),
                           segundo_apellido=self.window.segundoapellido_input.text(),
                           cedula=int(self.window.cedula_input.text()),
                           telefono=self.window.telefono_input.text(),
                           email=self.window.email_input.text(),
                           carrera=self.window.carrera_input.text(),
                           semestre=int(self.window.semestre_input.text()),
                           direccion="Barinas")
        session.add(estudiante)
        session.commit()
        QMessageBox.information(self.window,"Usuario creado",
                                    "Se a registrado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    def conectar_eventos(self):
        self.window.RegistrarButton.clicked.connect(self.registrar)

    
    


    

    



        
    