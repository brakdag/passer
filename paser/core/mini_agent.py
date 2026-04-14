import os
import logging
import uuid
import json
from typing import Optional, Dict, Any
from paser.infrastructure.gemini_adapter import GeminiAdapter
from paser.core.executor import AutonomousExecutor


logger = logging.getLogger(__name__)

class Citizen:
    """Represents a single autonomous citizen with its own state and role."""
    def __init__(self, citizen_id: str, role_instruction: str):
        from paser.tools.registry import AVAILABLE_TOOLS, SYSTEM_INSTRUCTION
        self.citizen_id = citizen_id
        self.adapter = GeminiAdapter()
        
        # Get the orchestrator's model from config
        self.model = self._get_orchestrator_model()
        
        # RE-STRUCTURED IDENTITY: Agency first, then Specialization, then Protocol
        # This prevents the agent from becoming a passive chatbot
        agency_core = (
            "You are an AUTONOMOUS AGENT. You do not just chat; you ACT using tools.\n"
            "STRICT RULE: Never ask the user to provide the content of a file or directory. "
            "You have the tools to read them yourself. If you need information from a file, "
            "use the appropriate tool immediately."
        )
        
        combined_instruction = (
            f"{agency_core}\n\n"
            f"YOUR SPECIALIZATION:\n{role_instruction}\n\n"
            f"TECHNICAL PROTOCOL:\n{SYSTEM_INSTRUCTION}"
        )
        
        # Initialize the chat with the combined identity
        self.adapter.start_chat(self.model, combined_instruction, temperature=0.7)
        
        # Create a dedicated executor for this citizen
        # We use a limited max_turns to prevent hanging
        self.executor = AutonomousExecutor(
            assistant=self.adapter,
            tools=AVAILABLE_TOOLS,
            max_turns=10
        )

    def _get_orchestrator_model(self) -> str:
        """Reads the model name configured for the main orchestrator."""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get("model_name", "models/gemini-1.5-pro")
        except Exception as e:
            logger.error(f"Could not read orchestrator config for model: {e}")
            return "models/gemini-1.5-pro"

    async def execute_task(self, prompt: str, context_str: Optional[str] = None) -> str:
        full_prompt = prompt
        if context_str:
            full_prompt = f"Context:\n{context_str}\n\nTask: {prompt}"
        
        # The executor handles the ReAct loop (thought -> tool -> response)
        return await self.executor.execute(full_prompt, thinking_enabled=False)

class MiniAgentManager:
    """Orchestrates the lifecycle and roles of the citizens."""
    def __init__(self, staff_dir: str = "staff"):
        self.staff_dir = staff_dir
        self.citizens: Dict[str, Citizen] = {}

    def _load_role(self, role_name: Optional[str]) -> str:
        """Loads the system instruction from the staff directory."""
        if not role_name:
            role_name = "generalist"
        
        role_path = os.path.join(self.staff_dir, f"{role_name}.md")
        try:
            with open(role_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Role {role_name} not found in {self.staff_dir}. Falling back to generalist.")
            try:
                with open(os.path.join(self.staff_dir, "generalist.md"), 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                return "You are a helpful autonomous assistant."

    def get_citizen(self, citizen_id: Optional[str], role: Optional[str] = None) -> Citizen:
        if citizen_id is None:
            citizen_id = str(uuid.uuid4())[:8]
        
        if citizen_id not in self.citizens:
            role_instruction = self._load_role(role)
            self.citizens[citizen_id] = Citizen(citizen_id, role_instruction)
            
        return self.citizens[citizen_id]

    def terminate_citizen(self, citizen_id: str):
        if citizen_id in self.citizens:
            del self.citizens[citizen_id]

# Global manager instance
manager = MiniAgentManager()