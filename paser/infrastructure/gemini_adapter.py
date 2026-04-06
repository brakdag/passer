from typing import Generator, Optional, Any
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from paser.core.interfaces import IAIAssistant

class GeminiAdapter(IAIAssistant):
    def __init__(self):
        self.client = genai.Client()
        self.chat: Any = None
        self._current_model: Optional[str] = None

    @property
    def current_model(self) -> Optional[str]:
        return self._current_model

    def start_chat(self, model_name: str, system_instruction: str, temperature: float):
        self._current_model = model_name
        
        # Validar el modelo antes de iniciar
        available_models = self.get_available_models()
        if model_name not in available_models:
            raise ValueError(f"Modelo no disponible: {model_name}. Use /models para ver los disponibles.")
        
        config_params = {"temperature": temperature}
        history = []
        
        if "gemma" in model_name.lower():
            # Gemma models often don't support system_instruction in the config
            # We simulate it by adding it to the chat history
            config_params["system_instruction"] = None
            history = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=f"System Instructions: {system_instruction}")]
                ),
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text="Understood. I will follow these instructions.")]
                ),
            ]
        else:
            config_params["system_instruction"] = system_instruction

        try:
            self.chat = self.client.chats.create(
                model=model_name,
                config=types.GenerateContentConfig(**config_params),
                history=history
            )
        except ClientError as e:
            raise RuntimeError(f"Error al iniciar chat con el modelo {model_name}: {e}")

    def send_message_stream(self, message: str) -> Generator[str, None, None]:
        if not self.chat:
            yield ""
            return
        try:
            response = self.chat.send_message_stream(message)
            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    yield chunk.text
        except ClientError as e:
            if getattr(e, 'status_code', None) == 429 or '429' in str(e):
                yield f"\n⚠️ Error: Cuota de API excedida (429). Por favor, espera un momento o cambia el modelo. {e}"
            else:
                raise e

    def send_message(self, message: str) -> Any:
        if not self.chat:
            return None
        try:
            return self.chat.send_message(message)
        except ClientError as e:
            if getattr(e, 'status_code', None) == 429 or '429' in str(e):
                # Retornamos un string que el AutonomousExecutor._extract_text pueda manejar
                return f"⚠️ Error: Cuota de API excedida (429). Por favor, espera un momento o cambia el modelo. {e}"
            raise e

    def get_available_models(self) -> list:
        # Relaxed filtering to ensure models appear
        models = self.client.models.list()
        return [m.name for m in models if m.name and ('gemini' in m.name.lower() or 'gemma' in m.name.lower())]
