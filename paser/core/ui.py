"""
paser/core/ui.py
Interfaz de consola con Rich y prompt_toolkit con soporte para modos Vim.
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.box import ROUNDED
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from contextlib import contextmanager
import threading
import time

console = Console()

# --- Vim Mode State Management ---

class UIState:
    INSERT = "INSERT"
    NORMAL = "NORMAL"
    
    def __init__(self):
        self.mode = self.INSERT
        self.scroll_offset = 0

ui_state = UIState()

# Global session to maintain state and bindings
_session = None

def get_session(history=None):
    global _session
    if _session is None:
        _session = PromptSession(history=history)
    return _session

# Key Bindings for Vim-like navigation
kb = KeyBindings()

@kb.add('escape')
def _(event):
    ui_state.mode = UIState.NORMAL

@kb.add('i')
def _(event):
    if ui_state.mode == UIState.NORMAL:
        ui_state.mode = UIState.INSERT
    else:
        event.current_buffer.insert_text('i')

@kb.add('j')
def _(event):
    if ui_state.mode == UIState.NORMAL:
        # Send ANSI escape sequence for Cursor Down / Scroll Down
        sys.stdout.write('\x1b[B')
        sys.stdout.flush()
    else:
        event.current_buffer.insert_text('j')

@kb.add('k')
def _(event):
    if ui_state.mode == UIState.NORMAL:
        # Send ANSI escape sequence for Cursor Up / Scroll Up
        sys.stdout.write('\x1b[A')
        sys.stdout.flush()
    else:
        event.current_buffer.insert_text('k')

def get_bottom_toolbar():
    """Returns the status bar based on the current UI mode."""
    if ui_state.mode == UIState.NORMAL:
        return HTML('<ansiyellow> <b>— NORMAL —</b> </ansiyellow> (j/k: scroll, i: insert)')
    return HTML('<ansigreen> <b>— INSERT —</b> </ansigreen> (Esc: normal)')

# --- UI Helpers ---

def print_panel(title: str, message: str, box_type=ROUNDED, style: str = "none"):
    console.print(Panel(message, title=title, expand=False, box=box_type, border_style=style))

def print_error(message: str):
    console.print(Panel(message, title="󰅚 Error", border_style="red"))

def print_info(message: str):
    console.print(Panel(message, title="󰋽 Info", border_style="blue"))

def print_model_response(text: str):
    try:
        md = Markdown(text)
        console.print(md)
    except Exception:
        console.print(Text(text, style="cyan"))
    console.print()

def print_tool_call(tool_name: str, args: dict):
    console.print(
        Panel(
            f"```json\n{{\"name\": \"{tool_name}\", \"args\": {args}}}\n```",
            title="󰒓 Tool Call",
            border_style="magenta",
            expand=False,
        )
    )

def print_tool_result(tool_name: str, result: str):
    console.print(
        Panel(result[:200] if len(result) > 200 else result,
              title=f"󰄵 {tool_name}",
              border_style="green",
              expand=False)
    )

async def async_get_confirmation(message: str) -> bool:
    """Asynchronous confirmation prompt for security-sensitive tools."""
    response = await get_input(f"{message} (y/n): ")
    return response.lower().strip() == 'y'

async def get_input(prompt_text: str, history=None) -> str:
    style = Style.from_dict({
        '': '#00FF00',
        'prompt': '#00FF00 bold',
    })
    
    session = get_session(history=history)
    
    # We use prompt_async with our custom key bindings and bottom toolbar
    return await session.prompt_async(
        prompt_text, 
        style=style, 
        key_bindings=kb, 
        bottom_toolbar=get_bottom_toolbar
    )

@contextmanager
def SpinnerContext(message: str = "", color: str = "cyan", newline: bool = False):
    """
    Muestra un spinner profesional usando rich.console.status.
    Sincroniza el modo de la UI a NORMAL y restaura el modo previo al finalizar.
    """
    # Guardamos el modo actual para restaurarlo después
    previous_mode = ui_state.mode
    ui_state.mode = UIState.NORMAL
    
    if newline:
        console.print()
        
    # Construimos el mensaje para que parezca parte de la barra inferior
    # \u2014 es el em-dash usado en get_bottom_toolbar
    status_msg = f"[bold yellow]\u2014 NORMAL \u2014[/bold yellow] [{color}]{message}[/{color}]"
    
    try:
        with console.status(status_msg, spinner="material"):
            yield
    finally:
        # Restauramos el modo original DESPUÉS de que el contexto de rich haya cerrado
        # Esto evita que prompt_toolkit se confunda con el estado del terminal
        ui_state.mode = previous_mode
