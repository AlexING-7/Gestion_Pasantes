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
from modelos.modulo import Tutor_Academico,session
# from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui

from dotenv import load_dotenv


class NewTutorA:
    
    def __init__(self,tutor=None):
        load_dotenv()
        self.tutor=tutor
        self.window=cargar_ui("UI/new_tutor_academico.ui")
        self.conectar_eventos()
    
    def exec(self):
        self.window.exec()
    
    def close(self):
        self.window.close()   
    
    def registrar(self):
        self.guardar_foto()
        tutor=Tutor_Academico(primer_nombre=self.window.primernombre_input.text(),
                           segundo_nombre=self.window.segundonombre_input.text(),
                           primer_apellido=self.window.primerapellido_input.text(),
                           segundo_apellido=self.window.segundoapellido_input.text(),
                           cedula=int(self.window.cedula_input.text()),
                           telefono=self.window.telefono_input.text(),
                           email=self.window.email_input.text(),
                           fecha_de_nacimiento=self.window.dateFecha.date().toString(Qt.ISODate),
                           foto=self.ruta_foto_guardada,
                           sexo=self.window.genero_input.currentText(),
                           especialidad=self.window.especialidad_input.text())
        session.add(tutor)
        session.commit()
        QMessageBox.information(self.window,"Tutor Academico registrado",
                                    "Se a registrado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    
    def actualizar(self):
        self.guardar_foto()
        self.tutor.primer_hombre=self.window.primernombre_input.text()
        self.tutor.segundo_nombre=self.window.segundonombre_input.text()
        self.tutor.primer_apellido=self.window.primerapellido_input.text()
        self.tutor.segundo_apellido=self.window.segundoapellido_input.text()
        self.tutor.cedula=int(self.window.cedula_input.text())
        self.tutor.telefono=self.window.telefono_input.text()
        self.tutor.email=self.window.email_input.text()
        self.tutor.fecha_de_nacimiento=self.window.dateFecha.date().toString(Qt.ISODate)
        self.tutor.sexo=self.window.genero_input.currentText()
        self.tutor.foto=self.ruta_foto_guardada
        self.tutor.especialidad=self.window.especialidad_input.text()
        session.commit()
        QMessageBox.information(self.window,"Usuario Actualizado",
                                    "Se a actualizado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    

    def conectar_eventos(self):
        if not self.tutor:
            self.window.RegistrarButton.setText("Registrar")
            self.window.RegistrarButton.clicked.connect(self.registrar)
            self.window.subirfotoButton.clicked.connect(self.subir_foto)
        else:
            self.datos()
            self.window.RegistrarButton.setText("Actualizar")
            self.window.RegistrarButton.clicked.connect(self.actualizar)
            self.window.subirfotoButton.clicked.connect(self.subir_foto)
        self.validaciones()


    def datos(self):
        self.window.label.setText("Editar Datos de Tutor Academico")
        self.window.primernombre_input.setText(self.tutor.primer_nombre)
        self.window.segundonombre_input.setText(self.tutor.segundo_nombre)
        self.window.primerapellido_input.setText(self.tutor.primer_apellido)
        self.window.segundoapellido_input.setText(self.tutor.segundo_apellido)
        self.window.cedula_input.setText(str(self.tutor.cedula))
        self.window.telefono_input.setText(str(self.tutor.telefono))
        self.window.email_input.setText(self.tutor.email)
        self.window.genero_input.setCurrentText(self.tutor.sexo)
        self.window.especialidad_input.setText(self.tutor.especialidad)
        self.ruta_foto_guardada=self.tutor.foto
        
    def subir_foto(self):
        # 1. Abrir explorador de archivos
        self.file_path, _ = QFileDialog.getOpenFileName(
            self.window, "Seleccionar Foto", "", "Imágenes (*.png *.jpg *.jpeg)"
        )
        
        if self.file_path:
            # 2. Crear carpeta de destino si no existe
            destino_dir = "resources/fotos_TutoresAcedemicos"
            if not os.path.exists(destino_dir):
                os.makedirs(destino_dir)
            
            # 3. Generar un nombre único para evitar duplicados
            extension = os.path.splitext(self.file_path)[1]
            nombre_archivo = f"tutor_academico_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
            self.ruta_final = os.path.join(destino_dir, nombre_archivo)
            
            # 4. Copiar el archivo físicamente
            QMessageBox.information(self.window, "Éxito", "Foto cargada correctamente.")
            self.window.subirfotoButton.setText("Listo")
            
                
    def guardar_foto(self):
        try:
            shutil.copy(self.file_path, self.ruta_final)
            self.ruta_foto_guardada = self.ruta_final  # Guardamos la ruta en una variable
                
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"No se pudo copiar el archivo: {e}")
            
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
    


    

    



        
    