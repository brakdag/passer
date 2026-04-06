import subprocess
import os
import logging
from .core_tools import context

logger = logging.getLogger("tools")

def analyze_pyright(path: str = ".") -> str:
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

def notificar_usuario(mensaje: str = "") -> str:
    """Envía una notificación sonora al usuario usando el archivo assets/type.wav."""
    import platform
    import subprocess
    import os

    logger.info(f"Notificación: {mensaje}")

    try:
        system = platform.system()
        # Construir ruta absoluta al archivo assets/type.wav relativo al paquete Paser
        # system_tools.py está en paser/tools/, assets/ está en la raíz del proyecto (hermana de paser/)
        current_file = os.path.abspath(__file__)
        tools_dir = os.path.dirname(current_file)
        paser_dir = os.path.dirname(tools_dir)
        project_root = os.path.dirname(paser_dir)
        sound_path = os.path.join(project_root, "assets", "type.wav")

        if not os.path.exists(sound_path):
            print('\a')
            logger.warning(f"Archivo de sonido no encontrado: {sound_path}")
            return "OK"

        if system == "Linux":
            try:
                subprocess.run(["paplay", sound_path], check=True, capture_output=True)
            except:
                subprocess.run(["aplay", sound_path], check=True, capture_output=True)
        elif system == "Darwin":
            subprocess.run(["afplay", sound_path], check=True, capture_output=True)
        elif system == "Windows":
            import winsound
            winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        else:
            print('\a')

        return "OK"
    except Exception as e:
        logger.error(f"Error al intentar notificar: {e}")
        return "Error"
