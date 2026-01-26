import os
import sys
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
try:
    from .widgets_personalizados import *
except Exception:
    try:
        from herramientas.widgets_personalizados import *
    except Exception:
        pass


class CustomUiLoader(QUiLoader):
    def createWidget(self, className, parent=None, name=''):
        cls = globals().get(className)
        if cls is not None:
            try:
                widget = cls(parent)
                widget.setObjectName(name)
                return widget
            except Exception:
                # Fall back to default creation on any error
                pass
        return super().createWidget(className, parent, name)

def cargar_ui(UI,widget=None):
    try:
        ui_file_path = os.path.join(".", UI).replace("\\","/")
        
        if not os.path.exists(ui_file_path):
            raise FileNotFoundError(f"No se encontró el archivo: {ui_file_path}")
        
        ui_file = QFile(ui_file_path)
        
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise Exception(f"No se pudo abrir el archivo: {ui_file.errorString()}")
        
        loader = CustomUiLoader()
        load = loader.load(ui_file, parentWidget=widget)
        ui_file.close() 

    except Exception as e:
        print(e)
        QMessageBox.critical(None, "Error", f"Error al cargar la interfaz:\n{str(e)}")
        sys.exit(1)
    return load
    