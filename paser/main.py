from paser.infrastructure.gemini_adapter import GeminiAdapter
from paser.core.chat_manager import ChatManager
from paser.tools.registry import AVAILABLE_TOOLS, SYSTEM_INSTRUCTION

def main():
    assistant = GeminiAdapter()
    chat_manager = ChatManager(assistant, AVAILABLE_TOOLS, SYSTEM_INSTRUCTION)
    chat_manager.run()

if __name__ == "__main__":
    main()
