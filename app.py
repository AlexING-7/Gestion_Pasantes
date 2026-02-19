import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from PySide6.QtWidgets import QApplication
from iniciar_sesion.login import Login
if __name__=="__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QToolTip { background-color: #f1f1f1; color: white; border: 1px solid #444; padding: 5px; }")
    login=Login()
    login.sesion_activa()
    sys.exit(app.exec())