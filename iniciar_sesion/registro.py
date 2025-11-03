from PySide6.QtWidgets import (QDialog,QLabel,QPushButton,QLineEdit,QMessageBox)
from PySide6.QtGui import QFont

class RegistrarUsuarioView(QDialog):
    
    def __init__(self):
        super().__init__()
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setGeometry(100,100,350,250)
        self.setWindowTitle("Registration")
        
        user_label=QLabel(self)
        user_label.setText("Usuario:")
        user_label.move(20,44)
        
        self.user_input=QLineEdit(self)
        self.user_input.resize(250,24)
        self.user_input.move(90,40)
        
        password1_label=QLabel(self)
        password1_label.setText("Password:")
        password1_label.setFont(QFont("Arial",10))
        password1_label.move(20,74)
        
        self.password1_input=QLineEdit(self)
        self.password1_input.resize(250,24)
        self.password1_input.move(90,70)
        self.password1_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        
        password2_label=QLabel(self)
        password2_label.setText("Password:")
        password2_label.setFont(QFont("Arial",10))
        password2_label.move(20,104)
        
        self.password2_input=QLineEdit(self)
        self.password2_input.resize(250,24)
        self.password2_input.move(90,100)
        self.password2_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        
        create_button = QPushButton(self)
        create_button.setText("Crear")
        create_button.resize(150,32)
        create_button.move(20,170)
        create_button.clicked.connect(self.crear_usuario)
        
        cancel_button = QPushButton(self)
        cancel_button.setText("Cancelar")
        cancel_button.resize(150,32)
        cancel_button.move(170,170)
        cancel_button.clicked.connect(self.cancelar_creacion)
        
    def cancelar_creacion(self):
        self.close()
        
    def crear_usuario(self):
        user_path="usuario.txt"
        usuario=self.user_input.text()
        password1=self.password1_input.text()
        password2=self.password2_input.text()
        
        if password1 == "" or password2 == "" or usuario == "":
            QMessageBox.warning(self,"Error",
            "datos invalidos",
            QMessageBox.StandardButton.Close,
            QMessageBox.StandardButton.Close)
        elif password1!=password2:
            QMessageBox.warning(self,"Error",
            "Las Contraseñas no Coinciden",
            QMessageBox.StandardButton.Close,
            QMessageBox.StandardButton.Close)
            
        else:
            try:
                with open(user_path,'+a') as f:
                    f.writelines(f"{usuario},{password1}\n")
                QMessageBox.information(self,"Usuario Registrado",
                                        "Usuario Registrado Correctamente",
                                        QMessageBox.StandardButton.Ok,
                                        QMessageBox.StandardButton.Ok)
                
            except FileNotFoundError as e:
                 QMessageBox.warning(self,"Error",
                f"No se encuentra {e}",
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
                