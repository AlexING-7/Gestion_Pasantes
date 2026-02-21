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
from modelos.modulo import Pasantia,Tutor_Academico,Student,Enterprise,Configuracion,session
# from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from herramientas.conversiones import convertir_a_json
from sqlalchemy import select

from dotenv import load_dotenv


class NewPasante:
    
    def __init__(self,pasante=None):
        load_dotenv()
        self.pasante=pasante
        self.empresas=session.query(Enterprise).all()

        self.tutorA=session.query(Tutor_Academico).all()
        self.window=cargar_ui("UI/new_pasanteCoord.ui")
        self.window.stackedWidget.setCurrentIndex(0)
        self.conectar_eventos()
    
    def exec(self):
        self.window.exec()
    
    def close(self):
        self.window.close()   
    
    def listas(self):
        for empresa in self.empresas:
            self.window.empresa_input.addItem(f"{empresa.razon_social}:{empresa.rif}",empresa)
        for tutorA in self.tutorA:
            self.window.tutorA_input.addItem(f"{tutorA.primer_nombre}:{tutorA.cedula},",tutorA)
            
        self.window.carrera_input.clear()
        carreras=session.scalars(select(Configuracion.valor).where(Configuracion.clave=="carreras")).one_or_none()
        carreras_json=convertir_a_json(carreras)
        for i in carreras_json["carreras"]:
            self.window.carrera_input.addItem(i,i) 
    
    def lista_tutoresE(self):
        
        empresa=self.window.empresa_input.currentData()
        print(empresa)
        for tutor in empresa.tutores:
            self.window.tutorE_input.addItem(f"{tutor.primer_nombre}:{tutor.cedula},",tutor)
            
    def show_sucursal(self,x):
        if x:
            self.window.frame.setHidden(True)
        else:
            self.window.frame.setHidden(False)        
            
    def registrar(self):
        pasante=Pasantia()
        self.datos_pasante(pasante)
        estudiante=Student()
        estudiante.primer_nombre = self.window.primernombre_input.text()
        estudiante.segundo_nombre = self.window.segundonombre_input.text()
        estudiante.primer_apellido = self.window.primerapellido_input.text()
        estudiante.segundo_apellido = self.window.segundoapellido_input.text()
        estudiante.cedula = int(self.window.cedula_input.text())
        estudiante.telefono = self.window.telefono_input.text()
        estudiante.email = self.window.email_input.text()
        estudiante.direccion = self.window.direccion_estudiante.toPlainText()
        estudiante.fecha_de_nacimiento = self.window.dateFecha.date().toString(Qt.ISODate)
        estudiante.sexo = self.window.genero_input.currentText() 
        estudiante.foto = self.ruta_foto_guardada 
        
        estudiante.pasantias.append(pasante)
        
        empresa=self.window.empresa_input.currentData()
        if empresa:
            empresa.pasantias.append(pasante)
            
        tutorA=self.window.tutorA_input.currentData()
        if tutorA:
            tutorA.pasantias.append(pasante)
        
        tutorE=self.window.tutorE_input.currentData()
        if tutorE:
            tutorE.pasantias.append(pasante)
        
        session.commit()
        QMessageBox.information(self.window,"Pasantia registrada",
                                    "Se a registrado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    
    def actualizar(self):
        self.datos_pasante(self.pasante)
        session.commit()
        QMessageBox.information(self.window,"Pasante Actualizado",
                                    "Se a actualizado satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        self.close()
    
    def datos_pasante(self,pasantia:Pasantia):
        if pasantia.student:
            estudiante=pasantia.student
            estudiante.primer_nombre = self.window.primernombre_input.text()
            estudiante.segundo_nombre = self.window.segundonombre_input.text()
            estudiante.primer_apellido = self.window.primerapellido_input.text()
            estudiante.segundo_apellido = self.window.segundoapellido_input.text()
            estudiante.cedula = int(self.window.cedula_input.text())
            estudiante.telefono = self.window.telefono_input.text()
            estudiante.email = self.window.email_input.text()
            estudiante.direccion = self.window.direccion_estudiante.toPlainText()
            estudiante.fecha_de_nacimiento = self.window.dateFecha.date().toString(Qt.ISODate)
            estudiante.sexo = self.window.genero_input.currentText() 
            estudiante.foto = self.ruta_foto_guardada 
                               
        pasantia.lapso_academico=self.window.lapso_input.text().strip()
        pasantia.carrera=self.window.carrera_input.currentText()
        pasantia.semestre=int(self.window.semestre_input.value())
        pasantia.inicio_pasantias=self.window.inicio_input.date().toString(Qt.ISODate)
        pasantia.final_pasantias=self.window.final_input.date().toString(Qt.ISODate)
        pasantia.departamento=self.window.departamento_input.text().strip()
        pasantia.estado=self.window.estado_input.currentText()
        pasantia.trabajo_asignado=self.window.trabajo_input.toPlainText().strip()
        pasantia.titulo_de_informe=self.window.titulo_input.text().strip()
        pasantia.plan_de_trabajo=self.window.plan_input.toPlainText().strip()
        pasantia.jefe_de_carta=self.window.repr_input.text().strip()
        pasantia.cargo_jefe_de_carta=self.window.cargo_repr_input.text().strip()
        pasantia.sede=self.window.checkBox.isChecked()
        pasantia.direccion=self.window.direccion_input.toPlainText().strip()
        
        
    
    def conectar_eventos(self):
        self.listas()
        if not self.pasante:
            self.window.RegistrarButton.setText("Registrar")
            self.window.RegistrarButton.clicked.connect(self.registrar)
            self.window.checkBox.toggled.connect(self.show_sucursal)
        else:
            self.datos()
            self.window.RegistrarButton.setText("Actualizar")
            self.window.RegistrarButton.clicked.connect(self.actualizar)
            self.window.checkBox.toggled.connect(self.show_sucursal)     
        self.window.empresa_input.currentIndexChanged.connect(self.lista_tutoresE)
        self.window.subirfotoButton.clicked.connect(self.subir_foto)
        self.window.btnAtras.clicked.connect(self.ir_a_anterior)
        self.window.btnSiguiente.clicked.connect(self.ir_a_siguiente)

        # Activar validaciones de campos
        self.validaciones()
    def ir_a_siguiente(self):
        indice_actual = self.window.stackedWidget.currentIndex()
        total_paginas = self.window.stackedWidget.count()
        proximo_indice = (indice_actual + 1) % total_paginas
        self.window.stackedWidget.setCurrentIndex(proximo_indice)
        
    def ir_a_anterior(self):
        indice_actual = self.window.stackedWidget.currentIndex()
        total_paginas = self.window.stackedWidget.count()
        indice_anterior = (indice_actual - 1 + total_paginas) % total_paginas
        self.window.stackedWidget.setCurrentIndex(indice_anterior)

    def datos(self):
        self.pasante:Pasantia
        self.estudiante=self.pasante.student
        self.ruta_foto_guardada=self.pasante.student.foto
        self.window.primernombre_input.setText(self.estudiante.primer_nombre)
        self.window.segundonombre_input.setText(self.estudiante.segundo_nombre)
        self.window.primerapellido_input.setText(self.estudiante.primer_apellido)
        self.window.segundoapellido_input.setText(self.estudiante.segundo_apellido)
        self.window.cedula_input.setText(str(self.estudiante.cedula))
        self.window.telefono_input.setText(str(self.estudiante.telefono))
        self.window.email_input.setText(self.estudiante.email)
        nacimiento = getattr(self.estudiante, 'fecha_de_nacimiento', None)
        if nacimiento:
            qd0 = QDate.fromString(str(nacimiento), Qt.ISODate)
            if qd0.isValid():
                self.window.dateFecha.setDate(qd0)
        self.window.direccion_estudiante.setPlainText(self.estudiante.direccion)
        self.window.genero_input.setCurrentText(self.estudiante.sexo)

        
        
        
        index2=self.window.tutorA_input.findData(self.pasante.tutor_academico)
        self.window.tutorA_input.setCurrentIndex(index2)
        
        index3=self.window.empresa_input.findData(self.pasante.empresa)
        self.window.empresa_input.setCurrentIndex(index3)
        
        index4=self.window.tutorE_input.findData(self.pasante.tutor_empresarial)
        self.window.tutorE_input.setCurrentIndex(index4)
        
        self.window.lapso_input.setText(self.pasante.lapso_academico)
        from herramientas.conversiones import null_string
        self.window.carrera_input.setCurrentText(getattr(self.pasante, 'carrera'))
        
        if getattr(self.pasante, 'semestre', None) is not None:
            try:
                self.window.semestre_input.setValue(int(self.pasante.semestre))
            except Exception:
                pass

        # Fechas: el modelo puede contener strings ISO o objetos date
        inicio = getattr(self.pasante, 'inicio_pasantias', None)
        if inicio:
            qd = QDate.fromString(str(inicio), Qt.ISODate)
            if qd.isValid():
                self.window.inicio_input.setDate(qd)
        final = getattr(self.pasante, 'final_pasantias', None)
        if final:
            qd2 = QDate.fromString(str(final), Qt.ISODate)
            if qd2.isValid():
                self.window.final_input.setDate(qd2)

        self.window.departamento_input.setText(null_string(getattr(self.pasante, 'departamento', None)))
        self.window.estado_input.setCurrentText(null_string(getattr(self.pasante, 'estado', None)))
        self.window.trabajo_input.setPlainText(null_string(getattr(self.pasante, 'trabajo_asignado', None)))
        self.window.titulo_input.setText(null_string(getattr(self.pasante, 'titulo_de_informe', None)))
        self.window.plan_input.setPlainText(null_string(getattr(self.pasante, 'plan_de_trabajo', None)))
        self.window.repr_input.setText(null_string(getattr(self.pasante, 'jefe_de_carta', None)))
        self.window.cargo_repr_input.setText(null_string(getattr(self.pasante, 'cargo_jefe_de_carta', None)))
        self.window.checkBox.setChecked(bool(getattr(self.pasante, 'sede', False)))
        self.window.direccion_input.setPlainText(null_string(getattr(self.pasante, 'direccion', None)))
        
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
            self.guardar_foto()
            QMessageBox.information(self.window, "Éxito", "Foto cargada correctamente.")
            self.window.subirfotoButton.setText("Listo")
            
                
    def guardar_foto(self):
        if not hasattr(self,"file_path"):
            self.ruta_foto_guardada=None
            return
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
        
        # Rango de fecha de nacimiento
        min_date = QDate(1944, 1, 1)
        max_date = QDate.currentDate().addYears(-17)
        try:
            self.window.dateFecha.setDateRange(min_date, max_date)
        except Exception:
            pass

        # Patron para lapso academico (ejemplo similar al de nuevo_estudiante)
        patron = r"^19|20\d{2}-[1-2]$"
        regex = QRegularExpression(patron)
        validador = QRegularExpressionValidator(regex)
        self.window.lapso_input.setValidator(validador)

        # Conectar cambios de texto para actualizar estilos (solo QLineEdit)
        self.window.primernombre_input.textChanged.connect(lambda: self.actualizar_estilo(self.window.primernombre_input))
        self.window.segundonombre_input.textChanged.connect(lambda: self.actualizar_estilo(self.window.segundonombre_input))
        self.window.primerapellido_input.textChanged.connect(lambda: self.actualizar_estilo(self.window.primerapellido_input))
        self.window.segundoapellido_input.textChanged.connect(lambda: self.actualizar_estilo(self.window.segundoapellido_input))
        self.window.telefono_input.textChanged.connect(lambda: self.actualizar_estilo(self.window.telefono_input))
        self.window.cedula_input.textChanged.connect(lambda: self.actualizar_estilo(self.window.cedula_input))
        self.window.email_input.textChanged.connect(lambda: self.actualizar_estilo(self.window.email_input))
        self.window.lapso_input.textChanged.connect(lambda: self.actualizar_estilo(self.window.lapso_input))


    def actualizar_estilo(self,widget):
        texto = widget.text()
        if not texto:
            widget.setProperty("estado", "neutral")

        elif widget.hasAcceptableInput():

            widget.setProperty("estado", "valido")

        else:
            widget.setProperty("estado", "invalido")

        widget.style().unpolish(widget)
        widget.style().polish(widget)
        
    def is_valid(self):
        if not self.window.primernombre_input.text() or not self.window.primerapellido_input.text():
            QMessageBox.warning(self.window, "Campos Vacios", "El nombre y el apellido del Estudiante debe registrarse")
            return True
        
        if not self.window.cedula_input.text() or not self.window.cedula_input.hasAcceptableInput():
            QMessageBox.warning(self.window, "Campos Invalidos o Vacios", "La cedula del Estudiante debe cumplir con el formato")
            return True
        
        if self.window.telefono_input.text() and not self.window.telefono_input.hasAcceptableInput():
            QMessageBox.warning(self.window, "Campos Invalidos", "El Telefono del Estudiante debe cumplir con el formato")
            return True
        
        if not self.window.email_input.text() or not self.window.email_input.hasAcceptableInput():
            QMessageBox.warning(self.window, "Campos Invalidos o Vacios", "El Correo del Estudiante debe cumplir con el formato")
            return True
        
        if self.window.lapso_input.text() and not self.window.lapso_input.hasAcceptableInput():
            QMessageBox.warning(self.window, "Campos Invalidos", "El Lapso del Estudiante debe cumplir con el formato")
            return True
        
        return False
    


    

    



        
    