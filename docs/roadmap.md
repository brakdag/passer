# Hoja de Ruta - Proyecto Passer

Este documento describe la visión, los objetivos y la planificación estratégica del proyecto Passer.

## 1. Estado Actual
El proyecto Passer es un sistema autónomo de Function Calling basado en el patrón ReAct. Se han implementado las funcionalidades básicas de interacción con el modelo Gemini, un sistema de seguridad para el manejo de rutas (`get_safe_path`) y un conjunto de herramientas locales.

## 2. Objetivos a Corto Plazo
- **Verificación de Seguridad**: Realizar auditorías de código periódicas para confirmar que las mitigaciones de seguridad están operativas.
- **Ampliación de Pruebas**: Implementar tests unitarios y de integración para cubrir todos los casos de borde de las herramientas.
- **Optimización de Prompting**: Refinar la `system_instruction` para mejorar la precisión de las llamadas a herramientas y reducir alucinaciones.

## 3. Objetivos a Medio Plazo
- **Memoria Persistente**: Implementar un sistema de memoria a largo plazo (ej. base de datos SQLite o almacenamiento de vectores) para que el agente recuerde interacciones pasadas entre sesiones.
- **Nuevas Herramientas**:
    - Herramienta de ejecución de comandos de sistema controlada (sandbox).
    - Integración con APIs externas adicionales.
    - Herramienta de búsqueda avanzada en archivos (grep-like).
- **Interfaz de Usuario**: Mejorar la experiencia de consola o implementar una interfaz web básica.

## 4. Objetivos a Largo Plazo
- **Soporte Multi-Modelo**: Adaptar `gemini_adapter.py` para soportar otros LLMs (Claude, GPT-4) manteniendo la misma interfaz de herramientas.
- **Orquestación de Agentes**: Permitir que Passer pueda delegar tareas a otros agentes especializados.

## 5. Seguimiento
Para ver el estado actual de las tareas, errores y nuevas características, consulta los **[GitHub Issues del proyecto](https://github.com/brakdag/paser/issues)**.
