from google import genai
from google.genai import types
import os
import re
import datetime
import math
import json
import urllib.request
import urllib.parse
import html2text

# Directorio base del proyecto
PROJECT_ROOT = os.getcwd()
TEMPERATURE = 0.7
THINKING_ENABLED = True

# Inicializar cliente
client = genai.Client()

def get_safe_path(path: str) -> str:
    """Resuelve la ruta de forma segura dentro del directorio del proyecto."""
    base = os.path.abspath(PROJECT_ROOT)
    target = os.path.abspath(os.path.join(base, path))
    if not target.startswith(base):
        raise ValueError("Acceso fuera del directorio permitido.")
    return target

def obtener_hora_actual(zona_horaria: str) -> str:
    """Devuelve la hora actual para una zona horaria específica."""
    try:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        return f"La hora actual en {zona_horaria} (simulado UTC) es: {now_utc.strftime('%H:%M:%S')}"
    except Exception as e:
        return f"Error al obtener la hora: {e}"

def calculadora_basica(operacion: str) -> str:
    """Evalúa una operación matemática simple (suma, resta, multiplicacion, division)."""
    try:
        result = eval(operacion) # nosec
        return f"El resultado de '{operacion}' es: {result}"
    except Exception as e:
        return f"Error al calcular '{operacion}': {e}"

def leer_archivo(path: str) -> str:
    """Lee el contenido de un archivo de texto en el directorio del proyecto."""
    try:
        safe_path = get_safe_path(path)
        if not os.path.isfile(safe_path):
            return f"Error: Archivo no encontrado en '{path}'."
        with open(safe_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer el archivo: {e}"

def escribir_archivo(path: str, contenido: str) -> str:
    """Crea o sobreescribe un archivo de texto en el directorio del proyecto."""
    try:
        safe_path = get_safe_path(path)
        with open(safe_path, 'w') as f:
            f.write(contenido)
        return f"Archivo '{path}' creado/actualizado exitosamente."
    except Exception as e:
        return f"Error al escribir el archivo: {e}"

def borrar_archivo(path: str) -> str:
    """Borra un archivo de texto en el directorio del proyecto."""
    try:
        safe_path = get_safe_path(path)
        if not os.path.isfile(safe_path):
            return f"Error: Archivo no encontrado en '{path}'."
        os.remove(safe_path)
        return f"Archivo '{path}' borrado exitosamente."
    except Exception as e:
        return f"Error al borrar el archivo: {e}"

def listar_archivos(path: str = ".") -> str:
    """Lista los archivos y directorios en una ruta dada dentro del proyecto."""
    try:
        safe_path = get_safe_path(path)
        if not os.path.isdir(safe_path):
            return f"Error: '{path}' no es un directorio válido."
        archivos = os.listdir(safe_path)
        return json.dumps(archivos)
    except Exception as e:
        return f"Error al listar archivos: {e}"

def buscar_en_internet(query: str) -> str:
    """Busca en internet usando DuckDuckGo."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        # Extract links and titles (robust regex)
        links = re.findall(r'<a[^>]*?href=\"([^\"]+)\"[^>]*?>(.*?)</a>', html, re.DOTALL)
        
        # Limpiar y extraer URLs reales
        results = []
        for link, title in links:
            if 'uddg=' in link:
                parsed = urllib.parse.urlparse(link)
                params = urllib.parse.parse_qs(parsed.query)
                if 'uddg' in params:
                    actual_link = params['uddg'][0]
                    clean_title = re.sub(r'<[^>]*?>', '', title).strip()
                    results.append({"title": clean_title, "link": actual_link})
            elif link.startswith('http'):
                clean_title = re.sub(r'<[^>]*?>', '', title).strip()
                results.append({"title": clean_title, "link": link})
        return json.dumps(results)
    except Exception as e:
        return f"Error: {e}"

def leer_url(url: str) -> str:
    """Lee el contenido textual de una página web a partir de una URL."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Uso de html2text para convertir HTML a Markdown limpio
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        text = h.handle(html)
        return text[:3000] # Limit size
    except Exception as e:
        return f"Error al leer la URL: {e}"

AVAILABLE_TOOLS = {
    "obtener_hora_actual": obtener_hora_actual,
    "calculadora_basica": calculadora_basica,
    "leer_archivo": leer_archivo,
    "escribir_archivo": escribir_archivo,
    "borrar_archivo": borrar_archivo,
    "listar_archivos": listar_archivos,
    "buscar_en_internet": buscar_en_internet,
    "leer_url": leer_url
}

TOOL_CATALOG = """
[
    {"name": "obtener_hora_actual", "description": "Obtiene la hora actual.", "parameters": {"type": "object", "properties": {"zona_horaria": {"type": "string"}}, "required": ["zona_horaria"]}},
    {"name": "calculadora_basica", "description": "Evalúa una operación matemática.", "parameters": {"type": "object", "properties": {"operacion": {"type": "string"}}, "required": ["operacion"]}},
    {"name": "leer_archivo", "description": "Lee archivo.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "escribir_archivo", "description": "Escribe archivo.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "contenido": {"type": "string"}}, "required": ["path", "contenido"]}},
    {"name": "borrar_archivo", "description": "Borra archivo.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "listar_archivos", "description": "Lista archivos.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "buscar_en_internet", "description": "Busca en internet.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "leer_url", "description": "Lee URL.", "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}
]
"""

SYSTEM_INSTRUCTION = f"""
Eres un agente autónomo con acceso a herramientas.
Catálogo: {TOOL_CATALOG}
Si necesitas razonar, comienza las líneas con '*'.
Si necesitas usar una herramienta, usa: <TOOL_CALL>{{"name": "...", "args": {{...}}}}</TOOL_CALL>
"""

def get_available_models():
    return [m.name for m in client.models.list() if 'generateContent' in m.supported_generation_methods]

def iniciar_chat():
    global THINKING_ENABLED, PROJECT_ROOT
    model_name = 'models/gemma-4-31b-it'
    
    chat = client.chats.create(model=model_name, config=types.GenerateContentConfig(temperature=TEMPERATURE))
    chat.send_message(SYSTEM_INSTRUCTION)
    
    print("--- Chat iniciado ---")
    while True:
        try:
            user_input = input("Tú: ")
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input: continue
        if user_input.strip() == ':q': break
        
        if user_input.strip().startswith('/cd '):
            new_dir = user_input.strip()[4:]
            if os.path.isdir(new_dir):
                PROJECT_ROOT = os.path.abspath(new_dir)
                print(f"Directorio: {PROJECT_ROOT}")
            continue
        elif user_input.strip() == '/thinking':
            THINKING_ENABLED = not THINKING_ENABLED
            print(f"Pensamientos: {'Visible' if THINKING_ENABLED else 'Oculto'}")
            continue
        elif user_input.strip() == '/models':
            models = get_available_models()
            for i, m in enumerate(models): print(f"{i}: {m}")
            choice = input("Modelo: ")
            try:
                idx = int(choice)
                model_name = models[idx]
                chat = client.chats.create(model=model_name, config=types.GenerateContentConfig(temperature=TEMPERATURE))
                chat.send_message(SYSTEM_INSTRUCTION)
            except: print("Error.")
            continue
        
        # Procesar (Autonomous Loop)
        current_input = user_input
        is_first_turn = True
        while True:
            try:
                response_generator = chat.send_message_stream(current_input)
                full_response_text = ""
                if is_first_turn:
                    print("Gemini: ", end="")
                    is_first_turn = False
                
                for chunk in response_generator:
                    if hasattr(chunk, 'text') and chunk.text:
                        full_response_text += chunk.text
                        for line in chunk.text.splitlines(keepends=True):
                            if THINKING_ENABLED or not line.lstrip().startswith('*'):
                                print(line, end="", flush=True)
                
                # TOOL_CALL
                start_tag, end_tag = "<TOOL_CALL>", "</TOOL_CALL>"
                s = full_response_text.find(start_tag)
                e = full_response_text.find(end_tag)
                tool_json = full_response_text[s+len(start_tag):e] if s != -1 and e != -1 else None
                
                if tool_json:
                    tool_call = json.loads(tool_json)
                    f_name = tool_call.get("name")
                    f_args = tool_call.get("args", {})
                    if f_name in AVAILABLE_TOOLS:
                        print(f"DEBUG: Ejecutando {f_name} con {f_args}")
                        if f_name == "borrar_archivo":
                            print(f"\n[Confirmación requerida] ¿Quieres borrar el archivo '{f_args.get('path')}'? (y/n)")
                            confirm = input("Confirmar (y/n): ")
                            res = AVAILABLE_TOOLS[f_name](**f_args) if confirm == 'y' else "Cancelado."
                        else:
                            res = AVAILABLE_TOOLS[f_name](**f_args)
                        
                        print(f"DEBUG: Resultado: {res}")
                        chat.send_message(f"<TOOL_RESPONSE>{json.dumps({'status': 'success', 'data': res})}</TOOL_RESPONSE>")
                        current_input = "" # Trigger next turn in loop
                        continue
                    else:
                        chat.send_message(f"<TOOL_RESPONSE>{json.dumps({'status': 'error', 'data': 'Tool not found'})}</TOOL_RESPONSE>")
                        break
                else:
                    print("") # Nueva línea al terminar el streaming final
                    break # No tool call, stop autonomous loop
            except Exception as e: 
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    iniciar_chat()
