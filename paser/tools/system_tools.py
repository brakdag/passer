import subprocess
import os
import logging
from .core_tools import context

logger = logging.getLogger("tools")

def analizar_codigo_con_pyright(path: str = ".") -> str:
    """Analiza código usando pyright y devuelve errores si existen."""
    try:
        pyright_path = os.path.join(context.root, "venv", "bin", "pyright")
        if not os.path.exists(pyright_path):
            pyright_path = "pyright"
            
        safe_path = context.get_safe_path(path)
        result = subprocess.run([pyright_path, "--outputjson", safe_path], capture_output=True, text=True)
        if result.returncode == 0:
            return "No se encontraron errores de tipo."
        return result.stdout
    except Exception as e:
        logger.error(f"Error ejecutando pyright: {e}")
        return f"Error ejecutando pyright: {e}"
