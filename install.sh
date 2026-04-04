#!/bin/bash
# Install script for 'passer'
set -e

# Get project root from where the script is executed
PROJECT_ROOT=$(pwd)
echo "Setting up project in: $PROJECT_ROOT"

# 1. Create/Recreate virtual environment
echo "Creating virtual environment..."
python3 -m venv "$PROJECT_ROOT/venv"

# 2. Upgrade pip and install dependencies
echo "Installing dependencies..."
"$PROJECT_ROOT/venv/bin/pip" install --upgrade pip
"$PROJECT_ROOT/venv/bin/pip" install -r "$PROJECT_ROOT/requirements.txt"

# 3. Setup symlink in ~/bin
echo "Setting up 'passer' command..."
mkdir -p "$HOME/bin"
# Ensure the script uses the absolute path dynamically
# We will regenerate chat.sh to be portable
echo "#!/bin/bash
PROJECT_ROOT=\"$PROJECT_ROOT\"
export PYTHONPATH=\"\$PROJECT_ROOT\"
\"\$PROJECT_ROOT/venv/bin/python\" -m passer.main \"\$@\"" > "$PROJECT_ROOT/chat.sh"
chmod +x "$PROJECT_ROOT/chat.sh"

ln -sf "$PROJECT_ROOT/chat.sh" "$HOME/bin/passer"

# 4. Check PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo "Warning: \$HOME/bin is not in your PATH."
    echo "Add 'export PATH=\"\$HOME/bin:\$PATH\"' to your ~/.zshrc or ~/.bashrc"
else
    echo "Successfully installed! You can now run 'passer' from anywhere."
fi
