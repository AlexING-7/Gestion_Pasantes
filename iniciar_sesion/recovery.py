
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
# from PySide6.QtWidgets import QWidget, QLabel, QMessageBox
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

User=db.User
TSession=db.TSession
session=db.session

class RecoveryWindow:
    
    def __init__(self):
        self.recovery_system = EmailPasswordRecovery(
                                smtp_server="smtp.gmail.com",
                                port=587,
                                email="juegosintercarreras@gmail.com",
                                password="pxgt sqzr thfp rqel")
        self.window=cargar_ui("recovery.ui")
        self.conectar_eventos()
    
    def show(self):
        self.window.show()
    
    def close(self):
        self.window.close()    
    
    def conectar_eventos(self):
        self.window.emailButton.clicked.connect(self.get_code)
        

    def get_code(self):
        code=self.window.codigo_input1.text()+self.window.codigo_input2.text()+self.window.codigo_input3.text()+self.window.codigo_input4.text()+self.window.codigo_input5.text()+self.window.codigo_input6.text()
        return code
        
class EmailPasswordRecovery:
    def __init__(self, smtp_server, port, email, password):
        self.smtp_server = smtp_server  
        self.port = port                
        self.email = email             
        self.password = password       
        self.recovery_codes = {}        
    
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
    
    def user_exists(self,email):
        user=session.query(User).where(User.email==email).one_or_none()
        return user
    
    def initiate_recovery(self, email):
        user=self.user_exists(email)
        if not user:
            return False  # Usuario no existe
        
        user_email = user.email
        recovery_code = self.generate_recovery_code()
        self.recovery_codes[user.email] = recovery_code
        
        return self.send_recovery_email(user_email, recovery_code)
    
    def verify_recovery_code(self, useremail, code):
        return (useremail in self.recovery_codes and 
                self.recovery_codes[useremail] == code)
    
if __name__=="__main__":
    # 1. Configurar el sistema
    recovery_system = EmailPasswordRecovery(
        smtp_server="smtp.gmail.com",
        port=587,
        email="juegosintercarreras@gmail.com",
        password="pxgt sqzr thfp rqel"
    )

    # 2. Usuario solicita recuperación
    username = "alexander30409@gmail.com"
    if recovery_system.initiate_recovery(username):
        print("✅ Código enviado al email registrado")
        
        # 3. Usuario ingresa el código recibido
        codigo_recibido = input("Ingresa el código de 6 dígitos: ")
        
        # 4. Verificar código
        if recovery_system.verify_recovery_code(username, codigo_recibido):
            nueva_contraseña = input("Ingresa tu nueva contraseña: ")

            
        else:
            print("❌ Código incorrecto o expirado")
    else:
        print("❌ Usuario no encontrado o error enviando email")

    



        
    