# Plan de Trabajo: Simplificación y Renombramiento de Herramientas (Reflejos de Código)

El objetivo es renombrar las herramientas de Paser para que utilicen nombres basados en patrones de programación (Python/JS), facilitando que la IA las invoque de forma instintiva y reduciendo errores de llamada.

## ✅ Pasos a realizar

### 1. Renombramiento de Funciones Físicas
Cambiar el nombre de las definiciones de función en los módulos de herramientas:
- [x] `paser/tools/util_tools.py`: `obtener_hora_actual` → `get_time`, `calculadora_basica` → `calculate`, `obtener_directorio_actual` → `get_cwd`.
- [x] `paser/tools/file_tools.py`: `leer_archivo` → `read_file`, `escribir_archivo` → `write_file`, `borrar_archivo` → `remove_file`, `listar_archivos` → `list_dir`, `leer_lineas` → `read_lines`, `leer_cabecera` → `read_head`, `modificar_linea` → `update_line`, `reemplazar_texto` → `replace_text`, `reemplazar_bloque_texto` → `replace_block`, `buscar_reemplazar_global` → `global_replace`, `mover_archivo` → `rename_path`, `crear_carpeta` → `make_dir`.
- [x] `paser/tools/web_tools.py`: `buscar_en_internet` → `web_search`, `leer_url` → `fetch_url`.
- [x] `paser/tools/system_tools.py`: `analizar_codigo_con_pyright` → `analyze_pyright`.

### 2. Actualización del Registro y Catálogo
- [x] `paser/tools/registry.py`: 
    - Actualizar el mapa `AVAILABLE_TOOLS` con las nuevas referencias.
    - Actualizar el `TOOL_CATALOG` (JSON) con los nuevos nombres y descripciones.
    - Actualizar la `SYSTEM_INSTRUCTION`.

### 3. Sincronización de la Interfaz de Usuario
- [x] `paser/core/chat_manager.py`: Actualizar el diccionario `FILE_TOOLS` para que el feedback visual (iconos y verbos) coincida con los nuevos nombres de las herramientas.

### 4. Verificación Final
- [x] Validar que no existan referencias a los nombres antiguos en todo el proyecto.
- [x] Verificar que el `TOOL_CATALOG` sea coherente con las funciones implementadas.
- [x] Comprobar que el `ChatManager` sigue notificando correctamente el uso de archivos.