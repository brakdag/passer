import asyncio
from paser.tools.ghost_browser import playwright_execute_sync
import json

def test_serialization():
    try:
        # Test a simple action
        result = playwright_execute_sync(action="goto", params={"url": "https://www.google.com"})
        print(f"Result type: {type(result)}")
        print(f"Result value: {result}")
        
        # Try to serialize it
        json.dumps(result)
        print("Serialization successful!")
    except Exception as e:
        print(f"Caught expected error: {e}")

if __name__ == "__main__":
    test_serialization()