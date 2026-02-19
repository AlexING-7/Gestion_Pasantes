import pandas as pd 
import json
from modelos.modulo import BaseModel

def exportar_modelo_a_excel(datos,ruta_archivo,entidad:BaseModel):
    data = []
    columns=entidad.__table__.columns.keys()
    
    for p in datos:
        diccionario=dict([(column,getattr(p,column,'No se Encuentra')) for column in columns])
        data.append(diccionario)
    
    df = pd.DataFrame(data)
    
    # 4. Guardar en Excel
    df.to_excel(ruta_archivo, index=False)
    print("Datos del ORM exportados correctamente.")
    
