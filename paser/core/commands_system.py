import os
import json
from paser.core.ui import get_input, console, print_panel
from paser.tools import core_tools

async def cmd_cd(handler, input_stripped):
    path = input_stripped[4:]
    try:
        core_tools.context.set_root(path)
        console.print(f'Directorio cambiado a: {core_tools.context.root}', style='green')
    except FileNotFoundError as e:
        console.print(str(e), style='red')
    return True

async def cmd_thinking(handler, input_stripped):
    handler.chat_manager.thinking_enabled = not handler.chat_manager.thinking_enabled
    console.print(f'Pensamientos: {"Visible" if handler.chat_manager.thinking_enabled else "Oculto"}', style='bold')
    return True

async def cmd_models(handler, input_stripped):
    models = handler.chat_manager.assistant.get_available_models()
    for i, m in enumerate(models): console.print(f'{i}: {m}')
    choice = await get_input('Modelo: ')
    try:
        idx = int(choice)
        model_name = models[idx]
        temp_input = await get_input(f'Temp (0-1, default {handler.chat_manager.temperature}): ')
        new_temp = float(temp_input or handler.chat_manager.temperature)
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
        try:
            with open(config_path, 'r') as f: config = json.load(f)
        except Exception: config = {}
        config['model_name'] = model_name
        config['default_temperature'] = new_temp
        with open(config_path, 'w') as f: json.dump(config, f, indent=4)
        handler.chat_manager.temperature = new_temp
        handler.chat_manager.assistant.start_chat(model_name, handler.chat_manager.system_instruction, new_temp)
        print_panel('Modelo cambiado', f'🤖 {model_name} | Temperatura: {new_temp}', style='green')
    except Exception as e: 
        console.print(f'Error: {e}', style='red')
    return True

async def cmd_max_turns(handler, input_stripped):
    parts = input_stripped.split()
    if len(parts) < 2: 
        console.print('Uso: /max_turns [número]', style='red')
    else:
        try:
            new_max = int(parts[1])
            if new_max <= 0: raise ValueError
            handler.chat_manager.executor.max_turns = new_max
            console.print(f'Límite de turnos actualizado a: {new_max}', style='green')
        except ValueError: 
            console.print('Por favor, proporciona un número entero positivo.', style='red')
    return True

async def cmd_save_langchain(handler, input_stripped):
    current_state = getattr(handler.chat_manager.assistant, 'save_langchain_enabled', False)
    new_state = not current_state
    if hasattr(handler.chat_manager.assistant, 'save_langchain_enabled'):
        handler.chat_manager.assistant.save_langchain_enabled = new_state
    handler.chat_manager.save_langchain_enabled = new_state
    handler.chat_manager.config_manager.set('save_langchain_enabled', new_state)
    status = 'Activado' if new_state else 'Desactivado'
    console.print(f'Guardado de LangChain: {status}', style='green')
    return True
