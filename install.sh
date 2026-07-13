#!/bin/bash

# GrillBiz MCP Server and Skills Installer
# Works on Mac (and other Unix systems).

echo "=================================================="
echo "          GRILLBIZ INSTALLATION WIZARD            "
echo "=================================================="

# Determine operating system
OS_NAME=$(uname)

# 1. Verify Python 3 & Version Requirement (>= 3.10)
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' &>/dev/null; then
    echo "Error: Python 3.10 or higher is required to run the Model Context Protocol (MCP) server."
    echo "Your current version is: $(python3 --version)"
    echo "Please upgrade Python (e.g. run 'brew install python' on Mac or use 'uv') and try again."
    exit 1
fi

# 2. Install Required Python Packages
echo -e "\n[1/3] Installing python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install mcp playwright pillow

# Install Playwright browser binaries
echo "Installing Chromium for card screenshot exports..."
python3 -m playwright install chromium

# 3. Configure Claude Desktop MCP (if macOS)
echo -e "\n[2/3] Registering GrillBiz with Claude Desktop..."
if [ "$OS_NAME" = "Darwin" ]; then
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    
    mkdir -p "$CLAUDE_CONFIG_DIR"
    
    # Run helper Python command to inject GrillBiz MCP server definition safely
    python3 -c "
import os, json

config_path = r\"$CLAUDE_CONFIG_FILE\"
server_script = os.path.abspath(\"mcp_server.py\")

if os.path.exists(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}
else:
    data = {}

if 'mcpServers' not in data:
    data['mcpServers'] = {}

data['mcpServers']['grillbiz'] = {
    'command': 'python3',
    'args': [server_script]
}

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('Success: Registered GrillBiz MCP server inside Claude Desktop config!')
"
else
    echo "Notice: Non-Mac OS detected. Skipping automated Claude Desktop configuration."
    echo "To configure Claude manually, add this block to your Claude Desktop config JSON:"
    echo "--------------------------------------------------"
    echo "  \"mcpServers\": {"
    echo "    \"grillbiz\": {"
    echo "      \"command\": \"python3\","
    echo "      \"args\": [\"$(pwd)/mcp_server.py\"]"
    echo "    }"
    echo "  }"
    echo "--------------------------------------------------"
fi

# 4. Copy skills to global agent customizations folders
echo -e "\n[3/4] Copying skills to local AI agent config directories..."
GEMINI_SKILLS_DIR="$HOME/.gemini/config/skills"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"

if [ -d "$GEMINI_SKILLS_DIR" ] || [ -d "$HOME/.gemini/config" ]; then
    mkdir -p "$GEMINI_SKILLS_DIR"
    cp -R skills/* "$GEMINI_SKILLS_DIR/"
    echo "✅ Copied GrillBiz skills to Antigravity global config ($GEMINI_SKILLS_DIR)"
fi

if [ -d "$CLAUDE_SKILLS_DIR" ] || [ -d "$HOME/.claude" ]; then
    mkdir -p "$CLAUDE_SKILLS_DIR"
    cp -R skills/* "$CLAUDE_SKILLS_DIR/"
    echo "✅ Copied GrillBiz skills to Claude Code global config ($CLAUDE_SKILLS_DIR)"
fi

# 5. Verify Local Installation
echo -e "\n[4/4] Verifying MCP server compilation..."
if python3 mcp_server.py --help &>/dev/null; then
    echo "Success: GrillBiz MCP Server compiled successfully!"
else
    echo "Warning: MCP Server could not start. Make sure you run 'pip install mcp'"
fi

echo -e "\n=================================================="
echo "          GRILLBIZ INSTALLED SUCCESSFULLY         "
echo "Restart Claude Desktop to start using GrillBiz tools!"
echo "=================================================="
