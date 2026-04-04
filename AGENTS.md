# AGENTS.md: Implementación de Custom Function Calling (ReAct Pattern)

## 🎯 OBJETIVO PRINCIPAL

 Integrar un sistema de "Function Calling" (Llamada a Funciones) **completamente local y manual**.

**RESTRICCIÓN CRÍTICA:** ESTÁ ESTRICTAMENTE PROHIBIDO utilizar los parámetros nativos de la SDK de Google (`tools`, `function_calling`, `ToolConfig`, etc.). Todo el ciclo de razonamiento, invocación y respuesta debe manejarse exclusivamente a través de manipulación de texto (Prompt Engineering), parseo del output y control del flujo de chat.

## 🏗️ ARQUITECTURA DEL SISTEMA

El sistema debe operar bajo un bucle ReAct (Reasoning and Acting) con los siguientes componentes:

### 1. Inyección del "System Prompt"

Al inicializar `genai.GenerativeModel`, debes inyectar un contexto inicial robusto (System Instruction) que obligue al modelo a seguir este contrato:

- **Catálogo:** Lista de funciones disponibles en formato legible (ej. JSON Schema o firmas de funciones).
- **Sintaxis Estricta:** Si el modelo decide usar una herramienta, su respuesta **debe detenerse** y emitir un bloque de texto exacto con este formato:
  ```text
  <TOOL_CALL>{"name": "nombre_de_funcion", "args": {"param1": "valor"}}</TOOL_CALL>
  ```
- **Regla de Pausa:** El modelo debe entender que no debe inventar la respuesta de la herramienta, sino emitir el `<TOOL_CALL>` y esperar el resultado.

### 2. Middleware de Intercepción (Streaming Parser)

Actualmente el script usa `stream=True` y hace `print` directo. Modifica esta lógica:

- Acumula los `chunk.text` en una variable `buffer` de tipo string.
- Mientras se hace el streaming, busca el patrón `<TOOL_CALL>` usando Expresiones Regulares (`re`).
- **Si detecta texto normal:** Haz un `print` a la consola como lo hace actualmente (imitando un stream fluido).
- **Si detecta `<TOOL_CALL>`:** Oculta este bloque al usuario (no lo imprimas). Extrae el JSON contenido dentro de las etiquetas.

### 3. Execution Environment (El Runner)

Crea un diccionario de enrutamiento o "Registry":

```python
AVAILABLE_TOOLS = {
    "obtener_clima": funcion_python_obtener_clima,
    "calculadora": funcion_python_calculadora
}
```

Toma el JSON parseado del paso 2.

Verifica si name existe en AVAILABLE_TOOLS.

Desempaqueta args y ejecuta la función Python correspondiente.

Captura cualquier excepción (try/except) durante la ejecución para evitar que el script colapse si el modelo alucina parámetros.

4. Bucle de Retroalimentación (Feedback Loop)
   Una vez que la función local retorna un valor (o un mensaje de error):

Formatea el resultado en un bloque de texto. Ejemplo:

Plaintext

<TOOL_RESPONSE>{"status": "success", "data": "25°C, soleado"}</TOOL_RESPONSE>
Envía silenciosamente este bloque al historial del chat usando chat.send_message(resultado_formateado, stream=True) sin pedir input del usuario.

Procesa esta nueva respuesta (volviendo al paso 2) hasta que el modelo emita una respuesta en lenguaje natural para el usuario.

🛠️ TAREAS DE IMPLEMENTACIÓN PARA LA IA
Refactorizar iniciar_chat(): Modifica el loop while True para soportar el ciclo de intercepción y re-ejecución descrito.

Crear 2 Funciones de Prueba (Mock Tools):

obtener_hora_actual(zona_horaria: str) -> Devuelve la hora.

calculadora_basica(operacion: str) -> Evalúa una operación matemática simple.

Mantener Funcionalidad Existente: El comando :q (salir) y /models (cambiar modelo) deben seguir funcionando perfectamente. El historial de chat debe persistir correctamente durante la sesión.

⚠️ CRITERIOS DE ACEPTACIÓN
El código resultante es un script funcional en Python 3.

No usa tools= en la configuración del modelo de genai.

El usuario final solo ve las respuestas conversacionales del modelo, el intercambio de <TOOL_CALL> y <TOOL_RESPONSE> ocurre de forma invisible en el background.
