import pandas as pd 
import json

def exportar_modelo_a_excel(datos,ruta_archivo):
    data = []
    for p in datos:
        data.append({
            'ID': p.id,
            'Nombre': p.primer_nombre,
            'Apellido': p.primer_apellido,
            'Email': p.email
        })
    
    df = pd.DataFrame(data)
    
    # 4. Guardar en Excel
    df.to_excel(ruta_archivo, index=False)
    print("Datos del ORM exportados correctamente.")
    
