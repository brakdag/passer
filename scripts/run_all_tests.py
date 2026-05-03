import sys
import subprocess
import os

# Resolve the project root
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    print(f"Running all tests using pytest from {root_dir}...\n")
    # Use sys.executable -m pytest to ensure we use the pytest installed in the current environment
    result = subprocess.run([sys.executable, '-m', 'pytest', 'tests'], cwd=root_dir)
    
    if result.returncode != 0:
        print("\nTests failed!")
        sys.exit(result.returncode)
    else:
        print("\nAll tests passed successfully!")
