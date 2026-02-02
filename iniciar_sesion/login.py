import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modelos.modulo import User,TSession,session
import time
from PySide6.QtWidgets import (QApplication, QLabel,QMainWindow,QLineEdit,QPushButton,QMessageBox,QFileDialog)
from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from herramientas.logs import registrar_log
from PySide6.QtGui import QShortcut,QKeySequence
from bcrypt import checkpw
from herramientas.CustomMain import CustomWindow
class Login(CustomWindow):
    
    def __init__(self):
        super(Login,self).__init__()
        self.logged=False
        self.window=cargar_ui("UI/login.ui",self)
        self.layout_principal.addWidget(self.window)
        self.conectar_eventos()
        

    
    def sesion_activa(self):
        sesion_mac=session.query(TSession).where(TSession.mac_adresss==gma()).one_or_none()
        if sesion_mac:
            self.logged=True
            
            if sesion_mac.user.rol=="Administrador":
                self.open_main_window()
                registrar_log(session=session,
                              usuario=sesion_mac.user.username,
                              accion="LOGIN",
                              mensaje="Login Rol Administrador",
                              )
            elif sesion_mac.user.rol=="Coordinador":
                self.open_main_coord_window()
                registrar_log(session=session,
                              usuario=sesion_mac.user.username,
                              accion="LOGIN",
                              mensaje="Login Rol Coordinador",
                              )
        else:
            self.show()
   
    def conectar_eventos(self):
        self.window.check_view_password.toggled.connect(self.mostrar_password)
        self.window.login_Button.clicked.connect(self.iniciar_mainview)
        self.window.Olvido_ContrasenaButton.clicked.connect(self.open_recovery_window)
        self.atajos()
        
    def atajos(self):
        self.atajo_secreto = QShortcut(QKeySequence("Return"), self.window)
        self.atajo_secreto.activated.connect(self.iniciar_mainview)

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
        user=session.query(User).where(User.username==self.window.user_input.text()).one_or_none()
        sesion=TSession(mac_adresss=gma(),
                        data_session="uijfdiosjfoifdjiogjdfoginfdoignfdiognfdignjfdigfnjdigondfgujfndgiofdngjfdgnfdikjgnfdiogjniodgjiogjfkdijgndofigjnfiodgnfdiognfdiognfdignfdignfdiognfdiognfdiognignfdigndifgnfdignfdigndfiognfdiongifdgnfdiongfidognifdsgnaiunaiounmfusjinfugkijnb ufgjkeirngvujhynrbguhynrgahuyebngvefuhbnvguizsnburfi",
                        last_activity=int(time.time()))        
        

        try:
            if user:
                if checkpw(self.window.password_input.text().encode(),user.password.encode()):
                    QMessageBox.information(self.window,"Usuario Inicio Sesión",
                                            f"Inicio Sesión Correctamente",
                                            QMessageBox.StandardButton.Ok,
                                            QMessageBox.StandardButton.Ok)
                    user.tsessions.append(sesion)

                    session.commit()
                    self.close()
                    if user.rol=="Administrador":
                        self.open_main_window()
                        registrar_log(session=session,
                              usuario=user.username,
                              accion="LOGIN",
                              mensaje="Login Rol Administrador",
                              )
                    elif user.rol=="Coordinador":
                        self.open_main_coord_window()
                        registrar_log(session=session,
                              usuario=user.username,
                              accion="LOGIN",
                              mensaje="Login Rol Coordinador",
                              )
                else:
                    QMessageBox.warning(self.window,"Error Mensaje",
                                f"Contraseña Incorrecta",
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
            else:
                QMessageBox.warning(self.window,"Error Mensaje",
                                f"Error Usuario No Encontrado",
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)

        except Exception as e:
            print(e)
            QMessageBox.warning(self.window,"Error Mensaje",
                                f"Error {e}",
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
        
    def open_main_window(self):
        from admin.main import MainWindow
        self.main_window=MainWindow()
        self.main_window.show()

    def open_main_coord_window(self):
        from coord.main import MainWindow as coordMainWindow
        self.main_window=coordMainWindow()
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