import os
import sys
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader

def cargar_ui(UI):
    try:
        ui_file_path = os.path.join(".", UI)
        
        if not os.path.exists(ui_file_path):
            raise FileNotFoundError(f"No se encontró el archivo: {ui_file_path}")
        
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise Exception(f"No se pudo abrir el archivo: {ui_file.errorString()}")
        
        window = loader.load(ui_file)
        ui_file.close()
        
        if not window:
            raise Exception(loader.errorString())
 
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error al cargar la interfaz:\n{str(e)}")
        sys.exit(1)
    return window