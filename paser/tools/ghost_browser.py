import asyncio
import json
import random
import os
from playwright.async_api import async_playwright
from playwright_stealth import stealth

class GhostBrowser:
    def __init__(self):
        self.storage_state_path = "ghost_session.json"
        self.intercepted_data = []

    async def execute_action(self, action_type, params, session_id=None):
        """
        Core method to execute playwright actions.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=params.get("headless", True))
            
            # Load session if exists
            context_args = {}
            if session_id and os.path.exists(self.storage_state_path):
                context_args["storage_state"] = self.storage_state_path

            context = await browser.new_context(**context_args)
            page = await context.new_page()
            
            # Apply stealth
            await stealth(page)

            # Setup network interception
            page.on("response", lambda response: self._handle_response(response))

            result = {"status": "success", "data": None}
            try:
                if action_type == "goto":
                    await page.goto(params["url"], wait_until=params.get("wait_until", "networkidle"))
                    result["data"] = page.url
                elif action_type == "click":
                    await page.click(params["selector"])
                elif action_type == "fill":
                    await page.fill(params["selector"], params["value"])
                elif action_type == "evaluate":
                    result["data"] = await page.evaluate(params["script"])
                elif action_type == "screenshot":
                    path = params.get("path", "screenshot.png")
                    await page.screenshot(path=path)
                    result["data"] = path
                elif action_type == "get_content":
                    result["data"] = await page.content()
                elif action_type == "wait_for":
                    await page.wait_for_selector(params["selector"])
                
                # Save session if requested
                if params.get("save_session"):
                    await context.storage_state(path=self.storage_state_path)

            except Exception as e:
                result = {"status": "error", "message": str(e)}
            finally:
                await browser.close()
            
            return result

    def _handle_response(self, response):
        # Logic for network_intercept
        pass

    async def capture_network_data(self, pattern):
        """
        Captures network responses matching a pattern.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            captured = []
            
            async def handle_response(response):
                if pattern in response.url:
                    try:
                        data = await response.json()
                        captured.append({"url": response.url, "data": data})
                    except:
                        try:
                            text = await response.text()
                            captured.append({"url": response.url, "data": text})
                        except:
                            pass

            page.on("response", handle_response)
            return captured

# Tool wrappers to be called by registry.py

async def playwright_execute(action: str, params: dict, session_id: str = None):
    gb = GhostBrowser()
    res = await gb.execute_action(action, params, session_id)
    return res

def playwright_execute_sync(action: str, params: dict, session_id: str = None):
    """
    Synchronous wrapper to prevent coroutine serialization errors.
    """
    import asyncio
    gb = GhostBrowser()
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(gb.execute_action(action, params, session_id))



async def network_intercept(pattern: str, url: str):
    gb = GhostBrowser()
    # We use a simplified approach: navigate to URL and capture
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Apply stealth here too
        await stealth(page)

        captured = []
        async def handle_response(response):
            if pattern in response.url:
                try:
                    data = await response.json()
                    captured.append({"url": response.url, "data": data})
                except:
                    try:
                        text = await response.text()
                        captured.append({"url": response.url, "data": text})
                    except:
                        pass

        page.on("response", handle_response)
        try:
            await page.goto(url, wait_until="networkidle")
            await asyncio.sleep(2) # Wait for async responses
        except Exception as e:
            return [{"error": str(e)}]
        finally:
            await browser.close()
        return captured

async def proxy_rotate(proxy_url: str):
    # Placeholder for proxy rotation logic
    return {"status": "success", "proxy": proxy_url}
