import os
import subprocess
import time
import re
from datetime import datetime
from paser.core.ui import console, print_panel, SpinnerContext, print_model_response, get_input

async def cmd_close_issue(handler, input_stripped):
    parts = input_stripped.split()
    if len(parts) < 3: 
        console.print('Uso: /close_issue [repo] [issue_number]', style='red')
    else:
        try:
            from paser.tools.github_tools import close_issue
            console.print(close_issue(parts[1], int(parts[2])), style='green')
        except Exception as e: 
            console.print(f'Error: {e}', style='red')
    return True

async def cmd_repeat(handler, input_stripped):
    parts = input_stripped.split(maxsplit=2)
    if len(parts) < 3: 
        console.print('Uso: /repeat [minutos] [mensaje]', style='red')
    else:
        try:
            handler.chat_manager.recurring_tasks[int(parts[1])] = {'msg': parts[2], 'last_run': time.time()}
            console.print(f'Gallina configurada: "{parts[2]}" cada {parts[1]} minutos.', style='green')
        except ValueError: 
            console.print('El tiempo debe ser un número entero.', style='red')
    return True

async def cmd_stop_repeat(handler, input_stripped):
    handler.chat_manager.recurring_tasks = {}
    console.print('Gallina detenida. Ya no picoteará más.', style='yellow')
    return True

async def cmd_snapshot(handler, input_stripped):
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'snapshot_{timestamp}.png'
        assets_dir = 'assets'
        os.makedirs(assets_dir, exist_ok=True)
        filepath = os.path.join(assets_dir, filename)
        captured = False
        for tool in ['scrot', 'maim']:
            try:
                cmd = [tool, '-o', filepath] if tool == 'scrot' else [tool, filepath]
                subprocess.run(cmd, check=True, capture_output=True)
                captured = True
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        if not captured:
            console.print('[bold red]Error:[/bold red] No se encontró "scrot" ni "maim" instalados en el sistema.', style='red')
            console.print('Instálalos con: [bold]sudo apt install scrot maim[/bold]', style='dim')
            return True
        print_panel('Captura realizada', f'Archivo guardado en: {filepath}', style='green')
        notification = f'He realizado una captura de pantalla del sistema: {filepath}. Por favor, analízala y dime qué ves.'
        with SpinnerContext('Analizando captura...', 'magenta', newline=True):
            result = await handler.chat_manager.executor.execute(
                user_input=notification, 
                thinking_enabled=handler.chat_manager.thinking_enabled, 
                get_confirmation_callback=get_input
            )
            if result:
                print_model_response(re.sub(r'<[^>]+>.*?</[^>]+>', '', result, flags=re.DOTALL))
        return True
    except Exception as e:
        console.print(f'[bold red]Error crítico en /snapshot:[/bold red] {e}', style='red')
        return True
