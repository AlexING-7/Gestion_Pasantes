# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
import sys
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.wrapper_layout = QVBoxLayout(self.centralwidget)
        self.wrapper_layout.setObjectName(u"wrapper_layout")
        self.main_container = QFrame(self.centralwidget)
        self.main_container.setObjectName(u"main_container")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_container.sizePolicy().hasHeightForWidth())
        self.main_container.setSizePolicy(sizePolicy)
        self.main_container.setStyleSheet(u"#main_container{\n"
"	background-color: #fff;\n"
"	border-radius:9px;\n"
"}")
        self.main_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_container.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_principal = QVBoxLayout(self.main_container)
        self.layout_principal.setSpacing(0)
        self.layout_principal.setObjectName(u"layout_principal")
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.title_bar = QFrame(self.main_container)
        self.title_bar.setObjectName(u"title_bar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.title_bar.sizePolicy().hasHeightForWidth())
        self.title_bar.setSizePolicy(sizePolicy1)
        self.title_bar.setMinimumSize(QSize(0, 30))
        self.title_bar.setStyleSheet(u"QFrame{\n"
"	background-color: #004080; \n"
"	padding:0px;\n"
"}\n"
"#title_bar{\n"
"	border-top-right-radius:9px; \n"
"	border-top-left-radius:9px;\n"
"\n"
"}")
        self.title_bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.title_bar.setFrameShadow(QFrame.Shadow.Raised)
        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setSpacing(0)
        self.title_layout.setObjectName(u"title_layout")
        self.title_layout.setContentsMargins(15, 0, 0, 0)
        self.title_label = QLabel(self.title_bar)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setStyleSheet(u"padding:0px;")

        self.title_layout.addWidget(self.title_label)

        self.horizontalSpacer = QSpacerItem(599, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.title_layout.addItem(self.horizontalSpacer)

        self.btn_min = QPushButton(self.title_bar)
        self.btn_min.setObjectName(u"btn_min")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_min.sizePolicy().hasHeightForWidth())
        self.btn_min.setSizePolicy(sizePolicy2)
        self.btn_min.setStyleSheet(u"QPushButton{\n"
"	\n"
"	background-color: transparent;\n"
"	padding:0px;\n"
"	border:none;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	background-color: #3366CC;\n"
"	\n"
"}")
        icon = QIcon()
        icon.addFile(u"./resources/images/window-minimize-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_min.setIcon(icon)
        self.btn_min.setIconSize(QSize(25, 25))

        self.title_layout.addWidget(self.btn_min)

        self.btn_max = QPushButton(self.title_bar)
        self.btn_max.setObjectName(u"btn_max")
        sizePolicy2.setHeightForWidth(self.btn_max.sizePolicy().hasHeightForWidth())
        self.btn_max.setSizePolicy(sizePolicy2)
        self.btn_max.setStyleSheet(u"QPushButton{\n"
"	\n"
"	background-color: transparent;\n"
"	padding:0px;\n"
"	border:none;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	background-color: #3366CC;\n"
"	\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"./resources/images/window-maximize-symbolic-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_max.setIcon(icon1)
        self.btn_max.setIconSize(QSize(25, 25))

        self.title_layout.addWidget(self.btn_max)

        self.btn_close = QPushButton(self.title_bar)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy2.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy2)
        self.btn_close.setStyleSheet(u"QPushButton{\n"
"	\n"
"	background-color: transparent;\n"
"	padding:0px;\n"
"	border:none;\n"
"	border-top-right-radius:9px;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	background-color: rgb(232, 17, 35);\n"
"	\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u"./resources/images/close-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_close.setIcon(icon2)
        self.btn_close.setIconSize(QSize(25, 25))

        self.title_layout.addWidget(self.btn_close)


        self.layout_principal.addWidget(self.title_bar)


        self.wrapper_layout.addWidget(self.main_container)

        MainWindow.setCentralWidget(self.centralwidget)
        # Evitar que el fondo por defecto de MainWindow asome en las esquinas redondeadas
        MainWindow.setStyleSheet("background: transparent;")
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.statusbar.setObjectName(u"statusbar")
        #MainWindow.setStatusBar(self.statusbar)
        
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"MENU!!!!!!!!!!!!!!!", None))
        self.btn_min.setText("")
        self.btn_max.setText("")
        self.btn_close.setText("")
    # retranslateUi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

