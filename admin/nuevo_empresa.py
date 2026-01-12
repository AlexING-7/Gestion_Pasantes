import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
import shutil
from datetime import datetime
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox,QMainWindow, QFileDialog
from PySide6.QtGui import QRegularExpressionValidator, QValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QFile, Qt
# from PySide6.QtUiTools import QUiLoader
from modelos.modulo import Enterprise,session
# from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui

from dotenv import load_dotenv


class NewEnterprise:
    
    def __init__(self,empresa=None):
        load_dotenv()
        self.empresa=empresa
        self.window=cargar_ui("UI/new_empresa.ui")
        self.conectar_eventos()
    
    def exec(self):
        self.window.exec()
    
    def close(self):
        self.window.close()   
    
    def registrar(self):
        empresa=Enterprise(
                           rif=int(self.window.rif_input.text()),
                           razon_social=self.window.razon_input.text(),
                           telefono=self.window.telefono_input.text(),
                           email=self.window.email_input.text(),
                           direccion=self.window.direccion_input.toPlainText(),
                           rubro=self.window.rubro_input.text(),
                        )
        session.add(empresa)
        session.commit()
        QMessageBox.information(self.window,"Empresa Registrada",
                                    "Se a registrado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    
    def actualizar(self):
        self.empresa.razon_social=self.window.razon_input.text()
        self.empresa.rif=int(self.window.rif_input.text())
        self.empresa.telefono=self.window.telefono_input.text()
        self.empresa.rubro=self.window.rubro_input.text()
        self.empresa.email=self.window.email_input.text()
        self.empresa.direccion=self.window.direccion_input.toPlainText()

        session.commit()
        QMessageBox.information(self.window,"Usuario Actualizado",
                                    "Se a actualizado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    

    def conectar_eventos(self):
        if not self.empresa:
            self.window.RegistrarButton.setText("Registrar")
            self.window.RegistrarButton.clicked.connect(self.registrar)
        else:
            self.datos()
            self.window.RegistrarButton.setText("Actualizar")
            self.window.RegistrarButton.clicked.connect(self.actualizar)
        self.validaciones()


    def datos(self):
        self.window.label.setText("Editar Datos de Empresa")
        self.window.razon_input.setText(self.empresa.razon_social)
        self.window.rif_input.setText(str(self.empresa.rif))
        self.window.telefono_input.setText(str(self.empresa.telefono))
        self.window.email_input.setText(self.empresa.email)
        self.window.direccion_input.setPlainText(self.empresa.direccion)
        self.window.rubro_input.setText(self.empresa.rubro)
                   
    def validaciones(self):
        rx_nombre = QRegularExpression(r"^[a-zA-ZÁÉÍÓÚÑáéíóúñ\s']+$")
        validator_nombre = QRegularExpressionValidator(rx_nombre)
        
        self.window.razon_input.setValidator(validator_nombre)
        self.window.rubro_input.setValidator(validator_nombre)

        #_______________________________________________________________
        rx = QRegularExpression(r"^\d{5,9}$")
        val = QRegularExpressionValidator(rx)
        
        self.window.rif_input.setValidator(val)
        
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
    


    

    



        
    