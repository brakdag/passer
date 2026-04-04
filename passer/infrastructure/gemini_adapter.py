from google import genai
from google.genai import types
from passer.core.interfaces import IAIAssistant
from typing import Generator

class GeminiAdapter(IAIAssistant):
    def __init__(self):
        self.client = genai.Client()
        self.chat = None

    def start_chat(self, model_name: str, system_instruction: str, temperature: float):
        self.chat = self.client.chats.create(
            model=model_name, 
            config=types.GenerateContentConfig(temperature=temperature)
        )
        self.chat.send_message(system_instruction)

    def send_message_stream(self, message: str) -> Generator[str, None, None]:
        response = self.chat.send_message_stream(message)
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                yield chunk.text

    def send_message(self, message: str):
        return self.chat.send_message(message)

    def get_available_models(self) -> list:
        return [m.name for m in self.client.models.list() if hasattr(m, 'supported_generation_methods') and 'generateContent' in m.supported_generation_methods]
