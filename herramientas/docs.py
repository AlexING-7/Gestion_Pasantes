from docxtpl import DocxTemplate
from modelos.modulo import Pasantia
import os

def reemplazar_texto(datos:Pasantia,filename="herramientas/2.CARTA ACEPTACION DEL PASANTE.docx"):
    doc = DocxTemplate(filename)

    # 2. Crear el diccionario de datos (el contexto)
    # Las claves deben coincidir EXACTAMENTE con lo que pusiste en las {{ }}
    context = {
        #estudiante
        'primer_nombre_estudiante': str(datos.student.primer_nombre),
        'segundo_nombre_estudiante': str(datos.student.segundo_nombre),
        'primer_apellido_estudiante': str(datos.student.primer_apellido),
        'segundo_apellido_estudiante': str(datos.student.segundo_apellido),
        'cedula_estudiante': str(datos.student.cedula),
        'sexo_estudiante': str(datos.student.sexo),
        'telefono_estudiante': str(datos.student.telefono),
        'email_estudiante': str(datos.student.email),
        'carrera': str(datos.carrera),
        'semestre': str(datos.semestre)
    }

    # 3. Renderizar (rellenar) el documento
    doc.render(context)

    # 4. Guardar el resultado final
    nombre="acta_generada.docx"
    doc.save(nombre)

    try:
        os.startfile(nombre)
    except AttributeError:
        # Esto ocurre si intentas correr este código en Mac o Linux
        print("os.startfile solo funciona en Windows.")
