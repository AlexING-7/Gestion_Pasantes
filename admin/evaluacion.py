
from modelos.modulo import Pasantia
import shutil
from PySide6.QtWidgets import QMessageBox
from herramientas.plantilla_ui import cargar_ui
from modelos.modulo import Evaluacion,session


class show_evaluar():
    
    def __init__(self,pasante:Pasantia,editar=False) -> None:
        self.editar=editar
        self.pasante=pasante
        self.window=cargar_ui("UI/evaluar.ui")
        self.spinTutorA=self.window.spinTutorA
        self.spinTutorE=self.window.spinTutorE
        self.spinExpo=self.window.spinExpo
        self.spinTaller=self.window.spinTaller
        self.btnCalcular=self.window.btnCalcular
        self.conectar_eventos()
        
    def exec(self):
        self.window.exec()
        
    def close(self):
        self.window.close()
        
    def conectar_eventos(self):
        self.btnCalcular.clicked.connect(self.calcular)
        self.datos()
        
    
    def edit(self):
        pass
    
    def datos(self):
        if not self.editar:
            return
        self.spinTutorA.setValue(self.pasante.evaluacion.nota_tutor_aca)
        self.spinTutorE.setValue(self.pasante.evaluacion.nota_tutor_emp)
        self.spinExpo.setValue(self.pasante.evaluacion.exposicion)
        self.spinTaller.setValue(self.pasante.evaluacion.taller_induccion)

    def calcular(self):
        try:
            a = float(self.spinTutorA.value())
            e = float(self.spinTutorE.value())
            expo = float(self.spinExpo.value())
            taller = float(self.spinTaller.value())
        except Exception:
            # Valores inválidos: asegurar al menos 1
            a = e = expo = taller = 1.0
        w_a = 0.40
        w_e = 0.40
        w_expo = 0.15
        w_taller = 0.05
        total = a * w_a + e * w_e + expo * w_expo + taller * w_taller
        total = max(1.0, min(20.0, total))
        self.total = round(total, 2)     
        if self.editar and getattr(self.pasante, "evaluacion", None):
            evalu = self.pasante.evaluacion
            evalu.nota_tutor_aca = a
            evalu.nota_tutor_emp = e
            evalu.exposicion = expo
            evalu.taller_induccion = taller
            evalu.total = self.total
        else:
            evalu = Evaluacion(nota_tutor_aca=a,
                               nota_tutor_emp=e,
                               exposicion=expo,
                               taller_induccion=taller,
                               total=self.total)
            self.pasante.evaluacion = evalu
        session.add(evalu)
        session.commit()
        QMessageBox.information(self.window, "Pasante Evaluado",
                                "Nota se ha registrado satisfactoriamente",
                                QMessageBox.StandardButton.Ok)
    