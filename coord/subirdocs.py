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
from modelos.modulo import Pasantia,DocumentoAdjunto,session
# from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from herramientas.conversiones import jsonFormatos

from dotenv import load_dotenv


class NewDoc:
    
    def __init__(self,pasante:Pasantia):
        self.pasante=pasante

        self.window=cargar_ui("UI/subirdoc.ui")
        self.conectar_eventos()
    
    def exec(self):
        self.window.exec()
    
    def close(self):
        self.window.close()   
    
    def listas(self):
        formatos=jsonFormatos()
        self.window.input_tipo.addItem("Foto de Carnet",None)
        self.window.input_tipo.addItem("Copia de Cedula",None)
        for text,data in formatos.items():
            self.window.input_tipo.addItem(text,data)

    def conectar_eventos(self):
        self.listas()
        self.window.btnAsignar.setText("Subir")
        self.window.btnAsignar.clicked.connect(self.subir)
        
    def subir(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self.window, "Seleccionar Archivo", "", "Archivos (*.pdf *.doc *.docx)"
        )
        
        if self.file_path:
            # 2. Crear carpeta de destino si no existe
            destino_dir = f"resources/documentos/{self.pasante.carrera}/{self.pasante.student.cedula}"
            if not os.path.exists(destino_dir):
                os.makedirs(destino_dir)
            
            # 3. Generar un nombre único para evitar duplicados
            extension = os.path.splitext(self.file_path)[1]
            nombre_archivo = f"{self.window.input_tipo.currentText()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
            self.ruta_final = os.path.join(destino_dir, nombre_archivo).replace("\\","/")
        else:
            QMessageBox.critical(self.window, "Error", f"Seleccione el Archivo")
            return
        
        documento=DocumentoAdjunto(tipo_de_documento=self.window.input_tipo.currentText(),
                                   ruta=self.ruta_final
                                   )
        
        self.pasante.documentos.append(documento)
        session.commit()
        
        try:
            shutil.copy(self.file_path, self.ruta_final)
             # Guardamos la ruta en una variable
                
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"No se pudo copiar el archivo: {e}")  
        
        QMessageBox.information(self.window, "Éxito", "Archivo Guardado correctamente.")
       
        self.close()
               

        
        #_______________________________________________________________
        #self.window.semestre_input.
        #self.window.direccion_input.
        #self.window.genero_input.
    


    

    



        
    