import unittest
import json
from paser.tools.ghost_browser import browser_execute

class TestGhostBrowser(unittest.TestCase):
    def test_playwright_execute_noop(self):
        """Validate that browser_execute returns a JSON-serializable dict for a no-op action."""
        # 'noop' is not explicitly handled in browser_execute, it will fall through
        # and return success with data=None unless it crashes.
        result = browser_execute(action="noop", params={}, session_id=None)
        
        self.assertIsInstance(result, dict, "Result must be a dict")
        self.assertEqual(result.get("status"), "success", f"Unexpected status: {result}")
        # Ensure it can be JSON-encoded without error
        json.dumps(result)

if __name__ == '__main__':
    unittest.main()