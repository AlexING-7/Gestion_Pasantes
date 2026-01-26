
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QHBoxLayout,QStyle,QLineEdit,QAbstractScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon
from PySide6.QtUiTools import QUiLoader

from modelos.modulo import session,User
from sqlalchemy import select
from sqlalchemy import or_,and_
from getmac import get_mac_address as gma
from herramientas.plantilla_ui import cargar_ui
from herramientas.conversiones import cifrar
from herramientas.modern_messagebox import ModernMessageBox
from PySide6.QtWidgets import QHeaderView


class StackUsers():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.tabla_users=self.window.tabla_users
        self.window.tabla_users.installEventFilter(main)
        self.conectar_eventos()
        
    def conectar_eventos(self):
        self.pag_users()
        self.window.usuarios_btnGuardar.clicked.connect(self.guardar)
        self.window.comboAccionUser.currentIndexChanged.connect(self.labelChange)
        
    def labelChange(self):
        if self.window.comboAccionUser.currentText()=="Create":
            self.window.labelCrearEditarUser.setText("Crear Usuario")
        elif self.window.comboAccionUser.currentText()=="Update":
            self.window.labelCrearEditarUser.setText("Editar Usuario")
    
    def guardar(self):
        if self.window.comboAccionUser.currentText()=="Create":
            self.crear()
        elif self.window.comboAccionUser.currentText()=="Update":
            self.edit()
    
    def header(self):
        header=self.tabla_users.horizontalHeader()
        #ced
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        #gmail
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        #rol
        self.tabla_users.setColumnWidth(2, 100)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        #accion
        self.tabla_users.setColumnWidth(3, 150)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
    
    def pag_users(self):
        self.header()
        users=self.get_data()
        self.tabla_users.setRowCount(0)
        for fila,user in enumerate(users):
            user:User
            self.tabla_users.insertRow(fila)
            
            self.tabla_users.setItem(fila,0,QTableWidgetItem(str(user.username)))
            self.tabla_users.setItem(fila,1,QTableWidgetItem(str(user.email)))
            self.tabla_users.setItem(fila,2,QTableWidgetItem(str(user.rol)))

                       
            widget_contenedor = QWidget()
            
            layout_botones = QHBoxLayout(widget_contenedor)
            
            layout_botones.setContentsMargins(5, 2, 5, 2) 
            layout_botones.setSpacing(10) 
            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(lambda checked,x=user: self.read(x))
            btn_borrar = QPushButton("Borrar")
            btn_borrar.clicked.connect(lambda checked,x=user: self.delete(x))

            btn_editar.setStyleSheet("background-color: #4CAF50; color: white;") 
            btn_borrar.setStyleSheet("background-color: #f44336; color: white;")                 

            layout_botones.addWidget(btn_editar)
            layout_botones.addWidget(btn_borrar)

            # 6. Insertar el contenedor en la celda
            self.tabla_users.setCellWidget(fila, 3, widget_contenedor)
            
    
    def get_data(self):
        stmt=select(User)
        return session.scalars(stmt).all()
    
    def crear(self):
        combo=self.window.comboAccionUser
        # Indicar modo 'create' en el combo
        try:
            combo.setCurrentText("Create")
        except Exception:
            try:
                combo.setCurrentIndex(0)
            except Exception:
                pass
        username=self.window.username_input.text()
        correo=self.window.correo_input.text()
        rol=self.window.rol_input.currentText()
        contraseña=self.window.password_input.text()
        confirmar_contraseña=self.window.confirmarPassword_input.text()
        # Validaciones básicas
        if not username or not correo or not contraseña or not confirmar_contraseña:
            QMessageBox.warning(self.window, "Campos incompletos", "Completa todos los campos requeridos.")
            return

        if contraseña != confirmar_contraseña:
            QMessageBox.warning(self.window, "Contraseñas no coinciden", "Las contraseñas ingresadas no coinciden.")
            return

        # Verificar duplicados (username o email)
        stmt = select(User).where(or_(User.username == username, User.email == correo))
        existing = session.scalars(stmt).first()
        if existing:
            if existing.username == username:
                QMessageBox.warning(self.window, "Usuario existente", "El nombre de usuario ya está en uso.")
            else:
                QMessageBox.warning(self.window, "Correo existente", "El correo ya está registrado.")
            return

        # Crear y persistir
        nuevo = User(username=username, password=cifrar(contraseña), email=correo, rol=rol)
        session.add(nuevo)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self.window, "Error al crear", f"No se pudo crear el usuario:\n{e}")
            return

        QMessageBox.information(self.window, "Usuario creado", "Usuario creado correctamente.")
        # Limpiar campos y refrescar tabla
        try:
            self.window.username_input.setText("")
            self.window.correo_input.setText("")
            self.window.contraseña_input.setText("")
            self.window.confirmarContraseña_input.setText("")
            if hasattr(self.window.rol_input, 'setCurrentIndex'):
                self.window.rol_input.setCurrentIndex(0)
        except Exception:
            pass

        self.pag_users()
        # Asegurar que el combo quede en modo 'create' después de crear
        try:
            combo.setCurrentText("create")
        except Exception:
            try:
                combo.setCurrentIndex(0)
            except Exception:
                pass
    
    def edit(self):
        """Actualizar `self.current_user` con los valores del formulario.

        Si se pasa `user`, lo establece como `current_user` antes de actualizar.
        """
        # Determinar usuario objetivo
        if not hasattr(self, 'current_user') or self.current_user is None:
            QMessageBox.warning(self.window, "Selecciona usuario", "Selecciona un usuario para editar.")
            return

        username = self.window.username_input.text().strip()
        correo = self.window.correo_input.text().strip()
        rol = self.window.rol_input.currentText() if hasattr(self.window.rol_input, 'currentText') else None
        contraseña = self.window.password_input.text()
        confirmar_contraseña = self.window.confirmarPassword_input.text()

        # Validaciones básicas
        if not username or not correo:
            QMessageBox.warning(self.window, "Campos incompletos", "El nombre de usuario y el correo son obligatorios.")
            return

        # Si el usuario cambia la contraseña, validar coincidencia
        if contraseña or confirmar_contraseña:
            if contraseña != confirmar_contraseña:
                QMessageBox.warning(self.window, "Contraseñas no coinciden", "Las contraseñas ingresadas no coinciden.")
                return

        # Comprobar duplicados (username/email) excluyendo al usuario actual
        stmt = select(User).where(
            or_(User.username == username, User.email == correo)
        )
        found = session.scalars(stmt).all()
        for f in found:
            if f.id != self.current_user.id:
                if f.username == username:
                    QMessageBox.warning(self.window, "Usuario existente", "El nombre de usuario ya está en uso.")
                    return
                if f.email == correo:
                    QMessageBox.warning(self.window, "Correo existente", "El correo ya está registrado.")
                    return

        # Aplicar cambios al objeto en sesión
        try:
            db_user = session.get(User, self.current_user.id)
            if db_user is None:
                QMessageBox.critical(self.window, "Error", "Usuario no encontrado en la base de datos.")
                return

            db_user.username = username
            db_user.email = correo
            db_user.rol = rol
            # Actualizar contraseña solo si el usuario ingresó una nueva
            if contraseña:
                db_user.password = cifrar(contraseña)

            session.add(db_user)
            session.commit()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self.window, "Error al actualizar", f"No se pudo actualizar el usuario:\n{e}")
            return

        QMessageBox.information(self.window, "Actualizado", "Usuario actualizado correctamente.")
        # Limpiar campos de contraseña por seguridad
        try:
            self.window.contraseña_input.setText("")
            self.window.confirmarContraseña_input.setText("")
        except Exception:
            pass

        # Refrescar vista
        self.pag_users()
    
    def delete(self,dato:User):
        msg = ModernMessageBox(
                title="Advertencia",
                text="<h3 style='color: #ff5555'>Eliminar Estudiante</h3>",
                informative_text="¿Esta seguro de eliminar esta información?",
                parent=self.main
            )

        btn_save, btn_cancel = msg.add_custom_buttons()
            
            # Ejecutamos el diálogo (Modal loop)
        msg.exec()

        # Verificamos qué botón fue presionado
        clicked = msg.clickedButton()
        
        if clicked == btn_save:
            session.delete(dato)
            session.commit()
            self.pag_users()
    
    def read(self,user:User):
        combo=self.window.comboAccionUser
        # Indicar modo 'update' en el combo
        try:
            combo.setCurrentText("Update")
        except Exception:
            try:
                # Si no existe el texto, intentar seleccionar la segunda opción
                combo.setCurrentIndex(1)
            except Exception:
                pass
        # Guardar referencia al usuario actual para operaciones posteriores
        self.current_user = user

        # Rellenar campos del formulario con los datos del usuario
        try:
            self.window.username_input.setText(user.username or "")
        except Exception:
            pass

        try:
            self.window.correo_input.setText(user.email or "")
        except Exception:
            pass

        # Rol: intentar seleccionar por texto en el widget (combo)
        try:
            if hasattr(self.window.rol_input, 'setCurrentText'):
                self.window.rol_input.setCurrentText(user.rol or "")
            elif hasattr(self.window.rol_input, 'findText') and hasattr(self.window.rol_input, 'setCurrentIndex'):
                idx = self.window.rol_input.findText(user.rol or "")
                if idx >= 0:
                    self.window.rol_input.setCurrentIndex(idx)
        except Exception:
            pass

        # Por seguridad, no mostrar la contraseña actual; limpiar campos de contraseña
        try:
            self.window.password_input.setText("")
            self.window.confirmarPassword_input.setText("")
        except Exception:
            pass

        # Si la UI necesita enfoque o cambio de pestaña, el llamador puede manejarlo
    
    
    