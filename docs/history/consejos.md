# 🛡️ Protocolo de Verificación: Playwright Execute

Para que la herramienta `playwright_execute` funcione, no basta con "intentarlo". Se requiere precisión quirúrgica en los parámetros. Si la herramienta falla, es probable que se esté violando uno de los siguientes puntos de integridad.

## 1. Anatomía Correcta de la Llamada
La herramienta espera una estructura estrictamente definida. Un error en la clave del diccionario resultará en un fallo.

**Ejemplo de payload correcto para `goto`:**
```json
{
  "action": "goto",
  "params": {
    "url": "https://www.google.com",
    "wait_until": "networkidle"
  },
  "session_id": "test_session_01"
}
```

## 2. Puntos Críticos de Falla (Checklist)

- [ ] **URL Completa:** Asegúrese de incluir el protocolo (`http://` o `https://`). Playwright no adivina el protocolo.
- [ ] **Estado de Espera (`wait_until`):** 
    - El valor por defecto es `networkidle` (espera a que no haya tráfico de red). En sitios con trackers persistentes o websockets, esto puede causar un **timeout**.
    - **Consejo:** Si la página no carga, pruebe cambiar `wait_until` a `domcontentloaded` o `load`.
- [ ] **Modo Headless:** Por defecto, el navegador corre en modo `headless: True`. No verá una ventana abrirse; la verdad reside únicamente en el valor de retorno.
- [ ] **Sesiones:** Si usa un `session_id`, asegúrese de que el archivo `ghost_session.json` exista o que la primera llamada use `"save_session": true` en los `params` para crear el estado.

## 3. Cómo Diagnosticar el Error
Si recibe un `status: error`, analice el mensaje:

- **TimeoutError:** La página tardó demasiado en responder o el `wait_until` fue demasiado estricto.
- **Invalid URL:** El formato de la URL es incorrecto.
- **Sync loop error:** (ESTO YA DEBERÍA ESTAR SOLUCIONADO). Si aparece, el sistema no ha sido reiniciado correctamente.

## 4. La Prueba de Fuego (Verificación Absoluta)
Para probar que la herramienta realmente "anda", no use solo `goto`. Use una secuencia de verificación:
1. `goto` $\rightarrow$ Verificar que devuelve la URL correcta.
2. `get_content` $\rightarrow$ Verificar que el HTML devuelto contiene el título esperado de la página.

**La verdad no se asume, se prueba.**

--- 
*Documento generado por Sarah Jenkins - Sentinel of Integrity*