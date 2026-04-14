import datetime
import time
import ast
import operator
import logging
import json
import os
import re
import uuid
import subprocess
import selectors
from typing import Optional
from paser.infrastructure.gemini_adapter import GeminiAdapter
from .core_tools import context, ToolError
from .validation import validate_args
from .schemas import ValidateJsonSchema, ValidateJsonFileSchema

logger = logging.getLogger("tools")

def retry_request(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        backoff_factor = 1
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == max_retries - 1:
                    raise e
                sleep_time = backoff_factor * (2 ** i)
                logger.warning(f"Error in {func.__name__}, retrying in {sleep_time} seconds. Attempt {i+1}/{max_retries}. Error: {e}")
                time.sleep(sleep_time)
    return wrapper

def get_utc_time() -> str:
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return f"La hora actual (UTC) es: {now_utc.strftime('%H:%M:%S')}"

def get_cwd() -> str:
    import os
    return os.getcwd()

@validate_args(ValidateJsonSchema)
def validate_json(json_string: str) -> str:
    """Validates if a string is a valid JSON."""
    try:
        json.loads(json_string)
        return "✅ El JSON es válido."
    except json.JSONDecodeError as e:
        raise ToolError(f"JSON inválido: {str(e)}")

@validate_args(ValidateJsonFileSchema)
def validate_json_file(path: str) -> str:
    """Validates if a file contains valid JSON."""
    try:
        safe_path = context.get_safe_path(path)
        with open(safe_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return validate_json(json_string=content)
    except Exception as e:
        raise ToolError(f"Error al leer el archivo: {str(e)}")

def query_ai(prompt: str, temperature: float = 0.9, model: str = None, context_str: str = None) -> str:
    """
    Queries another AI instance for a second opinion, alternative perspectives, or to break reasoning loops.
    By default, it uses the same model as the agent but with a high temperature (0.9) for 'out-of-the-box' thinking.
    """
    try:
        adapter = GeminiAdapter()
        
        # Determine model to use
        if not model:
            # Try to get the current model from the system config
            try:
                config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
                with open(config_path, 'r') as f:
                    config = json.load(f)
                model = config.get("model_name")
            except Exception as e:
                logger.warning(f"Could not read config for model_name: {e}")

            # Fallback if config read failed or model_name is missing
            if not model:
                try:
                    available = adapter.get_available_models()
                    model = next((m for m in available if 'pro' in m.lower()), available[0])
                except Exception:
                    model = "models/gemini-1.5-flash"

        # Construct the prompt with context if provided
        full_prompt = prompt
        if context_str:
            full_prompt = f"Context:\n{context_str}\n\nQuestion: {prompt}"

        # System instruction for the reflection agent
        system_instruction = (
            "You are a specialized AI consultant providing a second opinion. "
            "Your goal is to be critical, identify blind spots, and offer alternative "
            "perspectives or 'out-of-the-box' solutions. Be concise and direct."
        )

        adapter.start_chat(model, system_instruction, temperature)
        response = adapter.send_message(full_prompt)
        
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        logger.error(f"Error in query_ai: {e}")
        raise ToolError(f"Error querying AI: {str(e)}")

class PaserMiniProcessManager:
    """Manages multiple independent processes of the paser-mini executable."""
    def __init__(self):
        self.processes: dict[str, subprocess.Popen] = {}
        self.process_cwd: dict[str, str] = {}
        self.executable_path = os.path.expanduser("~/.config/bin/paser-mini")

    def get_process(self, agent_id: str) -> subprocess.Popen:
        current_cwd = os.getcwd()
        
        # If process exists but CWD has changed, restart it to sync directory
        if agent_id in self.processes:
            if self.process_cwd.get(agent_id) != current_cwd:
                logger.info(f"CWD changed for agent {agent_id}. Restarting process to sync directory.")
                self.terminate_agent(agent_id)

        if agent_id not in self.processes:
            try:
                # Start paser-mini as a subprocess in the current working directory
                process = subprocess.Popen(
                    [self.executable_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1, # Line buffered
                    universal_newlines=True,
                    cwd=current_cwd
                )
                self.processes[agent_id] = process
                self.process_cwd[agent_id] = current_cwd
                
                # Initial wait for the prompt to ensure it's ready
                self._wait_for_prompt(process)
            except Exception as e:
                raise ToolError(f"Failed to start paser-mini process: {e}")
        return self.processes[agent_id]

    def _wait_for_prompt(self, process: subprocess.Popen, timeout: int = 30) -> str:
        """Reads stdout until the '> ' prompt is encountered."""
        output = []
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Paser-mini process timed out waiting for prompt '> '")
            
            char = process.stdout.read(1)
            if not char:
                break
            output.append(char)
            
            # Check if the last characters are the prompt '> '
            if "".join(output[-2:]) == "> ":
                break
        
        return "".join(output)

    def terminate_agent(self, agent_id: str):
        if agent_id in self.processes:
            self.processes[agent_id].terminate()
            if agent_id in self.process_cwd:
                del self.process_cwd[agent_id]
            del self.processes[agent_id]

# Global manager instance
mini_process_manager = PaserMiniProcessManager()

def chat_with_paser_mini(prompt: str, agent_id: str = None, context_str: str = None) -> str:
    """
    Interacts with a persistent paser-mini executable instance.
    Each agent_id corresponds to a separate OS process.
    """
    if agent_id is None:
        agent_id = str(uuid.uuid4())[:8]
    
    try:
        process = mini_process_manager.get_process(agent_id)
        
        # Prepare the message
        message = prompt
        if context_str:
            message = f"Context:\n{context_str}\n\nTask: {prompt}"
        
        # Send message to the process
        process.stdin.write(message + "\n")
        process.stdin.flush()
        
        # Read response until the prompt '> ' appears
        # We use a timeout to prevent the main agent from hanging
        response_text = mini_process_manager._wait_for_prompt(process, timeout=60)
        
        # Clean up the response (remove the trailing prompt)
        if response_text.endswith("> "):
            response_text = response_text[:-2]
            
        return f"[Agent: {agent_id}] {response_text.strip()}"
        
    except TimeoutError:
        # If it hangs, we terminate the process to clean up and allow a restart
        mini_process_manager.terminate_agent(agent_id)
        raise ToolError(f"Agent {agent_id} hung and was terminated. Please try again with a new session.")
    except Exception as e:
        logger.error(f"Error in chat_with_paser_mini: {e}")
        raise ToolError(f"Error interacting with paser-mini process: {str(e)}")
