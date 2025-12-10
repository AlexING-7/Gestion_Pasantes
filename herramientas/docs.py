from docxtpl import DocxTemplate
import os

def reemplazar_texto(datos,filename="herramientas/2.CARTA ACEPTACION DEL PASANTE.docx"):
    doc = DocxTemplate(filename)

    # 2. Crear el diccionario de datos (el contexto)
    # Las claves deben coincidir EXACTAMENTE con lo que pusiste en las {{ }}
    context = {
        'nombre': str(datos.primer_nombre),
        'apellido': str(datos.primer_apellido),
        'cedula': str(datos.cedula),
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
