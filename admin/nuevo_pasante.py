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


class NewPasante:
    
    def __init__(self,pasante=None):
        load_dotenv()
        self.pasante=pasante
        self.empresas=session.query(Enterprise).all()
        self.estudiantes=session.query(Student).all()
        self.tutorA=session.query(Tutor_Academico).all()
        self.window=cargar_ui("UI/new_pasante.ui")
        self.window.stackedWidget.setCurrentIndex(0)
        self.conectar_eventos()
    
    def exec(self):
        self.window.exec()
    
    def close(self):
        self.window.close()   
    
    def listas(self):
        for empresa in self.empresas:
            self.window.empresa_input.addItem(f"{empresa.razon_social}:{empresa.rif}",empresa)
        for estudiante in self.estudiantes:
            self.window.estudiante_input.addItem(f"{estudiante.primer_nombre}:{estudiante.cedula},",estudiante)
        for tutorA in self.tutorA:
            self.window.tutorA_input.addItem(f"{tutorA.primer_nombre}:{tutorA.cedula},",tutorA)
    
    def lista_tutoresE(self):
        
        empresa=self.window.empresa_input.currentData()
        print(empresa)
        for tutor in empresa.tutores:
            self.window.tutorE_input.addItem(f"{tutor.primer_nombre}:{tutor.cedula},",tutor)
            
    def registrar(self):
        pasante=Pasantia()
        self.datos_pasante(pasante)
        estudiante=self.window.estudiante_input.currentData()
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
        else:
            self.datos()
            self.window.RegistrarButton.setText("Actualizar")
            self.window.RegistrarButton.clicked.connect(self.actualizar)     
        self.window.empresa_input.currentIndexChanged.connect(self.lista_tutoresE)
        self.window.btnAtras.clicked.connect(lambda: self.window.stackedWidget.setCurrentIndex(0))
        self.window.btnSiguiente.clicked.connect(lambda: self.window.stackedWidget.setCurrentIndex(1))

        #self.validaciones()


    def datos(self):
        index1=self.window.estudiante_input.findData(self.pasante.student)
        self.window.estudiante_input.setCurrentIndex(index1)
        
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
    


    

    



        
    