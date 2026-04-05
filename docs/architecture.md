# Arquitectura del Sistema: Function Calling Local (Patrón ReAct)

Este proyecto implementa un agente autónomo utilizando el modelo Gemini de Google (vía `google-genai` SDK) que emplea el patrón **ReAct (Reasoning and Acting)** para ejecutar funciones locales de forma transparente para el usuario.

## 🎯 Objetivo Principal

Integrar un sistema de "Function Calling" (Llamada a Funciones) **completamente local y manual**.

**Restricción Crítica:** ESTÁ ESTRICTAMENTE PROHIBIDO utilizar los parámetros nativos de la SDK de Google (`tools`, `function_calling`, `ToolConfig`, etc.). Todo el ciclo de razonamiento, invocación y respuesta debe manejarse exclusivamente a través de manipulación de texto (Prompt Engineering), parseo del output y control del flujo de chat.

## 🏗️ Arquitectura del Sistema

El sistema opera bajo un bucle ReAct (Reasoning and Acting) con los siguientes componentes:

### 1. Inyección del "System Prompt"
Al inicializar el modelo, se inyecta un contexto inicial robusto (System Instruction) que obliga al modelo a seguir este contrato:
- **Catálogo:** Lista de funciones disponibles.
- **Sintaxis Estricta:** Si el modelo decide usar una herramienta, su respuesta debe detenerse y emitir un bloque de texto exacto:
  ```text
  <TOOL_CALL>{"name": "nombre_de_funcion", "args": {"param1": "valor"}}</TOOL_CALL>
  ```
- **Regla de Pausa:** El modelo no debe inventar la respuesta de la herramienta, sino emitir el `<TOOL_CALL>` y esperar el resultado.

### 2. Middleware de Intercepción (Streaming Parser)
El sistema intercepta el flujo de respuesta del modelo:
- Acumula los `chunk.text` en un búfer.
- Busca el patrón `<TOOL_CALL>` mediante expresiones regulares.
- Si detecta texto normal, lo imprime.
- Si detecta `<TOOL_CALL>`, oculta el bloque, extrae el JSON y ejecuta la herramienta localmente.

### 3. Execution Environment (El Runner)
Existe un registro (`AVAILABLE_TOOLS`) que enruta el nombre de la función (parseado del JSON) a la implementación en Python.

### 4. Bucle de Retroalimentación (Feedback Loop)
Una vez que la función local retorna un valor, se formatea y envía de vuelta al historial del chat:
```text
<TOOL_RESPONSE>{"status": "success", "data": "..."}</TOOL_RESPONSE>
```
Este proceso continúa hasta que el modelo emita una respuesta en lenguaje natural para el usuario.
