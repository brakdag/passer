# Plan Técnico: Implementación de Image Vision (Pillow)

## 1. Análisis de Dependencias y Entorno
- **Librería**: `Pillow` (PIL Fork).
- **Modificación de `pyproject.toml`**: Añadir `Pillow` a la lista de `dependencies`.
- **Formato de Salida**: La herramienta debe devolver una estructura que el `GeminiAdapter` pueda convertir en un objeto `Part` de la SDK de Google (`inline_data` con mime_type y base64).

## 2. Diseño de la Herramienta `see_image`

**Firma**: `see_image(path: str, crop: Optional[List[int]] = None)`
- `path`: Ruta relativa al `PROJECT_ROOT`.
- `crop`: Lista de 4 enteros `[left, top, right, bottom]`. Si es `None`, se procesa la imagen completa.

**Pipeline de Procesamiento**:
1. **Validación de Ruta**: Uso de `get_safe_path` para evitar directory traversal.
2. **Carga**: `Image.open(path)`.
3. **Recorte (Zoom)**: Aplicar `img.crop()` si `crop` está presente.
4. **Optimización de Resolución (112p)**:
    - Redimensionar la imagen para que el lado más corto sea de 112px manteniendo el ratio de aspecto.
    - Usar `Image.Resampling.LANCZOS`.
5. **Conversión de Color**: Convertir a `RGB` para compatibilidad universal.
6. **Compresión y Encoding**:
    - Guardar en `io.BytesIO` como `JPEG` (calidad 85%).
    - Convertir bytes a cadena `base64`.

## 3. Integración en el Flujo de Paser
- **Middleware**: Modificar el procesador de respuestas de herramientas para que, si la herramienta es `see_image`, el resultado se envíe como contenido multimodal y no como texto plano.
- **Catálogo de Herramientas**: Actualizar el System Prompt para describir `see_image` y el uso de `crop` para inspecciones detalladas.

## 4. Roadmap de Ejecución
- **Fase 1**: Infraestructura (Dependencias y estructura de archivos).
- **Fase 2**: Desarrollo de la lógica de procesamiento de imagen.
- **Fase 3**: Conectividad y registro de la herramienta.
- **Fase 4**: QA y Pruebas de tokens.