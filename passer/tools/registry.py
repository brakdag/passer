from passer.tools import tools_functions as tf

AVAILABLE_TOOLS = {
    "obtener_hora_actual": tf.obtener_hora_actual,
    "calculadora_basica": tf.calculadora_basica,
    "leer_archivo": tf.leer_archivo,
    "escribir_archivo": tf.escribir_archivo,
    "borrar_archivo": tf.borrar_archivo,
    "listar_archivos": tf.listar_archivos,
    "buscar_en_internet": tf.buscar_en_internet,
    "leer_url": tf.leer_url
}

TOOL_CATALOG = """
[
    {"name": "obtener_hora_actual", "description": "Obtiene la hora actual.", "parameters": {"type": "object", "properties": {"zona_horaria": {"type": "string"}}, "required": ["zona_horaria"]}},
    {"name": "calculadora_basica", "description": "Evalúa operación matemática.", "parameters": {"type": "object", "properties": {"operacion": {"type": "string"}}, "required": ["operacion"]}},
    {"name": "leer_archivo", "description": "Lee archivo.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "escribir_archivo", "description": "Escribe archivo.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "contenido": {"type": "string"}}, "required": ["path", "contenido"]}},
    {"name": "borrar_archivo", "description": "Borra archivo.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "listar_archivos", "description": "Lista archivos.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "buscar_en_internet", "description": "Busca en internet.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "leer_url", "description": "Lee URL.", "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}
]
"""

SYSTEM_INSTRUCTION = f"""
Eres un agente autónomo.
Catálogo: {TOOL_CATALOG}

Regla ESTRICTA:
Todas las llamadas a herramientas deben seguir este formato JSON exacto:
<TOOL_CALL>{{"name": "nombre_herramienta", "args": {{"nombre_parametro": "valor"}}}}</TOOL_CALL>

No resumas NADA hasta que hayas terminado de usar TODAS las herramientas necesarias. Si necesitas hacer varias tareas, ejecuta una, espera <TOOL_RESPONSE>, y ejecuta la siguiente.
"""
