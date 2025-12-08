import os
import sys
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader

def cargar_ui(UI,widget=None):
    try:
        ui_file_path = os.path.join(".", UI)
        
        if not os.path.exists(ui_file_path):
            raise FileNotFoundError(f"No se encontró el archivo: {ui_file_path}")
        
        ui_file = QFile(ui_file_path)
        
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise Exception(f"No se pudo abrir el archivo: {ui_file.errorString()}")
        
        load=QUiLoader().load(ui_file,parentWidget=widget)
        ui_file.close() 

    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error al cargar la interfaz:\n{str(e)}")
        sys.exit(1)
    return load
    