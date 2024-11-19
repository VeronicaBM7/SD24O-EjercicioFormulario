from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import shutil
import os #para acceder a la ruta del home
import uuid #Genera un nombre aleatoreo unico

# creación del servidor
app = FastAPI()



#Form(...)  -> operador elipsis 
@app.post("/fotos")
async def guarda_foto(nombre:str=Form(None),direccion:str=Form(None), check:bool=Form(None),foto:UploadFile=File(...)):
    print("Titulo: ", nombre)
    print("Descripción: ", direccion)
    print("check: ", check)

    home_usuario = os.path.expanduser("~") #home usuario
    nombre_archivo = uuid.uuid4() #Nombre de formato hexadecimal
    extension_foto = os.path.splitext(foto.filename)[1]
    ruta_imagen= f'{home_usuario}\\fotos-usuarios\\{nombre_archivo}{extension_foto}'
    ruta_imagen_VIP=f'{home_usuario}\\fotos-usuarios-VIP\\{nombre_archivo}{extension_foto}'
    #if para saber si es VIP
    if check:
        print("Guardando la foto en", ruta_imagen_VIP)
        with open(ruta_imagen_VIP, "wb") as imagen:
            contenido = await foto.read()
            imagen.write(contenido)
    else:
        print("Guardando la foto en", ruta_imagen)
        with open(ruta_imagen, "wb") as imagen:
            contenido = await foto.read()
            imagen.write(contenido)

    respuesta = {
        "Nombre": nombre,
        "Direccion": direccion,
        "Ruta":ruta_imagen if not check else ruta_imagen_VIP,
    }
    return respuesta

