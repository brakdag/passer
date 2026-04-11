from pydantic import BaseModel, Field
from typing import List, Optional

class ReadFileSchema(BaseModel):
    path: str = Field(..., description="Ruta del archivo a leer")

class WriteFileSchema(BaseModel):
    path: str = Field(..., description="Ruta del archivo a escribir")
    contenido: str = Field(..., description="Contenido a escribir en el archivo")

class ReadFilesSchema(BaseModel):
    paths: List[str] = Field(..., description="Lista de rutas de archivos a leer")

class ReplaceStringSchema(BaseModel):
    path: str = Field(..., description="Ruta del archivo")
    search_text: str = Field(..., description="Texto a buscar")
    replace_text: str = Field(..., description="Texto de reemplazo")

class ReplaceCodeBlockSchema(BaseModel):
    path: str = Field(..., description="Ruta del archivo")
    search_text: str = Field(..., description="Bloque de código a buscar")
    replace_text: str = Field(..., description="Bloque de código de reemplazo")

class RemoveFileSchema(BaseModel):
    path: str = Field(..., description="Ruta del archivo a borrar")

class CreateDirSchema(BaseModel):
    path: str = Field(..., description="Ruta del directorio a crear")
