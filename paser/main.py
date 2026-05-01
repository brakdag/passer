import argparse
import asyncio
import unittest
import sys
import json
import os
from paser.infrastructure.gemini_adapter import GeminiAdapter
from paser.core.chat_manager import ChatManager
from paser.core.terminal_ui import TerminalUI
import os
from paser.tools.registry import AVAILABLE_TOOLS, SYSTEM_INSTRUCTION

async def main():
    parser = argparse.ArgumentParser(description="Paser: Agente autónomo con ReAct Pattern")
    parser.add_argument("--version", action="version", version="paser 0.1.0")
    parser.add_argument("--unit_tests", action="store_true", help="Ejecutar pruebas unitarias y generar reporte")
    parser.add_argument("-fsi", "--file-system-instructor", type=str, help="Carga un rol/instrucción desde un archivo Markdown")
    
    args = parser.parse_args()

    if args.unit_tests:
        print("--- Ejecutando suite de pruebas unitarias ---")
        suite = unittest.TestLoader().discover('tests', pattern='test_*.py')
        
        # Ejecutar pruebas y capturar resultados
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
        result = runner.run(suite)
        
        report = {
            "success": result.wasSuccessful(),
            "total": result.testsRun,
            "errors": len(result.errors),
            "failures": len(result.failures),
            "skipped": len(result.skipped)
        }
        
        with open("tests/test_results.json", "w") as f:
            json.dump(report, f, indent=4)
        
        print(f"\nReporte generado en tests/test_results.json")
        sys.exit(0 if result.wasSuccessful() else 1)

    # Preparar el System Instruction
    current_system_instruction = SYSTEM_INSTRUCTION
    if args.file_system_instructor:
        try:
            with open(args.file_system_instructor, "r", encoding="utf-8") as f:
                extra_instruction = f.read()
                current_system_instruction = f"{extra_instruction}\n\n{SYSTEM_INSTRUCTION}"
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el instructor desde el archivo: {e}")

    assistant = GeminiAdapter()
    ui = TerminalUI()
    chat_manager = ChatManager(assistant, AVAILABLE_TOOLS, current_system_instruction, ui)
    await chat_manager.run()

def cli():
    asyncio.run(main())

if __name__ == "__main__":
    cli()