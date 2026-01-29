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
from modelos.modulo import Student,session,Pasantia,User
# from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from herramientas.logs import registrar_log

from dotenv import load_dotenv


class NewStudent:
    
    def __init__(self,user:User,estudiante=None):
        load_dotenv()
        self.user=user
        self.estudiante=estudiante
        self.window=cargar_ui("UI/new_student.ui")
        self.conectar_eventos()
    
    def exec(self):
        self.window.exec()
    
    def close(self):
        self.window.close()   
    
    def registrar(self):
        self.guardar_foto()
        estudiante=Student(primer_nombre=self.window.primernombre_input.text(),
                           segundo_nombre=self.window.segundonombre_input.text(),
                           primer_apellido=self.window.primerapellido_input.text(),
                           segundo_apellido=self.window.segundoapellido_input.text(),
                           cedula=int(self.window.cedula_input.text()),
                           telefono=self.window.telefono_input.text(),
                           email=self.window.email_input.text(),
                           direccion=self.window.direccion_input.toPlainText(),
                           fecha_de_nacimiento=self.window.dateFecha.date().toString(Qt.ISODate),
                           foto=self.ruta_foto_guardada,
                           sexo=self.window.genero_input.currentText())
        if self.window.checkBox.isChecked():
            pasantia=Pasantia(carrera=self.window.carrera_input.currentText(),
                              semestre=int(self.window.semestre_input.value()),
                              lapso_academico=self.window.lapso_input.text())
            estudiante.pasantias.append(pasantia)
        session.add(estudiante)
        session.commit()
        QMessageBox.information(self.window,"Usuario creado",
                                    "Se a registrado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        registrar_log(session=session,
                      usuario=self.user.username,
                      tabla_afectada="Students",
                      id_registro_afectado=estudiante.id,
                      accion="INSERT",
                      mensaje=f"Registro al estudiante con CIV {estudiante.cedula}",
                              )
        self.close()
    
    def actualizar(self):
        # Capturar valores anteriores para el log
        prev = {
            "primer_nombre": self.estudiante.primer_nombre,
            "segundo_nombre": self.estudiante.segundo_nombre,
            "primer_apellido": self.estudiante.primer_apellido,
            "segundo_apellido": self.estudiante.segundo_apellido,
            "cedula": self.estudiante.cedula,
            "telefono": self.estudiante.telefono,
            "email": self.estudiante.email,
            "direccion": self.estudiante.direccion,
            "fecha_de_nacimiento": self.estudiante.fecha_de_nacimiento,
            "sexo": self.estudiante.sexo,
            "foto": getattr(self.estudiante, "foto", None),
        }

        # Intentar guardar nueva foto (si el usuario seleccionó una)
        try:
            self.guardar_foto()
        except Exception:
            # Si falla la copia, no sobreescribimos la foto
            pass

        # Aplicar cambios desde la UI
        self.estudiante.primer_nombre = self.window.primernombre_input.text()
        self.estudiante.segundo_nombre = self.window.segundonombre_input.text()
        self.estudiante.primer_apellido = self.window.primerapellido_input.text()
        self.estudiante.segundo_apellido = self.window.segundoapellido_input.text()
        try:
            self.estudiante.cedula = int(self.window.cedula_input.text())
        except Exception:
            # mantener el valor anterior si la conversión falla
            pass
        self.estudiante.telefono = self.window.telefono_input.text()
        self.estudiante.email = self.window.email_input.text()
        self.estudiante.direccion = self.window.direccion_input.toPlainText()
        self.estudiante.fecha_de_nacimiento = self.window.dateFecha.date().toString(Qt.ISODate)
        self.estudiante.sexo = self.window.genero_input.currentText()

        # Solo actualizar la ruta de la foto si existe
        if hasattr(self, "ruta_foto_guardada") and self.ruta_foto_guardada:
            self.estudiante.foto = self.ruta_foto_guardada

        session.commit()

        QMessageBox.information(
            self.window,
            "Usuario Actualizado",
            "Se ha actualizado satisfactoriamente",
            QMessageBox.StandardButton.Ok,
        )

        # Valores nuevos para el log
        nuevos = {
            "primer_nombre": self.estudiante.primer_nombre,
            "segundo_nombre": self.estudiante.segundo_nombre,
            "primer_apellido": self.estudiante.primer_apellido,
            "segundo_apellido": self.estudiante.segundo_apellido,
            "cedula": self.estudiante.cedula,
            "telefono": self.estudiante.telefono,
            "email": self.estudiante.email,
            "direccion": self.estudiante.direccion,
            "fecha_de_nacimiento": self.estudiante.fecha_de_nacimiento,
            "sexo": self.estudiante.sexo,
            "foto": getattr(self.estudiante, "foto", None),
        }

        registrar_log(
            session=session,
            usuario=self.user.username,
            tabla_afectada="Students",
            id_registro_afectado=self.estudiante.id,
            accion="UPDATE",
            valores_anteriores=prev,
            valores_nuevos=nuevos,
            mensaje=f"Actualizó al estudiante con CIV {self.estudiante.cedula}",
        )

        self.close()
    

    def conectar_eventos(self):
        if not self.estudiante:
            self.window.RegistrarButton.setText("Registrar")
            self.window.RegistrarButton.clicked.connect(self.registrar)
            self.window.subirfotoButton.clicked.connect(self.subir_foto)
            self.window.checkBox.toggled.connect(self.show_pasantias)
        else:
            self.datos()
            self.window.RegistrarButton.setText("Actualizar")
            self.window.RegistrarButton.clicked.connect(self.actualizar)
            self.window.subirfotoButton.clicked.connect(self.subir_foto)
            self.window.checkBox.setHidden(True)
            self.window.frame_pasantia.setHidden(True)
        self.validaciones()

    def show_pasantias(self,x):
        if x:
            self.window.frame_pasantia.setHidden(False)
        else:
            self.window.frame_pasantia.setHidden(True)


    def datos(self):
        self.window.label.setText("Editar Datos de Estudiante")
        self.window.primernombre_input.setText(self.estudiante.primer_nombre)
        self.window.segundonombre_input.setText(self.estudiante.segundo_nombre)
        self.window.primerapellido_input.setText(self.estudiante.primer_apellido)
        self.window.segundoapellido_input.setText(self.estudiante.segundo_apellido)
        self.window.cedula_input.setText(str(self.estudiante.cedula))
        self.window.telefono_input.setText(str(self.estudiante.telefono))
        self.window.email_input.setText(self.estudiante.email)
        #falta fecha
        self.window.direccion_input.setPlainText(self.estudiante.direccion)
        self.window.genero_input.setCurrentText(self.estudiante.sexo)
        self.ruta_foto_guardada=self.estudiante.foto
        
    def subir_foto(self):
        # 1. Abrir explorador de archivos
        self.file_path, _ = QFileDialog.getOpenFileName(
            self.window, "Seleccionar Foto", "", "Imágenes (*.png *.jpg *.jpeg)"
        )
        
        if self.file_path:
            # 2. Crear carpeta de destino si no existe
            destino_dir = "resources/fotos_estudiantes"
            if not os.path.exists(destino_dir):
                os.makedirs(destino_dir)
            
            # 3. Generar un nombre único para evitar duplicados
            extension = os.path.splitext(self.file_path)[1]
            nombre_archivo = f"estudiante_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
            self.ruta_final = os.path.join(destino_dir, nombre_archivo)
            
            # 4. Copiar el archivo físicamente
            QMessageBox.information(self.window, "Éxito", "Foto cargada correctamente.")
            self.window.subirfotoButton.setText("Listo")
            
                
    def guardar_foto(self):
        try:#aquiiiiiiii self file da error
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
    


    

    



        
    