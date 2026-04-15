from rich.table import Table
from paser.core.ui import console, LATEX_TO_UNICODE

async def cmd_history(handler, input_stripped):
    table = Table(title='Historial de Herramientas')
    table.add_column('Herramienta', style='cyan')
    table.add_column('Status', style='green')
    for entry in handler.history:
        table.add_row(entry['name'], entry['status'])
    console.print(table)
    return True

async def cmd_latex(handler, input_stripped):
    table = Table(title='Símbolos LaTeX Soportados', show_lines=True)
    table.add_column('LaTeX', style='cyan')
    table.add_column('Unicode', style='green')
    for latex, unicode_char in sorted(LATEX_TO_UNICODE.items()):
        table.add_row(latex, unicode_char)
    console.print(table)
    return True

async def cmd_help(handler, input_stripped, docs):
    table = Table(title='Comandos Disponibles')
    table.add_column('Comando', style='cyan')
    table.add_column('Descripción', style='green')
    for cmd in sorted(docs.keys()):
        table.add_row(cmd, docs[cmd])
    console.print(table)
    return True

async def cmd_clear(handler, input_stripped):
    console.clear()
    return True

async def cmd_tokens(handler, input_stripped):
    try:
        history = handler.chat_manager.assistant.get_chat_history()
        if history: 
            console.print(f'[bold cyan]💫 Contexto actual:[/bold cyan] {handler.chat_manager.assistant.count_tokens(history)} tokens', style='yellow')
        else: 
            console.print('No hay una sesión de chat activa.', style='red')
    except Exception as e: 
        console.print(f'Error estimando tokens: {e}', style='red')
    return True

async def cmd_quota(handler, input_stripped):
    try:
        model = handler.chat_manager.executor.assistant.current_model
        count = handler.chat_manager.executor.quota_tracker.get_current_count(model)
        limit = handler.chat_manager.executor.quota_tracker.get_limit(model)
        if limit > 0:
            usage_str = f'{count} / {limit}'
            percent = (count / limit) * 100
            status = f' ({percent:.1f}%)'
        else:
            usage_str = f'{count} (sin límite conocido)'
            status = ''
        console.print(f'[bold cyan]💫 Consumo de API hoy ({model}):[/bold cyan] {usage_str}{status}', style='yellow')
    except Exception as e: 
        console.print(f'Error consultando cuota: {e}', style='red')
    return True
