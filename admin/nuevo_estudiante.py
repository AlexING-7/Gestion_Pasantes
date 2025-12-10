import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox,QMainWindow
# from PySide6.QtCore import QFile, QIODevice
# from PySide6.QtUiTools import QUiLoader
from modelos.modulo import Student,session
# from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui

from dotenv import load_dotenv


class NewStudent:
    
    def __init__(self,estudiante=None):
        load_dotenv()
        self.estudiante=estudiante
        self.window=cargar_ui("UI/new_student.ui")
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
                           carrera=self.window.carrera_input.currentText(),
                           semestre=int(self.window.semestre_input.value()),
                           direccion=self.window.direccion_input.toPlainText())
        session.add(estudiante)
        session.commit()
        QMessageBox.information(self.window,"Usuario creado",
                                    "Se a registrado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    
    def actualizar(self):
        self.estudiante.primer_hombre=self.window.primernombre_input.text()
        self.estudiante.segundo_nombre=self.window.segundonombre_input.text()
        self.estudiante.primer_apellido=self.window.primerapellido_input.text()
        self.estudiante.segundo_apellido=self.window.segundoapellido_input.text()
        self.estudiante.cedula=int(self.window.cedula_input.text())
        self.estudiante.telefono=int(self.window.telefono_input.text())
        self.estudiante.email=self.window.email_input.text()
        self.estudiante.carrera=self.window.carrera_input.currentText()
        self.estudiante.semestre=int(self.window.semestre_input.value())
        self.estudiante.direccion=self.window.direccion_input.toPlainText()
        session.commit()
        QMessageBox.information(self.window,"Usuario Actualizado",
                                    "Se a actualizado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    

    def conectar_eventos(self):
        if not self.estudiante:
            self.window.RegistrarButton.setText("Registrar")
            self.window.RegistrarButton.clicked.connect(self.registrar)
        else:
            self.datos()
            self.window.RegistrarButton.setText("Actualizar")
            self.window.RegistrarButton.clicked.connect(self.actualizar)


    def datos(self):
        self.window.label.setText("Editar Datos de Estudiante")
        self.window.primernombre_input.setText(self.estudiante.primer_nombre)
        self.window.segundonombre_input.setText(self.estudiante.segundo_nombre)
        self.window.primerapellido_input.setText(self.estudiante.primer_apellido)
        self.window.segundoapellido_input.setText(self.estudiante.segundo_apellido)
        self.window.cedula_input.setText(str(self.estudiante.cedula))
        self.window.telefono_input.setText(str(self.estudiante.telefono))
        self.window.email_input.setText(self.estudiante.email)
        self.window.carrera_input.setCurrentText(self.estudiante.carrera)
        self.window.semestre_input.setValue(self.estudiante.semestre)
        self.window.direccion_input.setPlainText(self.estudiante.direccion)

    


    

    



        
    