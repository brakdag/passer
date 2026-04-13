import json
import os
from typing import Optional, List, Dict, Any

# Mapping of tools to categories
# Synchronized with registry_positional.json
TOOL_CATEGORIES = {
    "files": [
        "read_file", "read_files", "write_file", "remove_file", "list_dir", 
        "read_lines", "read_head", "update_line", "replace_string", 
        "replace_string_at_line", "global_replace", "rename_path", "create_dir", 
        "search_files_pattern", "search_text_global", "get_tree", 
        "read_file_with_lines", "copy_lines", "cut_lines", "paste_lines", "manage_imports",
        "get_cwd"
    ],
    "media": [
        "web_search", "fetch_url", "render_web_page", "api_request", 
        "see_image", "alert_sound", "convert_image", "play_music", 
        "stop_music", "speak_text", "notify_mobile", "notify_user", 
        "set_timer", "is_window_in_focus", "compile_latex",
        "get_time", "discover_capabilities"
    ],
    "github": [
        "list_issues", "create_issue", "close_issue", "edit_issue",
        "git_diff", "get_current_repo", "revert_file"
    ],
    "code": [
        "analyze_pyright", "get_definition", "get_references", "list_symbols", "find_all_calls", 
        "get_detailed_symbols", "get_imports", "find_missing_type_hints", 
        "format_code", "get_lsp_completions", "get_object_methods", "execute_python",
        "validate_json", "validate_json_file", "query_ai"
    ],
}

def discover_capabilities(category: Optional[str] = None) -> str:
    """
    Lists available tools. If no category is provided, returns a list of categories.
    If a category is provided, returns the detailed description and parameters of tools in that category.
    """
    catalog_path = os.path.join(os.path.dirname(__file__), "registry_positional.json")
    
    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
    except Exception as e:
        return f"Error loading tool catalog: {str(e)}"

    if category is None:
        categories = sorted(list(TOOL_CATEGORIES.keys()))
        return f"Available tool categories: {', '.join(categories)}"

    category = category.lower()
    if category not in TOOL_CATEGORIES:
        return f"Category '{category}' not found. Available categories: {', '.join(sorted(list(TOOL_CATEGORIES.keys())))}"

    tools_in_category = TOOL_CATEGORIES[category]
    detailed_tools = []

    for tool_def in catalog:
        name, description, params = tool_def
        if name in tools_in_category:
            detailed_tools.append(f"- {name}: {description} | Params: {params}")

    if not detailed_tools:
        return f"No tools found in category '{category}'."

    return f"Tools in category '{category}':\n" + "\n".join(detailed_tools)
