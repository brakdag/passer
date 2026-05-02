try:
    from paser.tools.ghost_browser import playwright_execute_sync
    print("Import successful")
except SyntaxError as e:
    print(f"SyntaxError: {e}")
except Exception as e:
    print(f"Other error: {e}")
