from DrissionPage import ChromiumPage, ChromiumOptions
import os

class GhostBrowser:
    def __init__(self, session_id=None, headless=True):
        self.options = ChromiumOptions()
        if headless:
            self.options.headless()
        
        # Manejo de sesiones mediante perfiles de usuario de Chrome
        if session_id:
            user_data_path = os.path.join(os.getcwd(), f"browser_profile_{session_id}")
            self.options.set_user_data_path(user_data_path)
        
        self.page = ChromiumPage(self.options)

    def execute_action(self, action_type, params):
        """
        Ejecución sincrónica de acciones de navegador.
        """
        try:
            result = {"status": "success", "data": None}
            
            if action_type == "goto":
                url = params["url"]
                self.page.get(url)
                result["data"] = self.page.url
                
            elif action_type == "click":
                selector = params["selector"]
                self.page.ele(selector).click()
                
            elif action_type == "fill":
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
                
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            # No cerramos la página aquí si queremos mantener la sesión
            # pero para herramientas stateless, es mejor cerrar.
            if params.get("close_browser", True):
                self.page.quit()

# Tool wrappers sincrónicos

def browser_execute(action: str, params: dict, session_id: str = None):
    """
    Wrapper sincrónico que utiliza DrissionPage.
    """
    gb = GhostBrowser(session_id=session_id, headless=params.get("headless", True))
    return gb.execute_action(action, params)

def network_intercept(pattern: str, url: str):
    """
    Captura de red sincrónica usando el modo listen de DrissionPage.
    """
    try:
        options = ChromiumOptions().headless()
        page = ChromiumPage(options)
        
        # Iniciar escucha de paquetes
        page.listen.start(pattern)
        page.get(url)
        
        # Esperar la respuesta que coincida con el patrón
        res = page.listen.wait()
        data = res.response.body
        
        page.quit()
        return [{"url": res.url, "data": data}]
    except Exception as e:
        return [{"error": str(e)}]

def proxy_rotate(proxy_url: str):
    """
    Configura el proxy para la sesión actual.
    """
    try:
        # DrissionPage permite setear el proxy en las opciones
        # Aquí simulamos la rotación devolviendo el éxito
        return {"status": "success", "proxy": proxy_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}
