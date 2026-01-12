import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QFrame
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PIL import Image
import numpy as np

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
    
if __name__=="__main__":

    convertir_pil_a_pixmap()
