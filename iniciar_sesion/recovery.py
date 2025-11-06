
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox
# from PySide6.QtCore import QFile, QIODevice
# from PySide6.QtUiTools import QUiLoader
import modelos.modulo as db
# from getmac import get_mac_address as gma
from plantilla_ui import cargar_ui
import smtplib
import random
import string
import hashlib
from email.mime.text import MIMEText
from dotenv import load_dotenv

User=db.User
TSession=db.TSession
session=db.session

class RecoveryWindow:
    
    def __init__(self):
        load_dotenv()
        self.recovery_system = EmailPasswordRecovery(
                                smtp_server="smtp.gmail.com",
                                port=587,
                                email=os.getenv('SMTP_EMAIL'),
                                password=os.getenv('SMTP_PASSWORD'))
        self.window=cargar_ui("recovery.ui")
        self.conectar_eventos()
    
    def show(self):
        self.window.show()
    
    def close(self):
        self.window.close()    
    
    def conectar_eventos(self):
        self.window.emailButton.clicked.connect(self.send_email)
        self.window.comprobarButton.clicked.connect(self.verify)
        self.window.restablecerButton.clicked.connect(self.restablecer)
    
    def send_email(self):
        if not self.recovery_system.initiate_recovery(self.window.correo_input.text()):
            QMessageBox.information(self.window,"Email no Encontrado",
                                        "No existe Usuario con ese Email",
                                        QMessageBox.StandardButton.Ok,
                                        QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self.window,"Email",
                                            "Codigo Enviado Correctamente",
                                            QMessageBox.StandardButton.Ok,
                                            QMessageBox.StandardButton.Ok)

    def get_code(self):
        code=self.window.codigo_input1.text()+self.window.codigo_input2.text()+self.window.codigo_input3.text()+self.window.codigo_input4.text()+self.window.codigo_input5.text()+self.window.codigo_input6.text()
        return code
    
    def restablecer(self):
        new_password=self.window.newpassword_input.text()
        repeat_password=self.window.repeatpassword_input.text()
        if new_password==repeat_password:
            self.recovery_system.user.password=new_password
            session.commit()
            QMessageBox.information(self.window,"Contraseña Restablecida",
                                    "Se a cambiado la contraseña satisfactoriamente",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.warning(self.window,"Error",
                                "Las Contraseñas no son iguales",
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
    
    def verify(self):
        if self.recovery_system.verify_recovery_code(self.get_code()):
            QMessageBox.information(self.window,"Codigo Listo",
                                        "Ya puede cambiar de contraseña",
                                        QMessageBox.StandardButton.Ok,
                                        QMessageBox.StandardButton.Ok)
            self.window.newpassword_input.setReadOnly(False)
            self.window.repeatpassword_input.setReadOnly(False)
    
    
        
class EmailPasswordRecovery:
    def __init__(self, smtp_server, port, email, password):
        self.smtp_server = smtp_server  
        self.port = port                
        self.email = email             
        self.password = password       
        
    
    def generate_recovery_code(self):
        return ''.join(random.choices(string.digits, k=6))
    
    def send_recovery_email(self, user_email, recovery_code):
        try:
            # Crear el mensaje de email
            msg = MIMEText(f'Tu código de recuperación es: {recovery_code}')
            msg['Subject'] = 'Código de Recuperación de Contraseña'
            msg['From'] = self.email
            msg['To'] = user_email
            
            # Conectar y enviar email
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()           # Encriptación TLS
                server.login(self.email, self.password)  # Autenticación
                server.send_message(msg)    # Enviar mensaje
            return True
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False
    
    def user_exists(self,email:str):
        user=session.query(User).where(User.email==email.strip()).one_or_none()
        return user
    
    def initiate_recovery(self, email):
        self.user=self.user_exists(email)
        if not self.user:
            return False  # Usuario no existe
        
        user_email = self.user.email
        recovery_code = self.generate_recovery_code()
        self.recovery_code = recovery_code
        
        return self.send_recovery_email(user_email, recovery_code)
    
    def verify_recovery_code(self,  code):
        return self.recovery_code == code
    

    



        
    