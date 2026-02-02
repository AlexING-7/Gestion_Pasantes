import pandas as pd 
import json
from modelos.modulo import Student

def exportar_modelo_a_excel(datos,ruta_archivo):
    data = []
    for p in datos:
        p:Student
        data.append({
            'ID': p.id,
            'Primer Nombre': p.primer_nombre,
            'Segundo Nombre': p.segundo_nombre,
            'Primer Apellido': p.primer_apellido,
            'Segundo Apellido': p.segundo_apellido,
            "Sexo":p.sexo,
            'Cedula': p.cedula,
            'Telefono':p.telefono,
            'Fecha de Nacimiento':str(p.fecha_de_nacimiento),
            'Email': p.email,
            'dirección':p.direccion,
        })
    
    df = pd.DataFrame(data)
    
    # 4. Guardar en Excel
    df.to_excel(ruta_archivo, index=False)
    print("Datos del ORM exportados correctamente.")
    
