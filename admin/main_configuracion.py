
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
import json
from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox,QFileDialog,QTableWidgetItem,QHBoxLayout,QStyle,QLineEdit,QAbstractScrollArea
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import  QIcon
from PySide6.QtUiTools import QUiLoader
from sqlalchemy import select,delete
from modelos.modulo import session,Configuracion,SistemaLog
from herramientas.conversiones import convertir_a_json
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QEvent

class StackConfig():
    
    def __init__(self,main):
        self.main=main
        self.window=main.window
        self.window.stackedWidget.setCurrentIndex(7)
        self.tamano_pagina = 15
        self.numero_pagina = 1
        self.conectar_eventos()
    
    def asinedWidgets(self):
        self.input_ciudad=self.window.input_ciudad
        self.input_escuela=self.window.input_escuela
        self.input_autoridad1=self.window.input_autoridad1
        self.input_cargoAutoridad1=self.window.input_cargoAutoridad1
        self.input_autoridad2=self.window.input_autoridad2
        self.input_cargoAutoridad2=self.window.input_cargoAutoridad2
        self.input_lapsoActual=self.window.input_lapsoActual
        self.input_inicioLapsoActual=self.window.input_inicioLapsoActual
        self.input_finalLapsoActual=self.window.input_finalLapsoActual
        self.input_horasMinimas=self.window.input_horasMinimas
        self.input_escalaNotas=self.window.input_escalaNotas
        self.input_notaMinima=self.window.input_notaMinima
        self.input_porcentajeTutorA=self.window.input_porcentajeTutorA
        self.input_porcentajeTutorE=self.window.input_porcentajeTutorE
        self.input_porcentajeTaller=self.window.input_porcentajeTaller
        self.input_porcentajeExposicion=self.window.input_porcentajeExposicion
        self.input_newUser=self.window.input_newUser
        self.input_passwordActual=self.window.input_passwordActual
        self.input_newPassword=self.window.input_newPassword
        self.input_repeatNewPassword=self.window.input_repeatNewPassword
        self.btnGenCopiaSeguridad=self.window.btnGenCopiaSeguridad
        self.btnRestaurarBD=self.window.btnRestaurarBD
        self.btnBorrarLogs=self.window.btnBorrarLogs
        self.rutaDocumentos=self.window.rutaDocumentos
        self.rutaTemporales=self.window.rutaTemporales
    def toolstips(self):
        self.input_ciudad.setToolTip("<b>Ejemplo:<br> Barinas")
        self.input_escuela.setToolTip("<b>Ejemplo:<br> Institulo Politecnico...")
        self.input_autoridad1.setToolTip("<b>Autoridad Firmante</b><br>Ejemplo:<br> Ing. Febe Montilva")
        self.input_autoridad2.setToolTip("<b>Autoridad Firmante</b><br>Ejemplo:<br> Lcda. Maria Lopez")
        self.input_cargoAutoridad2.setToolTip("<b>Cargo Autoridad Firmante</b><br>Ejemplo:<br> Jefe de Pasantias")
        self.input_cargoAutoridad2.setToolTip("<b>Cargo Autoridad Firmante</b><br>Ejemplo:<br> Coordinadora de la Extension")
        self.input_lapsoActual.setToolTip("<b>Lapso Actual</b><br>Ejemplo:<br> 2026-1")
        self.input_inicioLapsoActual.setToolTip("<b>Inicio de Lapso Actual</b><br>Ejemplo:<br> 01/02/2026")
        self.input_finalLapsoActual.setToolTip("<b>Final de Lapso Actual</b><br>Ejemplo:<br> 01/06/2026")
        self.input_horasMinimas.setToolTip("<b>Horas Minimas</b><br>Ejemplo:<br> 120")
        self.input_escalaNotas.setToolTip("<b>Escala de Notas</b><br>Ejemplo:<br> 1-20")
        self.input_notaMinima.setToolTip("<b>Nota Minima</b><br>Ejemplo:<br> 10")
        self.input_porcentajeTutorA.setToolTip("Ejemplo:<br> 40")
        self.input_porcentajeTutorE.setToolTip("Ejemplo:<br> 40")
        self.input_porcentajeExposicion.setToolTip("Ejemplo:<br> 15")
        self.input_porcentajeTaller.setToolTip("Ejemplo:<br> 15")
    def conectar_eventos(self):
        self.asinedWidgets()
        self.toolstips()
        # Cargar valores desde la base de datos a los widgets al iniciar
        try:
            self.cargar_configuracion()
        except Exception as e:
            print(f"Error cargando configuración inicial: {e}")
        self.window.guardar1.clicked.connect(self.guardar1)
        self.btnBorrarLogs.clicked.connect(self.borrarLogs)
        self.window.btnConfCarreras.clicked.connect(self.verCarreras)
        self.window.btnConfFormatos.clicked.connect(self.verFormatos)
        self.window.btnGenCopiaSeguridad.clicked.connect(self.copiarbase)
        self.window.btnRestaurarBD.clicked.connect(self.restaurarBD)

    def cargar_configuracion(self):
        mapeo = {
                "ciudad":"input_ciudad",
                "escuela":"input_escuela",
                "autoridad_firmante_1": "input_autoridad1",
                "cargo_autoridad_firmante_1": "input_cargoAutoridad1",
                "autoridad_firmante_2": "input_autoridad2",
                "cargo_autoridad_firmante_2": "input_cargoAutoridad2",
                "lapso_actual": "input_lapsoActual",
                "inicio_lapso_actual": "input_inicioLapsoActual",
                "final_lapso_actual": "input_finalLapsoActual",
                "horas_minimas": "input_horasMinimas",
                "escala_notas": "input_escalaNotas",
                "nota_minima": "input_notaMinima",
                "porcentaje_tutor_academico": "input_porcentajeTutorA",
                "porcentaje_tutor_empresarial": "input_porcentajeTutorE",
                "porcentaje_taller": "input_porcentajeTaller",
                "porcentaje_exposicion": "input_porcentajeExposicion"
                }

        claves = list(mapeo.keys())
        registros = session.execute(
            select(Configuracion).where(Configuracion.clave.in_(claves))
        ).scalars().all()

        config_dict = {reg.clave: reg for reg in registros}

        for clave, nombre_widget in mapeo.items():
            if clave not in config_dict:
                continue
            valor = config_dict[clave].valor
            widget = getattr(self, nombre_widget, None)
            if widget is None:
                continue

            # Manejar QDateEdit (tienen setDate)
            if hasattr(widget, 'setDate'):
                try:
                    qd = QDate.fromString(valor, "dd/MM/yyyy")
                    if qd.isValid():
                        widget.setDate(qd)
                except Exception:
                    pass

            # Manejar spinboxes u objetos con setValue
            elif hasattr(widget, 'setValue'):
                try:
                    # intentar entero primero, si falla float
                    if '.' in str(valor):
                        widget.setValue(float(valor))
                    else:
                        widget.setValue(int(valor))
                except Exception:
                    try:
                        widget.setValue(float(valor))
                    except Exception:
                        pass

            # Por defecto usar setText si existe
            elif hasattr(widget, 'setText'):
                try:
                    widget.setText(valor)
                except Exception:
                    pass

    def guardar1(self):
        mapeo = {
                "ciudad":"input_ciudad",
                "escuela":"input_escuela",
                "autoridad_firmante_1": "input_autoridad1",
                "cargo_autoridad_firmante_1": "input_cargoAutoridad1",
                "autoridad_firmante_2": "input_autoridad2",
                "cargo_autoridad_firmante_2": "input_cargoAutoridad2",
                "lapso_actual": "input_lapsoActual",
                "inicio_lapso_actual": "input_inicioLapsoActual",
                "final_lapso_actual": "input_finalLapsoActual",
                "horas_minimas": "input_horasMinimas",
                "escala_notas": "input_escalaNotas",
                "nota_minima": "input_notaMinima",
                "porcentaje_tutor_academico": "input_porcentajeTutorA",
                "porcentaje_tutor_empresarial": "input_porcentajeTutorE",
                "porcentaje_taller": "input_porcentajeTaller",
                "porcentaje_exposicion": "input_porcentajeExposicion"
                }
        try:
            # 1. Carga masiva de lo que ya existe
            claves = list(mapeo.keys())
            registros = session.execute(
                select(Configuracion).where(Configuracion.clave.in_(claves))
            ).scalars().all()

            # Diccionario auxiliar: {clave: objeto_SQLAlchemy}
            config_dict = {reg.clave: reg for reg in registros}

            for clave, nombre_widget in mapeo.items():
                widget = getattr(self, nombre_widget)
                
                # 2. Obtener el valor del widget según su tipo
                if hasattr(widget, "date"): # QDateEdit
                    nuevo_valor = widget.date().toString("dd/MM/yyyy")
                elif hasattr(widget, "value"): # QSpinBox o QDoubleSpinBox
                    nuevo_valor = str(widget.value())
                else: # QLineEdit o similares
                    nuevo_valor = widget.text()

                # 3. Lógica de "Actualizar o Crear"
                if clave in config_dict:
                    # Actualiza el existente
                    config_dict[clave].valor = nuevo_valor
                else:
                    # Crea el registro nuevo porque no existía
                    nuevo_registro = Configuracion(clave=clave, valor=nuevo_valor)
                    session.add(nuevo_registro)
                    print(f"Creada nueva configuración: {clave}")

            # 4. Guardar todos los cambios (Updates e Inserts)
            session.commit()
            print("Datos guardados y sincronizados correctamente.")

        except Exception as e:
            session.rollback()
            print(f"Error crítico al guardar en la BD: {e}")

    def verCarreras(self):
        from admin.carreras import ModernListApp
        
        stmt=select(Configuracion).where(Configuracion.clave=="carreras")
        carreras=session.scalars(stmt).one_or_none()
        carreras_json=convertir_a_json(carreras.valor)

        dialog = ModernListApp()
        dialog.set_items(carreras_json["carreras"])
    
        dialog.exec()
        # Si el usuario pulsó Guardar, `saved_json` estará disponible
        if hasattr(dialog, 'saved_json'):
            carreras.valor=json.dumps(dialog.saved_json, ensure_ascii=False)
            session.commit()
            QMessageBox.information(self.main, "Éxito", "Se Guardaron las carreras en el sistema")
    
    def verFormatos(self):
        from admin.formato_docs import ModernListApp
        
        stmt=select(Configuracion).where(Configuracion.clave=="formatos")
        cfg = session.scalars(stmt).one_or_none()
        initial = {}
        if cfg and cfg.valor:
            try:
                initial = json.loads(cfg.valor)
                if isinstance(initial, str):
                    initial = json.loads(initial)
            except Exception:
                initial = {}

        dialog = ModernListApp()
        dialog.set_items(initial)
    
        dialog.exec()
        # Si el usuario pulsó Guardar, `saved_json` estará disponible
        if hasattr(dialog, 'saved_json'):
            if not cfg:
                cfg = Configuracion(clave="formatos", valor=dialog.saved_json)
                session.add(cfg)
            else:
                cfg.valor = dialog.saved_json
            session.commit()
            QMessageBox.information(None, "Éxito", "Se Guardaron los formatos en el sistema")
    
            
    def copiarbase(self):
        from herramientas.BD import respaldo_desde_url
        respaldo_desde_url("mysql+pymysql://root@127.0.0.1/gestion_pasantes")
    
    def restaurarBD(self):
        # Abrir diálogo para seleccionar archivo SQL o SQL.gz
        ruta, _ = QFileDialog.getOpenFileName(self.main, "Seleccionar respaldo SQL", str(Path.home()), "Archivos SQL (*.sql *.sql.gz);;Todos los archivos (*)")
        if not ruta:
            return

        resp = QMessageBox.question(self.main, "Restaurar Base de Datos",
            f"Se restaurará la base de datos desde:\n{ruta}\nEsto reemplazará los datos actuales. ¿Continuar?",
            QMessageBox.Yes | QMessageBox.No)
        if resp != QMessageBox.Yes:
            return

        try:
            import subprocess
            # Si es .gz, descomprimir al vuelo con gunzip; si no, redirigir el archivo al cliente mysql
            if ruta.lower().endswith(".gz"):
                cmd = f'gunzip -c "{ruta}" | mysql -u root -h 127.0.0.1 gestion_pasantes'
            else:
                cmd = f'mysql -u root -h 127.0.0.1 gestion_pasantes < "{ruta}"'

            resultado = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if resultado.returncode == 0:
                QMessageBox.information(self.main, "Éxito", "La base de datos fue restaurada correctamente.")
            else:
                QMessageBox.critical(self.main, "Error al restaurar", f"Salida:\n{resultado.stderr or resultado.stdout}")
        except FileNotFoundError:
            QMessageBox.critical(self.main, "Error", "No se encontró el cliente 'mysql' o 'gunzip'. Asegúrese de que estén instalados y en el PATH.")
        except Exception as e:
            QMessageBox.critical(self.main, "Error", f"Excepción al restaurar la BD:\n{e}")
    
    def borrarLogs(self):
        logs=delete(SistemaLog)
        session.execute(logs)

        session.commit()
        QMessageBox.information(self.main, "Éxito", "Se Eliminaron los Logs del Sistema")