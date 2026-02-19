
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from docxtpl import DocxTemplate,InlineImage
from docx.shared import Mm, Cm, Inches
import jinja2
from modelos.modulo import Pasantia,Enterprise,session,Configuracion
import datetime
import os
from herramientas.conversiones import mes_espanol,convertir_a_romano,fecha_espanol,formato_miles, nombreCompleto,nombreParcial,sede_Sucursal

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
    jinja_env.filters['direccion'] = sede_Sucursal
    perfil_pasante=InlineImage(doc,datos.student.foto,width=Mm(32),height=Mm(35))
    contexto={
        'hoy':datetime.datetime.now(),
        #datos
        'datos':datos,
        'estudiante':datos.student,
        'foto_estudiante':perfil_pasante,
        'empresa':datos.empresa,
        'tutor_academico':datos.tutor_academico,
        'tutor_empresarial':datos.tutor_empresarial,
        'carrera': datos.carrera,
        'semestre': datos.semestre,
        'lapso': datos.lapso_academico,
        'inicio': datos.inicio_pasantias,
        'final': datos.final_pasantias,
        'departamento': datos.departamento,
        'estado': datos.estado,
        'trabajo_asignado': datos.trabajo_asignado,
        'titulo_de_informe': datos.titulo_de_informe,
        'autoridad_empresa':datos.jefe_de_carta,
        'cargo_empresa':datos.cargo_jefe_de_carta
       }
    contexto = {k: (v if v is not None else "N/A") for k, v in contexto.items()}
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

def asignacion_pasantias(datos,name="prueba.docx"):
    conf=session.query(Configuracion).all()
    dic_conf=dict((i.clave,i.valor) for i in conf)
    jinja_env = jinja2.Environment()
    jinja_env.filters['fecha_es'] = fecha_espanol
    jinja_env.filters['miles'] = formato_miles
    jinja_env.filters['romanos'] = convertir_a_romano
    jinja_env.filters['mes'] = mes_espanol
    jinja_env.filters['completo'] = nombreCompleto
    jinja_env.filters['parcial'] = nombreParcial
    jinja_env.filters['direccion'] = sede_Sucursal
    doc = DocxTemplate("formatos/ASIGNACION DE PASANTES.docx")
    
    contexto={"datos":datos,'hoy':datetime.datetime.now()}
    contexto.update(dic_conf)
    doc.render(contexto,jinja_env)
    doc.save(name)
    
    try:
        os.startfile(name)
    except AttributeError:
        # Esto ocurre si intentas correr este código en Mac o Linux
        print("os.startfile solo funciona en Windows.")


if __name__ == "__main__":
    pasantes=session.query(Pasantia).where(Pasantia.lapso_academico=="2025-2").all()
    #reemplazar_texto(pasante,"formatos/1. CARTA SOLICITUD DE PASANTIA.docx","prueba.docx")
    asignacion_pasantias(pasantes)
    