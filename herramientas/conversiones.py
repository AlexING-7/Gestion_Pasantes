from datetime import date
import bcrypt
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QFrame
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PIL import Image
import json
import numpy as np


def null_string(string):
    if not string:
        return ""
    else:
        return string
    
def calcular_edad(fecha_nacimiento: date | None) -> int | None:
        """Devuelve la edad en años a partir de una fecha (objeto date)."""
        if not fecha_nacimiento:
            return None
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        return edad

def calcular_duracion_meses(inicio: date | None, final: date | None) -> int | None:
    """Devuelve la duración en meses entre dos fechas (aproximada en meses completos).

    Si `inicio` o `final` es None devuelve None.
    """
    if not inicio or not final:
        return None
    # Si final es anterior a inicio, devolver 0
    if final < inicio:
        return 0
    años = final.year - inicio.year
    meses = final.month - inicio.month
    dias_correction = 1 if final.day < inicio.day else 0
    total_meses = años * 12 + meses - dias_correction
    return total_meses

def convertir_a_romano(numero):

    
    # Mapeo de valores
    roman_map = {
        1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
        100: 'C', 90: 'XC', 50: 'L', 40: 'XL',
        10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'
    }
    
    # Conversión
    resultado = []
    for valor in sorted(roman_map.keys(), reverse=True):
        while numero >= valor:
            resultado.append(roman_map[valor])
            numero -= valor
    
    return ''.join(resultado)

def fecha_espanol(fecha):
    mes = mes_espanol(fecha)
    return f"{fecha.day} de {mes} de {fecha.year}"

def mes_espanol(fecha):
    meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    mes=meses[fecha.month - 1]
    return mes

def formato_miles(valor):
    if valor is None: return "0"
    # Formatea con coma (1,500) y luego reemplaza por punto (1.500)
    return "{:,.0f}".format(valor).replace(",", ".")

def nombreCompleto(name):
    segundoN=" "+name.segundo_nombre+" " if name.segundo_nombre else " "
    segundoA=" "+name.segundo_apellido if name.segundo_apellido else ""
    return f"{name.primer_nombre}{segundoN}{name.primer_apellido}{segundoA}"
def nombreParcial(name):
    return f"{name.primer_nombre} {name.primer_apellido}"
def cifrar(password:str):
    utf=password.encode("utf-8")
    sal=bcrypt.gensalt()
    return bcrypt.hashpw(utf, sal).decode('utf-8')

def convertir_pil_a_pixmap(ruta:str="ejemplo.jpg"):
        
    pil_image = Image.open(ruta)
    
    if pil_image.mode != "RGBA":
        pil_image = pil_image.convert("RGBA")
    
    

    
    pil_image = pil_image.resize((190, 190), resample=Image.Resampling.LANCZOS)
    
       
    array_img=np.array(pil_image)
    for y in range(0,190):
        for x in range(0,190):
            if ((95-y)**2+(95-x)**2)>95**2:
                array_img[y,x]=[0,0,0,0]
               
 
    nueva_imagen = Image.fromarray(array_img)

    width, height = nueva_imagen.size
    data = nueva_imagen.tobytes()

    q_image = QImage(data, width, height, QImage.Format_RGBA8888)

    # D. Convertir QImage a QPixmap (que es lo que usa el QLabel)
    q_pixmap = QPixmap.fromImage(q_image)

    return q_pixmap

def guion_telefono(telefono:str):
    return f"{telefono[0:4]}-{telefono[4:]}"

def convertir_a_json(valor:str):
    _json=json.loads(valor.strip("'"))
    if isinstance(_json, str):
        _json = json.loads(_json)
    return _json

def jsonFormatos():
    from sqlalchemy import select
    from modelos.modulo import Configuracion,session
    stmt = select(Configuracion.valor).where(Configuracion.clave == "formatos")
    cfg = session.scalars(stmt).one_or_none()
    return convertir_a_json(cfg)

def sede_Sucursal(dato):
    if dato.sede:
        return dato.empresa.razon_social
    else:
        return dato.direccion



if __name__=="__main__":
    print(jsonFormatos()['Carta de Postulación a Pasantía'])
