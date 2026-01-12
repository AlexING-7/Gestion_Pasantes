import os
from datetime import datetime
from pathlib import Path
from PySide6.QtGui import  QIcon
from modelos.modulo import Pasantia
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QHBoxLayout,QStyle,QLineEdit,QAbstractScrollArea
import shutil
from modelos.modulo import DocumentoAdjunto,session

class show_documentos():
    
    def __init__(self,window,pasante:Pasantia) -> None:
        self.pasante=pasante
        print(self.pasante.student.cedula)
        self.window=window
        self.comboDoc=window.comboDoc
        self.comboDoc.setCurrentIndex(-1)
        self.lineRuta=window.lineRuta
        self.lineRuta.clear()
        self.btnSubirDoc=window.btnSubirDoc
        self.tabla_documentos=window.tabla_documentos
        self.regresarButtonP_2=self.window.regresarButtonP_2
        self.window.StackedPsa.setCurrentIndex(2)
        self.conectar_eventos()
        self.file_path=None
        
    def conectar_eventos(self):
        self.regresarButtonP_2.clicked.connect(lambda: self.window.StackedPsa.setCurrentIndex(1))
        if not self.lineRuta.actions(): 
            icon_path = Path(__file__).resolve().parent.parent / "resources" / "images" / "upload.svg"
            
            if icon_path.exists():
                icon = QIcon(str(icon_path))
            else:
                # Fallback al icono estándar si no encuentra el archivo
                sicon = self.lineRuta.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
            
            # Solo agregamos la acción si no existía ninguna
            self.icon = self.lineRuta.addAction(icon, QLineEdit.ActionPosition.LeadingPosition)
            self.icon.triggered.connect(self.path_file)
        try:
            self.window.btnSubirDoc.clicked.disconnect()
        except Exception:
            pass
        self.btnSubirDoc.clicked.connect(self.subir_documento)
    
    def path_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self.window, "Seleccionar Archivo", "", "Archivos (*.pdf *.doc *.docx)"
        )
        self.lineRuta.setText(self.file_path)
    
    def subir_documento(self):
        print(self.pasante.student.cedula)
        if self.file_path:
            # 2. Crear carpeta de destino si no existe
            destino_dir = f"resources/documentos/{self.pasante.carrera}/{self.pasante.student.cedula}"
            if not os.path.exists(destino_dir):
                os.makedirs(destino_dir)
            
            # 3. Generar un nombre único para evitar duplicados
            extension = os.path.splitext(self.file_path)[1]
            nombre_archivo = f"{self.comboDoc.currentText()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
            self.ruta_final = os.path.join(destino_dir, nombre_archivo).replace("\\","/")
        documento=DocumentoAdjunto(tipo_de_documento=self.comboDoc.currentText(),
                                   ruta=self.ruta_final
                                   )
        
        self.pasante.documentos.append(documento)
        session.commit()
        self.guardar_archivo()
        QMessageBox.information(self.window, "Éxito", "Archivo Guardado correctamente.")
        
            
    def guardar_archivo(self):
        try:
            shutil.copy(self.file_path, self.ruta_final)
             # Guardamos la ruta en una variable
                
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"No se pudo copiar el archivo: {e}")         
    
    def ver_documento(self):
        pass
    
    def eliminar_documento(self):
        pass
    
    def header(self):
        pass
    
    def pag_tabla_documentos(self):
        pass
    
    def generar_doc(self):
        pass