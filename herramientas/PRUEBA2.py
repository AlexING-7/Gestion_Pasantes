import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import json
from PySide6.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QScrollArea, QFrame, QLineEdit)
from PySide6.QtCore import Qt, QSize
from modelos.modulo import Configuracion,session
from sqlalchemy import select
import json

class ItemWidget(QFrame):
    """Widget personalizado para cada fila de la lista"""
    def __init__(self, text, parent_list):
        super().__init__()
        self.setObjectName("ItemFrame")
        self.parent_list = parent_list
        
        # Layout principal de la tarjeta
        layout = QHBoxLayout(self)
        
        # Etiqueta de texto
        self.label = QLabel(text)
        self.label.setStyleSheet("font-size: 14px; color: #333; border: none;")
        
        # Botón de eliminar
        self.btn_delete = QPushButton("")
        self.btn_delete.setFixedSize(30, 30)
        self.btn_delete.setObjectName("DeleteButton")
        self.btn_delete.clicked.connect(self.remove_self)
        
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.btn_delete)

    def remove_self(self):
        """Elimina este widget del layout del padre"""
        self.setParent(None)
        self.deleteLater()

class ModernListApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Carreras")
        self.resize(400, 500)
        self.setStyleSheet(self.get_styles())

        # Layout Principal: marco exterior (margen) + contenedor interior
        self.outer_frame = QFrame(self)
        self.outer_frame.setObjectName("OuterFrame")
        self.outer_frame.setStyleSheet("#OuterFrame{background-color: #003366;}")
        self.outer_layout = QVBoxLayout(self.outer_frame)
        self.outer_layout.setContentsMargins(25, 25, 25, 25)
        self.outer_layout.setSpacing(0)

        # Contenedor interior donde irá el contenido real (fondo claro)
        self.inner_widget = QWidget()
        self.inner_widget.setObjectName("InnerContainer")
        self.main_layout = QVBoxLayout(self.inner_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        # --- SECCIÓN DE ENTRADA ---
        self.input_layout = QHBoxLayout()
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Escribe algo nuevo...")
        self.entry.returnPressed.connect(self.add_item) # Agregar con Enter
        
        self.add_btn = QPushButton("")
        self.add_btn.setObjectName("AddButton")
        self.add_btn.clicked.connect(self.add_item)
        
        self.input_layout.addWidget(self.entry)
        self.input_layout.addWidget(self.add_btn)
        self.main_layout.addLayout(self.input_layout)

        # --- ÁREA DE SCROLL (LISTA) ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        # Contenedor interno para los items
        self.container = QWidget()
        self.container.setObjectName("Container")
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setAlignment(Qt.AlignTop) # Alinea items arriba
        self.list_layout.setSpacing(10)
        
        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)

        # --- BOTONES DE ACCIÓN ---
        self.buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar")
        self.save_btn.setObjectName("SaveButton")
        self.save_btn.clicked.connect(self.on_save)

        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("CancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.cancel_btn)
        self.buttons_layout.addWidget(self.save_btn)
        self.main_layout.addLayout(self.buttons_layout)

        # Añadir el contenedor interior al marco exterior y fijar el layout del diálogo
        self.outer_layout.addWidget(self.inner_widget)
        dlg_layout = QVBoxLayout(self)
        dlg_layout.setContentsMargins(0, 0, 0, 0)
        dlg_layout.addWidget(self.outer_frame)

    def add_item(self):
        text = self.entry.text().strip()
        if text:
            new_item = ItemWidget(text, self.list_layout)
            self.list_layout.addWidget(new_item)
            self.entry.clear()

    def on_save(self):
        """Genera un JSON con los items visibles y cierra el diálogo aceptándolo."""
        data = {"carreras": self.stringlist}
        self.saved_json = json.dumps(data, ensure_ascii=False)
        print(data)
        self.accept()

    @property
    def stringlist(self):
        """Devuelve una lista de strings con los textos de los items actuales.

        Útil para enviar/almacenar en una base de datos.
        """
        items = []
        for i in range(self.list_layout.count()):
            w = self.list_layout.itemAt(i).widget()
            if hasattr(w, 'label'):
                items.append(w.label.text())
        return items

    def set_items(self, items):
        """Llena la lista con los strings provistos (por ejemplo, desde la BD)."""
        # Limpiar items actuales
        while self.list_layout.count():
            child = self.list_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
                child.widget().deleteLater()

        # Añadir nuevos items
        for text in items:
            if text is None:
                continue
            new_item = ItemWidget(str(text), self.list_layout)
            self.list_layout.addWidget(new_item)

    def get_styles(self):
        return """

            QWidget {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', sans-serif;
                
            }
            #InnerContainer{
                border-radius:6px;
                
            }
            QLineEdit {
                color:#000;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 8px;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid #003366;
            }
            #AddButton {
                background-color: #003366;
                color: white;
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
                qproperty-icon: url(resources/images/plus-large-svgrepo-com.svg);
                qproperty-iconSize: 25px 25px;
            }
            #AddButton:hover {
                background-color: #005a9e;
            }
            #ItemFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }
            #ItemFrame:hover {
                border: 1px solid #003366;
            }
            #DeleteButton {
                background-color: transparent;
                color: #ff4d4d;
                border-radius: 15px;
                font-size: 16px;
                qproperty-icon: url(resources/images/delete-1487-svgrepo-comR.svg);
                qproperty-iconSize: 20px 20px;
            }
            #DeleteButton:hover {
                background-color: #ffe6e6;
            }
            #Container {
                background-color: transparent;
            }
            #SaveButton {
                background-color: #2e8b57;
                color: white;
                padding: 8px 14px;
                border-radius: 8px;
                font-weight: bold;
            }
            #SaveButton:hover {
                background-color: #3aa46a;
            }
            #CancelButton {
                background-color: #777;
                color: white;
                padding: 8px 14px;
                border-radius: 8px;
            }
            #CancelButton:hover {
                background-color: #999;
            }
            QLabel{
                background-color:transparent;
            }
        """

if __name__ == "__main__":

    stmt=select(Configuracion).where(Configuracion.clave=="carreras")
    carreras=session.scalars(stmt).one_or_none()
    carreras_json=json.loads(carreras.valor.strip("'"))
    if isinstance(carreras_json, str):
        carreras_json = json.loads(carreras_json)
    app = QApplication(sys.argv)
    dialog = ModernListApp()
    dialog.set_items(carreras_json["carreras"])
    
    result = dialog.exec()
    # Si el usuario pulsó Guardar, `saved_json` estará disponible
    if hasattr(dialog, 'saved_json'):
        carreras.valor=json.dumps(dialog.saved_json, ensure_ascii=False)
        session.commit()
    sys.exit(result)