import sys
import os

# Ensure project root is in path
root_path = os.getcwd()
if root_path not in sys.path:
    sys.path.append(root_path)

try:
    from paser.tools.registry import AVAILABLE_TOOLS
    print("Successfully imported AVAILABLE_TOOLS from registry.")
    
    if 'neural_mouse_control' in AVAILABLE_TOOLS:
        print("Tool 'neural_mouse_control' found in registry.")
        
        # Test the tool functionality
        print("Testing tool execution with screenshot command...")
        result = AVAILABLE_TOOLS['neural_mouse_control']("rect(0, 0, 0, 0)")
        
        if result.get('status') == 'screenshot_captured':
            print("SUCCESS: Tool executed and captured screenshot.")
            print(f"Image Resolution: {result['image']['resolution']}")
        else:
            print(f"FAILURE: Tool returned unexpected status: {result}")
    else:
        print("FAILURE: 'neural_mouse_control' NOT found in AVAILABLE_TOOLS mapping.")

except Exception as e:
    print(f"CRITICAL ERROR during integration test: {e}")
    import traceback
    traceback.print_exc()