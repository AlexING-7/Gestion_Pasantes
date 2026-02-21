
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from modelos.modulo import User,TSession,session,SistemaLog,Pasantia,Tutor_Academico,Enterprise
from PySide6.QtWidgets import QTableWidgetItem,QMessageBox,QFileDialog,QAbstractScrollArea

from dotenv import load_dotenv
from sqlalchemy import select

from PySide6.QtWidgets import QHeaderView
from herramientas.logs import registrar_log
from herramientas.conversiones import *
from PySide6.QtCore import QEvent,QSize,Qt
from herramientas.exports import exportar_modelo_a_excel

class StackLogs():
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.stackedWidget.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.window.tablaLogs.installEventFilter(main)
        self.tablaLogs=self.window.tablaLogs
        self.comboAcciones=self.window.comboAcciones
        self.comboTablas=self.window.comboTablas
        self.comboUsuarios=self.window.comboUsuarios
        self.contadores()
        
        self.conectar_eventos()
    
    def contadores(self):
        stmt=select(Pasantia.id).where(Pasantia.lapso_academico=="2025-2")
        pasantes=len(session.scalars(stmt).all())
        self.window.contarPasantes.setText(f"{pasantes}")
        
        stmt=select(Tutor_Academico.id).join(Tutor_Academico.pasantias).where(Pasantia.lapso_academico=="2025-2").distinct()
        tutores=len(session.scalars(stmt).all())
        self.window.contarTutores.setText(f"{tutores}")
        
        stmt=select(Enterprise.id).join(Enterprise.pasantias).where(Pasantia.lapso_academico=="2025-2").distinct()
        empresas=len(session.scalars(stmt).all())
        self.window.contarEmpresas.setText(f"{empresas}")
    
    def offset_count(self):
        return (self.numero_pagina - 1) * self.tamano_pagina 
    
    def eventFilter(self,source,event):       
        if source == self.tablaLogs and event.type() == QEvent.Type.Resize:

            height=self.tablaLogs.height()
            self.tamano_pagina=int(height/25.4)
            self.pag_logs()
            print("Ejecutando Logs") 
    
    def listas(self):
        users=session.scalars(select(User.username)).all()
        self.comboAcciones.addItem('Todas las Acciones',None)
        for i in ['UPDATE','INSERT','DELETE','LOGIN','LOGOUT','IMPORT','EXPORT','REPORT','ERROR']:
            self.comboAcciones.addItem(i,i)
        for i in ['users', 'students', 'pasantias', 'documentos_adjuntos', 'configuraciones']:
            self.comboTablas.addItem(i,i)
        for i in users:
            self.comboUsuarios.addItem(i,i)
    
    def conectar_eventos(self):
        self.listas()
        self.window.btnExportarLogs.clicked.connect(self.exportar)
        self.comboAcciones.activated.connect(lambda: self.cambio_programa())
        self.comboUsuarios.activated.connect(lambda: self.cambio_programa())
        self.comboTablas.activated.connect(lambda: self.cambio_programa())
        self.window.btnAntLogs.clicked.connect(lambda :self.change_table("Anterior"))
        self.window.btnSigLogs.clicked.connect(lambda :self.change_table("Siguiente"))
    
    def change_table(self,buttom):
        if buttom.lower()=="anterior":
            self.numero_pagina=self.numero_pagina-1 if self.numero_pagina>1 else 1
        elif buttom.lower()=="siguiente":
            self.numero_pagina+=1
        self.pag_logs()
    
    def header(self):
        header=self.tablaLogs.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        self.window.tablaLogs.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.window.tablaLogs.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        
        
    def pag_logs(self):
        self.tablaLogs.setRowCount(0)
        self.header()
        logs=self.get_data()

        if (self.all_data-self.offset_count())<=self.tamano_pagina:
           self.window.btnSigLogs.setEnabled(False)
        else:
            self.window.btnSigLogs.setEnabled(True)
        self.indice()     
        for fila,log in enumerate(logs):
            log:SistemaLog
            self.tablaLogs.insertRow(fila)
            
            self.tablaLogs.setItem(fila,0,QTableWidgetItem(str(log.fecha_hora)))
            self.tablaLogs.setItem(fila,1,QTableWidgetItem(str(log.usuario)))
            self.tablaLogs.setItem(fila,2,QTableWidgetItem(str(log.accion)))
            self.tablaLogs.setItem(fila,3,QTableWidgetItem(null_string(log.tabla_afectada)))
            self.tablaLogs.setItem(fila,4,QTableWidgetItem(null_string(log.id_registro_afectado)))
            self.tablaLogs.setItem(fila,5,QTableWidgetItem(str(log.mensaje)))
            self.tablaLogs.setItem(fila,6,QTableWidgetItem(str(log.ip_maquina)))
    
    def indice(self):
        ind1=1+self.offset_count()
        ind2=self.numero_pagina*self.tamano_pagina
        self.window.btnIndLogs.setText(f"{ind1}-{ind2 if ind2<self.all_data else self.all_data} de {self.all_data}")
    
    def cambio_programa(self):
        self.numero_pagina=1
        if not self.get_data():
            QMessageBox.warning(self.window, "Aviso", "Busqueda no encontrada")
            return
        self.pag_logs()
    
    def get_data(self):
        self.all_data=len(self.get_data_all())
        stmt=select(SistemaLog)
        condiciones=[]
        if self.comboAcciones.currentData():
            condiciones.append(SistemaLog.accion==self.comboAcciones.currentText())
        if self.comboTablas.currentData():
            condiciones.append(SistemaLog.tabla_afectada==self.comboTablas.currentData())
        if self.comboUsuarios.currentData():
            condiciones.append(SistemaLog.usuario==self.comboUsuarios.currentData())

        if condiciones:
            stmt=stmt.where(*condiciones)
        
        return session.scalars(stmt.limit(self.tamano_pagina).offset(self.offset_count())).all()
    
    def get_data_all(self):
        stmt=select(SistemaLog)
        condiciones=[]
        if self.comboAcciones.currentData():
            condiciones.append(SistemaLog.accion==self.comboAcciones.currentText())
        if self.comboTablas.currentData():
            condiciones.append(SistemaLog.tabla_afectada==self.comboTablas.currentData())
        if self.comboUsuarios.currentData():
            condiciones.append(SistemaLog.usuario==self.comboUsuarios.currentData())

        if condiciones:
            print(condiciones)
            stmt=stmt.where(*condiciones)
        
        return session.scalars(stmt).all()
    def exportar(self):
         # Abrir diálogo para guardar archivo
        archivo, _ = QFileDialog.getSaveFileName(
            self.main, 
            "Guardar Reporte", 
            "", 
            "Archivos de Excel (*.xlsx)"
        )
        
        if archivo:
            if not archivo.endswith('.xlsx'):
                archivo += '.xlsx'
                
            try:
                
                # Llamas a tu función de exportación aquí (Estrategia A o B)
                exportar_modelo_a_excel(self.get_data_all(),archivo,SistemaLog)
                
                QMessageBox.information(self.main, "Éxito", "La base de datos se exportó correctamente.")
            except Exception as e:
                QMessageBox.critical(self.main, "Error", f"No se pudo exportar: {str(e)}")