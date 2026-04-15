import os
import logging
import uuid
import json
from typing import Optional, Dict, Any
from paser.infrastructure.gemini_adapter import GeminiAdapter
from paser.core.executor import AutonomousExecutor
from paser.tools.registry import AVAILABLE_TOOLS, SYSTEM_INSTRUCTION

logger = logging.getLogger(__name__)

class Citizen:
    def __init__(self, citizen_id: str, role_instruction: str):
        self.citizen_id = citizen_id
        self.adapter = GeminiAdapter()
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
            with open(config_path, 'r') as f:
                config = json.load(f)
                model = config.get("model_name", "models/gemini-1.5-pro")
        except Exception:
            model = "models/gemini-1.5-pro"
        self.model = model
        # FIX: Combine global SYSTEM_INSTRUCTION with role_instruction
        combined_instruction = f"{SYSTEM_INSTRUCTION}\n\n{role_instruction}"
        self.adapter.start_chat(self.model, combined_instruction, temperature=0.7)
        self.executor = AutonomousExecutor(
            assistant=self.adapter,
            tools=AVAILABLE_TOOLS,
            max_turns=10
        )

    async def execute_task(self, prompt: str, context_str: Optional[str] = None) -> str:
        full_prompt = prompt
        if context_str:
            full_prompt = f"Context:\n{context_str}\n\nTask: {prompt}"
        return await self.executor.execute(full_prompt, thinking_enabled=False)

class MiniAgentManager:
    def __init__(self, staff_dir: str = "staff"):
        self.staff_dir = staff_dir
        self.citizens: Dict[str, Citizen] = {}

    def _load_role(self, role_name: Optional[str]) -> str:
        if not role_name:
            role_name = "generalist"
        return f"Your role, identity, and specific instructions are defined in the file: staff/{role_name}.md. Read this file first to understand your goals and behavior."

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

manager = MiniAgentManager()