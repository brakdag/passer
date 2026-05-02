import json

def test_playwright_execute_noop():
    """Validate that playwright_execute_sync returns a JSON-serializable dict for a no-op action."""
    from paser.tools.ghost_browser import playwright_execute_sync

    result = playwright_execute_sync(action="noop", params={}, session_id=None)
    # Should be a dict with status "success"
    assert isinstance(result, dict), "Result must be a dict"
    assert result.get("status") == "success", f"Unexpected status: {result}"
    # Ensure it can be JSON-encoded without error
    json.dumps(result)
