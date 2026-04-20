import sys
import os

# Add aimouse to path to allow importing from its src
# We assume the project root is the current working directory
root_path = os.getcwd()
aimouse_path = os.path.join(root_path, 'aimouse')
if aimouse_path not in sys.path:
    sys.path.append(aimouse_path)

try:
    from src.inference.llm_interface import llm_interface
except ImportError:
    try:
        from aimouse.src.inference.llm_interface import llm_interface
    except ImportError as e:
        llm_interface = None

def neural_mouse_control(command: str):
    """
    Controls the mouse using a neural interface for organic movement.
    Input: 'rect(x, y, width, height);action'.
    Actions: 'click' or 'rect(0,0,0,0)' for a screenshot.
    Returns a color-coded image for spatial orientation.
    """
    if llm_interface is None:
        return {"status": "error", "message": "Neural Mouse Interface not initialized or found in path."}
    
    try:
        result = llm_interface.execute(command)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
