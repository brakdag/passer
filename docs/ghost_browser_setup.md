# Guía de Configuración: Ghost-Browser Toolset

Este documento explica cómo configurar las dependencias necesarias para que las herramientas de navegación de alta fidelidad (`browser_execute`, `network_intercept`) funcionen correctamente.

## Requisitos Previos

Las herramientas de Ghost-Browser dependen de **Playwright** y **playwright-stealth**. Aunque estas se añaden al `pyproject.toml`, la instalación de los binarios del navegador es un paso separado.

## Instalación Paso a Paso

### 1. Instalar dependencias de Python
Si has modificado el `pyproject.toml`, asegúrate de actualizar tu entorno:

```bash
# Si usas pip directamente
pip install playwright playwright-stealth

# O si instalas el proyecto
pip install -e .
```

### 2. Instalar los binarios de Chromium
Playwright requiere descargar los ejecutables de los navegadores. Ejecuta el siguiente comando **dentro de tu entorno virtual**:

```bash
# Opción A: Con el venv activado
playwright install chromium

# Opción B: Sin activar el venv (usando la ruta directa)
./venv/bin/python -m playwright install chromium
```

### 3. (Opcional) Dependencias del Sistema
En algunos sistemas Linux (como Debian/Ubuntu), es posible que necesites instalar librerías adicionales para que Chromium pueda ejecutarse:

```bash
playwright install-deps
```

## Solución de Problemas

### Error: `command not found: playwright`
Este error ocurre porque el comando `playwright` no está en tu PATH global. 
**Solución:** Usa siempre `python -m playwright` o activa tu entorno virtual con `source venv/bin/activate`.

### Error: `ImportError: cannot import name 'stealth_async'`
Este error indica una versión incorrecta de la implementación. Asegúrate de estar usando la versión corregida que utiliza `from playwright_stealth import stealth`.

---
*Documento generado para el proyecto Paser.*