from docxtpl import DocxTemplate
from modelos.modulo import Pasantia
import os
from herramientas.conversiones import null_string

def reemplazar_texto(datos:Pasantia,filename,name):
    doc = DocxTemplate(filename)

    # 2. Crear el diccionario de datos (el contexto)
    # Las claves deben coincidir EXACTAMENTE con lo que pusiste en las {{ }}
    context = {
        #estudiante
        'primer_nombre_estudiante': str(datos.student.primer_nombre),
        'segundo_nombre_estudiante': null_string(datos.student.segundo_nombre),
        'primer_apellido_estudiante': str(datos.student.primer_apellido),
        'segundo_apellido_estudiante': null_string(datos.student.segundo_apellido),
        'cedula_estudiante': str(datos.student.cedula),
        'sexo_estudiante': str(datos.student.sexo),
        'telefono_estudiante': null_string(datos.student.telefono),
        'email_estudiante': str(datos.student.email),
        'direccion_estudiante': null_string(datos.student.direccion),
        'fecha_nacimiento_estudiante': null_string(str(datos.student.fecha_de_nacimiento)),
        #empresa
        'rif': str(datos.empresa.rif) if not datos.empresa else "",
        'razon_social': str(datos.empresa.razon_social) if not datos.empresa else "",
        'direccion_empresa': str(datos.empresa.direccion) if not datos.empresa else "",
        'email_empresa': str(datos.empresa.email) if not datos.empresa else "",
        'telefono_empresa': null_string(datos.empresa.telefono) if not datos.empresa else "",
        'rubro_empresa': null_string(datos.empresa.rubro) if not datos.empresa else "",
        #Tutor Academico
        'primer_nombre_tutorA':datos.tutor_academico.primer_nombre if not datos.tutor_academico else "",
        'segundo_nombre_tutorA':null_string(datos.tutor_academico.segundo_nombre) if not datos.tutor_academico else "",
        'primer_apellido_tutorA':datos.tutor_academico.primer_apellido if not datos.tutor_academico else "",
        'segundo_apellido_tutorA':null_string(datos.tutor_academico.segundo_apellido) if not datos.tutor_academico else "",
        'sexo_tutorA':datos.tutor_academico.sexo if not datos.tutor_academico else "",
        'cedula_tutorA':str(datos.tutor_academico.cedula) if not datos.tutor_academico else "",        
        'email_tutorA':datos.tutor_academico.email if not datos.tutor_academico else "",
        'telefono_tutorA':null_string(datos.tutor_academico.telefono) if not datos.tutor_academico else "",
        'fecha_nacimiento_tutorA': null_string(datos.tutor_academico.fecha_de_nacimiento) if not datos.tutor_academico else "",
        'especialidad': str(datos.tutor_academico.especialidad) if not datos.tutor_academico else "",
        #Tutor Empresarial
        'primer_nombre_tutorE':datos.tutor_empresarial.primer_nombre if not datos.tutor_empresarial else "",
        'segundo_nombre_tutorE':null_string(datos.tutor_empresarial.segundo_nombre) if not datos.tutor_empresarial else "",
        'primer_apellido_tutorE':datos.tutor_empresarial.primer_apellido if not datos.tutor_empresarial else "",
        'segundo_apellido_tutorE':null_string(datos.tutor_empresarial.segundo_apellido) if not datos.tutor_empresarial else "",
        'sexo_tutorE':datos.tutor_empresarial.sexo if not datos.tutor_empresarial else "",
        'cedula_tutorE':str(datos.tutor_empresarial.cedula) if not datos.tutor_empresarial else "",        
        'email_tutorE':datos.tutor_empresarial.email if not datos.tutor_empresarial else "",
        'telefono_tutorE':null_string(datos.tutor_empresarial.telefono) if not datos.tutor_empresarial else "",
        'fecha_nacimiento_tutorE': null_string(datos.tutor_empresarial.fecha_de_nacimiento) if not datos.tutor_empresarial else "",
        'cargo': str(datos.tutor_empresarial) if not datos.tutor_empresarial else "",
        #pasantia
        'carrera': str(datos.carrera),
        'semestre': str(datos.semestre),
        'lapso_academico': str(datos.lapso_academico),
        'inicio': null_string(datos.inicio_pasantias),
        'final': null_string(datos.final_pasantias),
        'departamento': null_string(datos.departamento),
        'estado': datos.estado,
        'trabajo_asignado': null_string(datos.trabajo_asignado),
        'titulo_de_informe': null_string(datos.titulo_de_informe),
    }

    # 3. Renderizar (rellenar) el documento
    doc.render(context)

    # 4. Guardar el resultado final
    nombre=name
    doc.save(nombre)

    try:
        os.startfile(nombre)
    except AttributeError:
        # Esto ocurre si intentas correr este código en Mac o Linux
        print("os.startfile solo funciona en Windows.")
