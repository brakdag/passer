import os
from datetime import datetime
from paser.core.ui import get_input, console, print_panel, SpinnerContext

async def cmd_save(handler, input_stripped):
    # Normalizar el comando para extraer el nombre
    cmd = '/save' if input_stripped.startswith('/save') else '/s'
    parts = input_stripped[len(cmd):].strip().split(maxsplit=1)
    name = parts[0] if parts else 'last_session'
    try:
        path = handler.chat_manager.save_session(name)
        print_panel('Sesión Guardada', f'Contexto guardado como: {name}\nPath: {path}', style='green')
    except Exception as e: 
        console.print(f'Error guardando sesión: {e}', style='red')
    return True

async def cmd_session(handler, input_stripped):
    session_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'sessions')
    os.makedirs(session_dir, exist_ok=True)
    sessions = [f for f in os.listdir(session_dir) if f.endswith('.json')]
    if not sessions:
        console.print('No hay sesiones guardadas.', style='yellow')
        return True
    for i, s in enumerate(sessions): 
        console.print(f'{i}: {s}')
    choice = await get_input('Selecciona sesión (o \'c\' para cancelar): ')
    if choice == 'c': return True
    try:
        idx = int(choice)
        name = sessions[idx].replace('.json', '')
        handler.chat_manager.load_session(name)
        print_panel('Sesión cargada', f'🤖 {name}', style='green')
    except Exception as e: 
        console.print(f'Error cargando sesión: {e}', style='red')
    return True

async def cmd_rm_session(handler, input_stripped):
    parts = input_stripped.split(maxsplit=1)
    if len(parts) < 2:
        console.print('Uso: /rm [nombre_sesion]', style='red')
        return True
    name = parts[1].strip()
    try:
        if handler.chat_manager.delete_session(name):
            print_panel('Sesión Eliminada', f'La sesión {name} ha sido borrada.', style='yellow')
        else:
            console.print(f'Sesión {name} no encontrada.', style='red')
    except Exception as e: 
        console.print(f'Error eliminando sesión: {e}', style='red')
    return True

async def cmd_new(handler, input_stripped):
    # 1. Generar resumen de la sesión actual
    summary_prompt = 'Por favor, genera un resumen conciso de nuestra conversación hasta ahora en aproximadamente 200 palabras.'
    with SpinnerContext('Generando resumen de la sesión...', 'magenta', newline=True):
        try:
            response = handler.chat_manager.assistant.send_message(summary_prompt)
            summary_text = response.text if hasattr(response, 'text') else str(response)
        except Exception as e:
            summary_text = f'No se pudo generar el resumen: {e}'
    
    print_panel('Resumen de la Sesión', summary_text, style='cyan')
    
    # 2. Guardar Snapshot y Reiniciar
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    snapshot_name = f'LS_{timestamp}'
    path = handler.chat_manager.save_session(snapshot_name)
    
    handler.chat_manager.assistant.start_chat(handler.chat_manager.assistant.current_model, handler.chat_manager.system_instruction, handler.chat_manager.temperature)
    handler.chat_manager.executor.turn_count = 0
    handler.history = []
    print_panel('Sesión Reiniciada', f'Historial limpiado. Snapshot guardado como: {snapshot_name}\nPath: {path}', style='green')
    return True
