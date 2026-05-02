# Paser: Technical Manual

## System Overview
Paser is an autonomous agent powered by Google's Gemini model that employs the **ReAct (Reasoning and Acting)** pattern to execute local functions transparently. Designed and optimized for **Debian/Linux** systems.

## Project Structure
```text
.
├── paser/                # Main application package
│   ├── core/             # ReAct engine, agent orchestration and state management
│   ├── tools/            # Tool definitions, registry and semantic navigators
│   ├── infrastructure/   # Low-level system wrappers and API clients
│   ├── config/           # Application settings and environment config
│   └── main.py           # CLI entry point
├── docs/
│   ├── technical_manual.md
│   └── staff/
│       ├── [member_name].md
│       └── HISTORY.md
├── tests/                # Unit and integration test suite
├── scripts/              # Installation and maintenance scripts
├── assets/               # Static assets and branding
├── docs/                 # Technical documentation
└── pyproject.toml        # Project metadata and dependencies
```

## Communication Protocol
- **Brevity & Productivity**: Concise, direct, and actionable output.
- **Local Function Calling**: Custom middleware for `<TOOL_CALL>` and `<TOOL_RESPONSE>`.
- **Security**: All file operations are restricted to the `PROJECT_ROOT` via `get_safe_path`.

## User Commands
- `/models`: Change AI model.
- `/thinking`: Toggle reasoning visibility.
- `/cd <path>`: Change working directory.
- `/history`: Show tool execution summary.
- `/session`: Manage saved sessions.
- `/reset`: Restart application.
- `/max_turns <n>`: Set autonomous turn limit.

## Tool Management
1. Implement function in `paser/tools/`.
2. Map in `paser/tools/registry.py`.
3. Define metadata in `paser/tools/registry_positional.json`.
4. Restart application.

## Prohibited Tools (Strict)
- `play_music`, `stop_music`, `speak_text`, `compile_latex`, `is_window_in_focus`.
- **Web Navigation**: `web_search`, `fetch_url`, `render_web_page`.
- **Code Navigation**: `get_definition`, `get_references`, `list_symbols`, etc.
- **System & API**: `convert_image`, `api_request`, `execute_python`.

## Available Tools
- Files & Directories: `read_file`, `write_file`, `list_dir`, `replace_string`, `get_tree`.
- Media & Interaction: `web_search`, `fetch_url`, `api_request`, `speak_text`, `alert_sound`.
- Code & Engineering: `list_symbols`, `get_definition`, `analyze_pyright`, `execute_python`, `chat_with_paser_mini`.
- GitHub & Version Control: `list_issues`, `create_issue`, `git_diff`, `get_current_repo`.