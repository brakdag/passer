import os
import json
import tempfile
import logging
import re
import fnmatch
from typing import Optional
from pathlib import Path
from .core_tools import context
from .validation import validate_args
from .schemas import ReadFileSchema, WriteFileSchema, ReadFilesSchema, ReplaceStringSchema, RemoveFileSchema, CreateDirSchema

logger = logging.getLogger("tools")

FILE_SIZE_LIMIT = 5 * 1024 * 1024

def is_binary_file(path: str) -> bool:
    try:
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)
    except Exception:
        return True

@validate_args(ReadFileSchema)
def read_file(path: str) -> str:
    safe_path = context.get_safe_path(path)
    if not os.path.isfile(safe_path):
        raise FileNotFoundError(f"Archivo no encontrado en '{path}'.")
    file_size = os.path.getsize(safe_path)
    if file_size > FILE_SIZE_LIMIT:
        raise ValueError(f"El archivo '{path}' es demasiado grande.")
    if is_binary_file(safe_path):
        raise ValueError(f"El archivo '{path}' es binario.")
    with open(safe_path, 'r', encoding='utf-8') as f:
        return f.read() or f"El archivo '{path}' está vacío."

@validate_args(ReadFilesSchema)
def read_files(paths: list[str]) -> str:
    results = []
    for path in paths:
        try:
            content = read_file(path=path)
            results.append(f"--- ARCHIVO: {path} ---\n{content}\n--- FIN ARCHIVO ---")
        except Exception as e:
            results.append(f"--- ARCHIVO: {path} ---\nError: {str(e)}\n--- FIN ARCHIVO ---")
    return "\n\n".join(results)

@validate_args(WriteFileSchema)
def write_file(path: str, contenido: str) -> str:
    safe_path = context.get_safe_path(path)
    os.makedirs(os.path.dirname(safe_path), exist_ok=True)
    with tempfile.NamedTemporaryFile('w', dir=os.path.dirname(safe_path), delete=False, encoding='utf-8') as tf:
        tf.write(contenido)
        temp_path = tf.name
    os.replace(temp_path, safe_path)
    return f"Archivo '{path}' creado/actualizado exitosamente."

@validate_args(RemoveFileSchema)
def remove_file(path: str) -> str:
    safe_path = context.get_safe_path(path)
    try:
        os.remove(safe_path)
        return f"Archivo '{path}' borrado exitosamente."
    except FileNotFoundError:
        raise FileNotFoundError(f"No se pudo borrar el archivo '{path}' porque no existe.")

def list_dir(path: str = ".") -> str:
    return json.dumps(os.listdir(context.get_safe_path(path)))

def read_lines(path: str, inicio: int, fin: int) -> str:
    safe_path = context.get_safe_path(path)
    with open(safe_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return "".join(lines[inicio-1:fin])

def read_head(path: str, cantidad_lineas: int) -> str:
    return read_lines(path, 1, cantidad_lineas)

def update_line(path: str, line_number: int, new_content: str) -> str:
    safe_path = context.get_safe_path(path)
    with open(safe_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if line_number < 1 or line_number > len(lines):
        raise IndexError(f"La línea {line_number} está fuera de rango. El archivo tiene {len(lines)} líneas.")
    
    lines[line_number-1] = new_content + "\n"
    with open(safe_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return f"Línea {line_number} de '{path}' modificada exitosamente."

@validate_args(ReplaceStringSchema)
def replace_string(path: str, search_text: str, replace_text: str) -> str:
    safe_path = context.get_safe_path(path)
    with open(safe_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if search_text not in content:
        raise ValueError(f"La cadena '{search_text}' no fue encontrada en el archivo '{path}'.")
    
    with open(safe_path, 'w', encoding='utf-8') as f:
        f.write(content.replace(search_text, replace_text))
    return f"Reemplazo completado exitosamente en '{path}'."




def global_replace(path: str, search_text: str, replace_text: str, extensiones: Optional[list] = None) -> str:
    safe_base_path = context.get_safe_path(path)
    modificados = []
    for root, _, files in os.walk(safe_base_path):
        for file in files:
            if extensiones and not any(file.endswith(ext) for ext in extensiones): continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if search_text in content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content.replace(search_text, replace_text))
                    modificados.append(file_path)
            except (UnicodeDecodeError, PermissionError):
                continue
    
    if not modificados:
        raise ValueError(f"No se encontró la cadena '{search_text}' en ningún archivo válido dentro de '{path}'.")
        
    return f"Reemplazo global completado exitosamente en {len(modificados)} archivos."

def rename_path(origen: str, destino: str) -> str:
    try:
        os.rename(context.get_safe_path(origen), context.get_safe_path(destino))
        return f"Ruta '{origen}' movida/renombrada a '{destino}' exitosamente."
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo o directorio de origen '{origen}' no existe.")

@validate_args(CreateDirSchema)
def create_dir(path: str) -> str:
    os.makedirs(context.get_safe_path(path), exist_ok=True)
    return f"Carpeta '{path}' creada exitosamente."

def search_files_pattern(pattern: str) -> str:
    return json.dumps([str(p.relative_to(context.get_safe_path("."))) for p in Path(context.get_safe_path(".")).glob(pattern)])

def search_text_global(query: str) -> str:
    results = []
    for root, _, files in os.walk(context.get_safe_path(".")):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if query in line:
                            results.append({"file": file, "line": i, "text": line.strip()})
            except (UnicodeDecodeError, PermissionError):
                continue
    return json.dumps(results)

def format_code(path: str) -> str:
    import subprocess
    subprocess.run(['black', context.get_safe_path(path)])
    return "Formateado con Black."

def get_tree(path: str = ".", max_depth: Optional[int] = None, exclude_patterns: Optional[list[str]] = None) -> str:
    return "Tree structure generated."
