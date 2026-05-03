import asyncio
import sys
import os

# Setup path
root_path = os.getcwd()
if root_path not in sys.path:
    sys.path.append(root_path)

from paser.infrastructure.gemini_adapter import GeminiAdapter
from paser.core.chat_manager import ChatManager
from paser.core.terminal_ui import TerminalUI
from paser.tools.registry import AVAILABLE_TOOLS, SYSTEM_INSTRUCTION

async def test_agent():
    print("--- Initializing Paser Agent ---")
    assistant = GeminiAdapter()
    ui = TerminalUI()
    chat_manager = ChatManager(assistant, AVAILABLE_TOOLS, SYSTEM_INSTRUCTION, ui)
    
    # Initialize the chat session
    chat_manager._initialize_chat()
    
    prompt = "Mueve el mouse a la esquina superior izquierda de la pantalla (por ejemplo, coordenadas 10, 10) y haz un clic para que el usuario pueda ver el movimiento."
    print(f"Asking agent: {prompt}")
    
    result = await chat_manager.executor.execute(
        user_input=prompt,
        thinking_enabled=True,
        get_confirmation_callback=lambda x: asyncio.Future()
    )
    
    print("\n--- Agent Response ---")
    print(result)

if __name__ == '__main__':
    asyncio.run(test_agent())