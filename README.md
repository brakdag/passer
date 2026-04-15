# Paser (Autonomous Function Calling System - ReAct Pattern)

<div align="center">
  <img src="assets/mascot.png" alt="Paser Mascot" width="200"/>
</div>

**Paser** is an autonomous agent powered by Google's Gemini model that employs the **ReAct (Reasoning and Acting)** pattern to execute local functions transparently. Designed and optimized for **Debian/Linux** systems.

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/brakdag/paser/main/install.sh | bash
```

## Execution

```bash
paser
```

## Project Structure

```text
. 
├── paser/                # Main application package
│   ├── core/             # ReAct engine, agent orchestration and state management
│   ├── tools/            # Tool definitions, registry and semantic navigators
│   ├── infrastructure/   # Low-level system wrappers and API clients
│   ├── config/           # Application settings and environment config
│   └── main.py           # CLI entry point
├── staff/                # Role definitions for specialized citizens (.md files)
├── tests/                # Unit and integration test suite
├── scripts/              # Installation and maintenance scripts
├── assets/               # Static assets and branding
├── docs/                 # Technical documentation
└── pyproject.toml        # Project metadata and dependencies
```

## Main Features

1. **Local Function Calling**: Uses a custom middleware to intercept `<TOOL_CALL>` and return `<TOOL_RESPONSE>`.
2. **Staff & Citizens System**: Paser acts as a **Pure Orchestrator (CEO)** that is strictly forbidden from editing code, delegating all technical implementations to specialized **Citizens** (mini-agents). 
    - **Roles**: Defined in `staff/*.md`.
    - **Isolation**: Each citizen has its own independent history.
    - **Efficiency**: Citizens use a fast model and limited execution turns to avoid blocking the main agent.
3. **Security**: All file operations are restricted to the `PROJECT_ROOT` via `get_safe_path`.

## User Commands
- `/models`: Change AI model.
- `/thinking`: Toggle reasoning visibility.
- `/cd <path>`: Change working directory.
- `/history`: Show tool execution summary.
- `/session`: Manage saved sessions.
- `/reset`: Restart application.
- `/max_turns <n>`: Set autonomous turn limit.

## Tool Management

### Adding a Tool
1. Implement function in `paser/tools/`.
2. Map in `paser/tools/registry.py`.
3. Define metadata in `paser/tools/registry_positional.json`.
4. Restart application.

## Available Tools

### Files & Directories
- `read_file`, `write_file`, `list_dir`, `replace_string`, `get_tree`, etc.

### Media & Interaction
- `web_search`, `fetch_url`, `api_request`, `speak_text`, `alert_sound`, etc.

### Code & Engineering
- `list_symbols`, `get_definition`, `analyze_pyright`, `execute_python`, `chat_with_paser_mini(prompt, citizen_id, role, context_str)`, etc.

### GitHub & Version Control
- `list_issues`, `create_issue`, `git_diff`, `get_current_repo`, etc.
