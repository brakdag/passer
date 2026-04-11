import asyncio
import re
from paser.core.ui import console, print_model_response, get_input

class EventMonitor:
    def __init__(self, event_manager, executor):
        self.event_manager = event_manager
        self.executor = executor

    async def monitor_loop(self, thinking_enabled):
        while True:
            try:
                for msg in self.event_manager.check_expired_events():
                    console.print(f"\n[EVENTO] {msg}", style="bold magenta")
                    res = await self.executor.execute(
                        user_input=f"[SISTEMA: {msg} ha expirado]", 
                        thinking_enabled=thinking_enabled, 
                        get_confirmation_callback=get_input
                    )
                    if res: 
                        print_model_response(re.sub(r'<[^>]+>.*?</[^>]+>', '', res, flags=re.DOTALL))
                await asyncio.sleep(1)
            except Exception:
                await asyncio.sleep(10)
