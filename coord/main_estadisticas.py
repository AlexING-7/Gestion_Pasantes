import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QListWidgetItem

from modelos.modulo import session,Student,Pasantia
from sqlalchemy import select
from sqlalchemy import or_,and_, cast, String
from getmac import get_mac_address as gma
from herramientas.widgets_personalizados import MiWidgetClickeable
from herramientas.plantilla_ui import cargar_ui
from herramientas.conversiones import null_string,calcular_edad,calcular_duracion_meses,convertir_pil_a_pixmap,formato_miles,guion_telefono
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent,QSize

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class StackEstadistica():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.current_pasante = None
         
        self.conectar_eventos()
        self.window.stackedWidget.setCurrentIndex(6)

    def conectar_eventos(self):
        pass

    