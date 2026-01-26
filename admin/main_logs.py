
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from modelos.modulo import User,TSession,session,SistemaLog
from PySide6.QtWidgets import QTableWidgetItem

from dotenv import load_dotenv
from sqlalchemy import select

from PySide6.QtWidgets import QHeaderView
from herramientas.logs import registrar_log
from herramientas.conversiones import *

class StackLogs():
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.stackedWidget.setCurrentIndex(0)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.window.tablaLogs.installEventFilter(main)
        self.tablaLogs=self.window.tablaLogs
        self.conectar_eventos()
        
    def conectar_eventos(self):
        self.pag_logs()
    
    def header(self):
        header=self.tablaLogs.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        
        
    def pag_logs(self):
        self.header()
        logs=self.get_data()
        self.tablaLogs.setRowCount(0)
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
    
    
    def get_data(self):
        stmt=select(SistemaLog)
        return session.scalars(stmt).all()