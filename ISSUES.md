# Project Issues

## [Resolved] UI: Professional Spinner Implementation
- **Description**: The previous spinner was a moving dot that spanned 80 characters, which was visually distracting and could interfere with other UI elements.
- **Solution**: Implemented a compact, Braille-based animated spinner (approx. 10 characters) using Nerd Fonts characters. This provides a more modern "pro" look and ensures no overlap with JSON tool calls or notifications.
- **File changed**: `paser/core/ui.py`

## [Open] Core: Malformed TOOL_CALL Feedback
- **Description**: When a `<TOOL_CALL>` is malformed (e.g., missing 'name' key), the executor logs the error to the console but doesn't return a response to the LLM. The model is left without feedback, potentially causing loops.
- **Solution**: Ensure that any parsing failure in `AutonomousExecutor` results in a `<TOOL_RESPONSE>` with `status: "error"` so the model can self-correct.
- **File changed**: `paser/core/executor.py`

## [Open] Tools: False Positive Success Status
- **Description**: Some tools return a string (e.g., "Error: File not found") instead of raising an exception. This leads to the executor reporting `status: "success"` despite the operation failing.
- **Solution**: Standardize tool error handling by removing internal try-except blocks that return error strings, allowing exceptions to propagate to the executor's global handler.
- **File changed**: `paser/tools/file_tools.py`, `paser/tools/web_tools.py`, etc.