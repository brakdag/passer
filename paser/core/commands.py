import os
from paser.core.ui import console
from paser.core.commands_session import cmd_save, cmd_session, cmd_rm_session, cmd_new
from paser.core.commands_system import cmd_cd, cmd_thinking, cmd_models, cmd_max_turns, cmd_save_langchain
from paser.core.commands_utils import cmd_history, cmd_latex, cmd_help, cmd_clear, cmd_tokens, cmd_quota
from paser.core.commands_special import cmd_close_issue, cmd_repeat, cmd_stop_repeat, cmd_snapshot

COMMAND_DOCS = {
    "/cd": "Cambiar el directorio de trabajo.",
    "/history": "Mostrar el historial de herramientas.",
    "/latex": "Mostrar símbolos LaTeX soportados.",
    "/clear": "Limpiar la terminal.",
    "/save": "Guardar la sesión actual.",
    "/session": "Listar y cargar sesiones.",
    "/rm": "Eliminar una sesión.",
    "/thinking": "Alternar modo de pensamiento.",
    "/new": "Resumir, guardar snapshot y reiniciar.",
    "/models": "Cambiar modelo y temperatura.",
    "/max_turns": "Ajustar límite de turnos.",
    "/repeat": "Configurar una tarea recurrente.",
    "/stop_repeat": "Detener tareas recurrentes.",
    "/t": "Ver tokens del contexto.",
    "/quota": "Ver consumo de la API.",
    "/close_issue": "Cerrar un issue de GitHub.",
    "/save_langchain": "Alternar guardado de LangChain.",
    "/snapshot": "Capturar y analizar pantalla.",
    "/help": "Mostrar esta ayuda."
}

COMMAND_MAP = {
    "/cd": cmd_cd,
    "/history": cmd_history,
    "/latex": cmd_latex,
    "/clear": cmd_clear,
    "/cls": cmd_clear,
    "/save": cmd_save,
    "/s": cmd_save,
    "/session": cmd_session,
    "/ls": cmd_session,
    "/rm": cmd_rm_session,
    "/rm_session": cmd_rm_session,
    "/thinking": cmd_thinking,
    "/new": cmd_new,
    "/n": cmd_new,
    "/models": cmd_models,
    "/max_turns": cmd_max_turns,
    "/repeat": cmd_repeat,
    "/stop_repeat": cmd_stop_repeat,
    "/t": cmd_tokens,
    "/quota": cmd_quota,
    "/close_issue": cmd_close_issue,
    "/save_langchain": cmd_save_langchain,
    "/snapshot": cmd_snapshot,
    "/help": cmd_help
}

class CommandHandler:
    def __init__(self, chat_manager):
        self.chat_manager = chat_manager
        self.history = []

    def log_tool(self, name, status):
        self.history.append({"name": name, "status": status})

    async def handle(self, user_input):
        input_stripped = user_input.strip()
        
        if input_stripped.lower() in (':q', '/q', '/quit', '/exit'):
            self.chat_manager.should_exit = True
            return True

        if input_stripped.startswith('/') or input_stripped.startswith(':'):
            cmd_part = input_stripped.split()[0]
            if cmd_part in COMMAND_MAP:
                func = COMMAND_MAP[cmd_part]
                # El comando /help necesita los docs
                if cmd_part == '/help':
                    return await func(self, input_stripped, COMMAND_DOCS)
                return await func(self, input_stripped)
            else:
                console.print("Comando no válido", style="red")
                return True

        return False
