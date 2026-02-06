
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from docxtpl import DocxTemplate,InlineImage
from docx.shared import Mm, Cm, Inches
import jinja2
from modelos.modulo import Pasantia,Enterprise,session,Configuracion
import datetime
import os
from herramientas.conversiones import mes_espanol,convertir_a_romano,fecha_espanol,formato_miles, nombreCompleto,nombreParcial

def reemplazar_texto(datos:Pasantia,filename,name):
    conf=session.query(Configuracion).all()
    dic_conf=dict((i.clave,i.valor) for i in conf)
    doc = DocxTemplate(filename)
    jinja_env = jinja2.Environment()
    jinja_env.filters['fecha_es'] = fecha_espanol
    jinja_env.filters['miles'] = formato_miles
    jinja_env.filters['romanos'] = convertir_a_romano
    jinja_env.filters['mes'] = mes_espanol
    jinja_env.filters['completo'] = nombreCompleto
    jinja_env.filters['parcial'] = nombreParcial
    perfil_pasante=InlineImage(doc,datos.student.foto,width=Mm(32),height=Mm(35))
    contexto={
        'hoy':datetime.datetime.now(),
        #datos
        'estudiante':datos.student,
        'foto_estudiante':perfil_pasante,
        'empresa':datos.empresa,
        'tutor_academico':datos.tutor_academico,
        'tutor_empresarial':datos.tutor_academico,
        'carrera': str(datos.carrera),
        'semestre': datos.semestre,
        'lapso': str(datos.lapso_academico),
        'inicio': datos.inicio_pasantias,
        'final': datos.final_pasantias,
        'departamento': datos.departamento,
        'estado': datos.estado,
        'trabajo_asignado': datos.trabajo_asignado,
        'titulo_de_informe': datos.titulo_de_informe,
        'autoridad_empresa':datos.jefe_de_carta,
        'cargo_empresa':datos.cargo_jefe_de_carta
       }
    contexto.update(dic_conf)

    # 3. Renderizar (rellenar) el documento
    doc.render(contexto,jinja_env)

    # 4. Guardar el resultado final
    nombre=name
    doc.save(nombre)

    try:
        os.startfile(nombre)
    except AttributeError:
        # Esto ocurre si intentas correr este código en Mac o Linux
        print("os.startfile solo funciona en Windows.")

if __name__ == "__main__":
    pasante=session.query(Enterprise).where(Enterprise.id==8).one_or_none()
    print(type(pasante.pasantias))
    conf=session.query(Configuracion).all()
    print(dict((i.clave,i.valor) for i in conf))
    #reemplazar_texto(pasante,"formatos/1. CARTA SOLICITUD DE PASANTIA.docx","prueba.docx")

    context = {
        #estudiante
        'primer_nombre_estudiante': str(datos.student.primer_nombre),
        'segundo_nombre_estudiante': datos.student.segundo_nombre,
        'primer_apellido_estudiante': str(datos.student.primer_apellido),
        'segundo_apellido_estudiante': datos.student.segundo_apellido,
        'cedula_estudiante': str(datos.student.cedula),
        'sexo_estudiante': str(datos.student.sexo),
        'telefono_estudiante': datos.student.telefono,
        'email_estudiante': str(datos.student.email),
        'direccion_estudiante': datos.student.direccion,
        'fecha_nacimiento_estudiante': str(datos.student.fecha_de_nacimiento),
        #empresa
        'rif': str(datos.empresa.rif) if not datos.empresa else None,
        'razon_social': str(datos.empresa.razon_social) if not datos.empresa else None,
        'direccion_empresa': str(datos.empresa.direccion) if not datos.empresa else None,
        'email_empresa': str(datos.empresa.email) if not datos.empresa else None,
        'telefono_empresa': datos.empresa.telefono if not datos.empresa else None,
        'rubro_empresa': datos.empresa.rubro if not datos.empresa else None,
        #Tutor Academico
        'primer_nombre_tutorA':datos.tutor_academico.primer_nombre if not datos.tutor_academico else None,
        'segundo_nombre_tutorA':datos.tutor_academico.segundo_nombre if not datos.tutor_academico else None,
        'primer_apellido_tutorA':datos.tutor_academico.primer_apellido if not datos.tutor_academico else None,
        'segundo_apellido_tutorA':datos.tutor_academico.segundo_apellido if not datos.tutor_academico else None,
        'sexo_tutorA':datos.tutor_academico.sexo if not datos.tutor_academico else None,
        'cedula_tutorA':str(datos.tutor_academico.cedula) if not datos.tutor_academico else None,        
        'email_tutorA':datos.tutor_academico.email if not datos.tutor_academico else None,
        'telefono_tutorA':datos.tutor_academico.telefono if not datos.tutor_academico else None,
        'fecha_nacimiento_tutorA': datos.tutor_academico.fecha_de_nacimiento if not datos.tutor_academico else None,
        'especialidad': str(datos.tutor_academico.especialidad) if not datos.tutor_academico else None,
        #Tutor Empresarial
        'primer_nombre_tutorE':datos.tutor_empresarial.primer_nombre if not datos.tutor_empresarial else None,
        'segundo_nombre_tutorE':datos.tutor_empresarial.segundo_nombre if not datos.tutor_empresarial else None,
        'primer_apellido_tutorE':datos.tutor_empresarial.primer_apellido if not datos.tutor_empresarial else "",
        'segundo_apellido_tutorE':datos.tutor_empresarial.segundo_apellido if not datos.tutor_empresarial else None,
        'sexo_tutorE':datos.tutor_empresarial.sexo if not datos.tutor_empresarial else None,
        'cedula_tutorE':str(datos.tutor_empresarial.cedula) if not datos.tutor_empresarial else None,        
        'email_tutorE':datos.tutor_empresarial.email if not datos.tutor_empresarial else None,
        'telefono_tutorE':datos.tutor_empresarial.telefono if not datos.tutor_empresarial else None,
        'fecha_nacimiento_tutorE': datos.tutor_empresarial.fecha_de_nacimiento if not datos.tutor_empresarial else None,
        'cargo': str(datos.tutor_empresarial) if not datos.tutor_empresarial else None,
        #pasantia
        'carrera': str(datos.carrera),
        'semestre': str(datos.semestre),
        'lapso_academico': str(datos.lapso_academico),
        'inicio': datos.inicio_pasantias,
        'final': datos.final_pasantias,
        'departamento': datos.departamento,
        'estado': datos.estado,
        'trabajo_asignado': datos.trabajo_asignado,
        'titulo_de_informe': datos.titulo_de_informe,
    }