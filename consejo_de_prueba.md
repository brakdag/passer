# 🛡️ Instrucciones de Validación Post-Reinicio

**Atención Agente:** El sistema de navegación ha sido migrado de **Playwright** $\rightarrow$ **DrissionPage**. 

### ⚠️ La Regla de Oro del Reinicio
Si al ejecutar `playwright_execute` recibes el error: 
`"Sync loop error: Cannot run the event loop while another loop is running"` 

**EL REINICIO FALLÓ.** 
Ese error pertenece al código antiguo y ya no existe en el disco. Si aparece, significa que el servidor sigue ejecutando la versión cacheada en RAM. No intentes arreglar el código; solicita un reinicio completo del proceso.

### ✅ Protocolo de Verificación de DrissionPage
Una vez confirmado que el servidor ha reiniciado, ejecuta estas tres pruebas en orden para validar la integridad del nuevo motor sincrónico:

#### Prueba 1: Conectividad Básica
**Acción:** `goto` $\rightarrow$ `https://www.google.com`
**Resultado esperado:** `status: success` y la URL de Google en los datos.

#### Prueba 2: Extracción de DOM
**Acción:** `get_content`
**Resultado esperado:** Un string largo con el HTML de la página. Si devuelve contenido, el navegador está renderizando JS correctamente.

#### Prueba 3: Persistencia de Sesión
**Acción:** `goto` con un `session_id` específico y `"save_session": true` en los params.
**Resultado esperado:** Creación de una carpeta `browser_profile_<session_id>` en el directorio actual.

### 🛠️ Notas Técnicas para el Agente
- **Sincronismo:** Ya no hay `async/await` ni `ThreadPoolExecutor`. El flujo es lineal.
- **Stealth:** DrissionPage es nativamente más difícil de detectar que Playwright.
- **Selectores:** Utiliza selectores estándar de CSS o XPath.

**La verdad reside en la evidencia. No asumas que funciona hasta que las tres pruebas pasen.**

--- 
*Documento emitido por Sarah Jenkins - Sentinel of Integrity*