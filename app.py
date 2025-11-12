import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from PySide6.QtWidgets import QApplication
from iniciar_sesion.login import Login

if __name__=="__main__":
    app = QApplication(sys.argv)
    login=Login()
    login.sesion_activa()
    sys.exit(app.exec())