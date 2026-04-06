# Project Issues

## [Resolved] UI: Contextual Icon Audit & Emoji Removal
- **Description**: Standard Unicode emojis were rendering as boxes (tofu) in the user's terminal. All visual indicators were migrated to strictly Nerd Font glyphs.
- **Solution**: Scanned all files and replaced non-NF characters with context-appropriate Nerd Font glyphs.
- **Files**: `paser/core/chat_manager.py`, `paser/core/ui.py`, `paser/core/commands.py`, `README.md`.

## [Resolved] UI: Nerd Font Icon Standardization
- **Description**: Standardized icons to ensure compatibility with JetBrains Mono Nerd Font v3.0+.
- **Solution**: Mapped common emojis to their NF equivalents.

## [Resolved] UI: Professional Spinner Implementation
- **Description**: Replaced the distracting 80-character spinner with a compact Braille-based animated spinner.
- **File changed**: `paser/core/ui.py`

## [Open] Core: Malformed TOOL_CALL Feedback
- **Description**: When a `<TOOL_CALL>` is malformed, the executor logs the error but doesn't return a response to the LLM, potentially causing loops.
- **Solution**: Ensure any parsing failure results in a `<TOOL_RESPONSE>` with `status: "error"`.
- **File changed**: `paser/core/executor.py`

## [Open] Tools: False Positive Success Status
- **Description**: Some tools return error strings instead of raising exceptions, leading to false `status: "success"` reports.
- **Solution**: Standardize tool error handling by allowing exceptions to propagate to the executor's global handler.
- **File changed**: `paser/tools/file_tools.py`, `paser/tools/web_tools.py`, etc.