import argparse
from paser.infrastructure.gemini_adapter import GeminiAdapter
from paser.core.chat_manager import ChatManager
from paser.tools.registry import AVAILABLE_TOOLS, SYSTEM_INSTRUCTION

def main():
    parser = argparse.ArgumentParser(description="Paser: Agente autónomo con ReAct Pattern")
    parser.add_argument("--version", action="version", version="paser 0.1.0")
    
    # Parseamos los argumentos, pero dejamos que la ejecución principal continúe
    args = parser.parse_args()

    assistant = GeminiAdapter()
    chat_manager = ChatManager(assistant, AVAILABLE_TOOLS, SYSTEM_INSTRUCTION)
    chat_manager.run()

if __name__ == "__main__":
    main()
