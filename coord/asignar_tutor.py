import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
import shutil
from datetime import datetime
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox,QMainWindow, QFileDialog
from PySide6.QtGui import QRegularExpressionValidator, QValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QFile, Qt, QDate
# from PySide6.QtUiTools import QUiLoader
from modelos.modulo import Pasantia,Tutor_Academico,Student,Enterprise,Tutor_Empresarial,session
# from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui

from dotenv import load_dotenv


class NewAsignar:
    
    def __init__(self,pasante:Pasantia):
        self.pasante=pasante
        self.tutorA=session.query(Tutor_Academico).all()
        self.window=cargar_ui("UI/asignartutor.ui")
        self.conectar_eventos()
    
    def exec(self):
        self.window.exec()
    
    def close(self):
        self.window.close()   
    
    def listas(self):
        for tutorA in self.tutorA:
            self.window.input_tutor.addItem(f"{tutorA.primer_nombre}:{tutorA.cedula},",tutorA)
            

    def actualizar(self):
        self.datos_pasante(self.pasante)
        session.commit()
        QMessageBox.information(self.window,"Pasante Actualizado",
                                    "Se a actualizado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    
    def datos_pasante(self,pasantia:Pasantia):                       
        pasantia.tutor_academico=self.window.input_tutor.currentData()

    
    
    def conectar_eventos(self):
        self.listas()
        self.datos()
        self.window.btnAsignar.setText("Asignar")
        self.window.btnAsignar.clicked.connect(self.actualizar)

    def datos(self):
        index2=self.window.input_tutor.findData(self.pasante.tutor_academico)
        self.window.input_tutor.setCurrentIndex(index2)

        
        
               
    def validaciones(self):
        rx_nombre = QRegularExpression(r"^[a-zA-ZÁÉÍÓÚÑáéíóúñ\s']+$")
        validator_nombre = QRegularExpressionValidator(rx_nombre)
        
        self.window.primernombre_input.setValidator(validator_nombre)
        self.window.segundonombre_input.setValidator(validator_nombre)
        self.window.primerapellido_input.setValidator(validator_nombre)
        self.window.segundoapellido_input.setValidator(validator_nombre)
        self.window.especialidad_input.setValidator(validator_nombre)
        #_______________________________________________________________
        rx = QRegularExpression(r"^\d{5,9}$")
        val = QRegularExpressionValidator(rx)
        
        self.window.cedula_input.setValidator(val)
        
        #_______________________________________________________________
        rx_tlf = QRegularExpression(r"^(0412|0422|0414|0424|0416|0426|02\d{2})\d{7}$")
        validator_tlf = QRegularExpressionValidator(rx_tlf)
        
        self.window.telefono_input.setValidator(validator_tlf)
        
        #_______________________________________________________________
        email_regex = QRegularExpression(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        validator = QRegularExpressionValidator(email_regex)
        
        self.window.email_input.setValidator(validator)
        
        #_______________________________________________________________
        #self.window.semestre_input.
        #self.window.direccion_input.
        #self.window.genero_input.
    


    

    



        
    