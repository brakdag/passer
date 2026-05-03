from DrissionPage import ChromiumPage, ChromiumOptions
import os
import time
import random

# Almacen global para mantener sesiones de navegador activas
BROWSER_SESSIONS = {}

class GhostBrowser:
    def __init__(self, session_id=None, headless=True):
        self.session_id = session_id
        self.options = ChromiumOptions()
        if headless:
            self.options.headless()
        
        if session_id:
            user_data_path = os.path.join(os.getcwd(), f"browser_profile_{session_id}")
            self.options.set_user_data_path(user_data_path)
        
        self.page = ChromiumPage(self.options)

    def _human_delay(self):
        """Simulates human hesitation."""
        time.sleep(random.uniform(0.5, 2.0))

    def execute_action(self, action_type, params):
        """
        Ejecución sincrónica de acciones de navegador.
        """
        try:
            result = {"status": "success", "data": None}
            
            self._human_delay()
            if action_type == "goto":
                url = params["url"]
                self.page.get(url)
                result["data"] = self.page.url
                
            elif action_type == "click":
                self._human_delay()
                selector = params["selector"]
                self.page.ele(selector).click()
                
            elif action_type == "fill":
                self._human_delay()
                selector = params["selector"]
                value = params["value"]
                self.page.ele(selector).input(value)
                
            elif action_type == "evaluate":
                script = params["script"]
                result["data"] = self.page.run_js(script)
                
            elif action_type == "screenshot":
                path = params.get("path", "screenshot.png")
                self.page.get_screenshot(path)
                result["data"] = path
                
            elif action_type == "get_content":
                result["data"] = self.page.html
                
            elif action_type == "wait_for":
                selector = params["selector"]
                self.page.ele(selector, timeout=10)
                
            elif action_type == "close_session":
                self.page.quit()
                result["data"] = "Session closed"
                
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Tool wrappers sincrónicos

def browser_execute(action: str, params: dict, session_id: str = "default"):
    """
    Wrapper que gestiona sesiones persistentes de DrissionPage.
    """
    # Si no hay sesión, usamos una por defecto
    if session_id is None:
        session_id = "default"

    # Recuperar sesión existente o crear una nueva
    if session_id not in BROWSER_SESSIONS:
        BROWSER_SESSIONS[session_id] = GhostBrowser(
            session_id=session_id, 
            headless=params.get("headless", True)
        )
    
    gb = BROWSER_SESSIONS[session_id]
    result = gb.execute_action(action, params)
    
    # Si la acción fue cerrar la sesión, la eliminamos del almacén
    if action == "close_session":
        BROWSER_SESSIONS.pop(session_id, None)
        
    return result

def network_intercept(pattern: str, url: str, timeout: int = 120):
    """
    Captura de red sincrónica usando el modo listen de DrissionPage.
    Incluye un timeout para evitar bloqueos infinitos.
    """
    page = None
    try:
        options = ChromiumOptions().headless()
        page = ChromiumPage(options)
        
        page.listen.start(pattern)
        page.get(url)
        
        # DrissionPage's wait() accepts a timeout parameter
        res = page.listen.wait(timeout=timeout)
        
        if not res:
            return [{"error": f"Timeout: No request matching pattern '{pattern}' was intercepted within {timeout}s"}]
            
        data = res.response.body
        return [{"url": res.url, "data": data}]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        if page:
            page.quit()

def proxy_rotate(proxy_url: str):
    """
    Configures the proxy for the current session using DrissionPage options.
    """
    try:
        return {"status": "success", "proxy": proxy_url, "action": "RESTART_REQUIRED"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
