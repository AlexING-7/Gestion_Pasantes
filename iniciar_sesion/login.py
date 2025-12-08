import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modelos.modulo import User,TSession,session
import os
import time
from PySide6.QtWidgets import (QApplication, QLabel,QMainWindow,QLineEdit,QPushButton,QMessageBox,QFileDialog)
from PySide6.QtGui import QFont, QPixmap
from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui


class Login(QMainWindow):
    
    def __init__(self):
        super(Login,self).__init__()
        self.logged=False
        self.window=cargar_ui("UI/login.ui",self)
        self.conectar_eventos()
        

    
    def sesion_activa(self):
        sesion_mac=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none()
        if sesion_mac:
            self.logged=True
            self.open_main_window()
        else:
            self.show()
   
    def conectar_eventos(self):
        self.window.check_view_password.toggled.connect(self.mostrar_password)
        self.window.login_Button.clicked.connect(self.iniciar_mainview)
        self.window.Olvido_ContrasenaButton.clicked.connect(self.open_recovery_window)

    def mostrar_password(self,clicked):
        if clicked:
            self.window.password_input.setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            self.window.password_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )
    
    def iniciar_mainview(self):
        user=session.query(User).where(User.username==self.window.user_input.text(),User.password==self.window.password_input.text()).one_or_none()
        sesion=TSession(mac_adresss=gma(),
                        data_session="uijfdiosjfoifdjiogjdfoginfdoignfdiognfdignjfdigfnjdigondfgujfndgiofdngjfdgnfdikjgnfdiogjniodgjiogjfkdijgndofigjnfiodgnfdiognfdiognfdignfdignfdiognfdiognfdiognignfdigndifgnfdignfdigndfiognfdiongifdgnfdiongfidognifdsgnaiunaiounmfusjinfugkijnb ufgjkeirngvujhynrbguhynrgahuyebngvefuhbnvguizsnburfi",
                        last_activity=int(time.time()))        
        

        try:

            if user:
                QMessageBox.information(self.window,"Usuario Inicio Sesión",
                                        f"Inicio Sesión Correctamente",
                                        QMessageBox.StandardButton.Ok,
                                        QMessageBox.StandardButton.Ok)
                user.tsessions.append(sesion)

                session.commit()
                self.close()
                self.open_main_window()
            else:
                QMessageBox.warning(self.window,"Error Mensaje",
                                f"Error Usuario No Encontrado",
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)

        except Exception as e:
            QMessageBox.warning(self.window,"Error Mensaje",
                                f"Error {e}",
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
        
    def open_main_window(self):
        from admin.main import MainWindow
        self.main_window=MainWindow()
        self.main_window.show()
        
    def open_recovery_window(self):
        from iniciar_sesion.recovery import RecoveryWindow
        self.recovery_window=RecoveryWindow()
        self.recovery_window.show()
        
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    login=Login()
    login.sesion_activa()
    sys.exit(app.exec())