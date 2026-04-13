import ast
import os
import sys
import json
import argparse
from .core_tools import ToolError

class CodeNavigator:
    def __init__(self, root_dir="."):
        self.root_dir = root_dir

    def _is_binary(self, path):
        try:
            with open(path, 'rb') as f:
                return b'\0' in f.read(1024)
        except Exception:
            return True

    def _get_python_files(self):
        python_files = []
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        return python_files

    def list_symbols(self, file_path):
        """Lists all classes and functions defined in a file."""
        if self._is_binary(file_path):
            raise ToolError("Binary file detected. Cannot list symbols.")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            
            symbols = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols.append({"name": node.name, "type": "function", "line": node.lineno})
                elif isinstance(node, ast.ClassDef):
                    symbols.append({"name": node.name, "type": "class", "line": node.lineno})
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            symbols.append({"name": target.id, "type": "variable", "line": node.lineno})
            
            return symbols
        except Exception as e:
            raise ToolError(str(e))

    def get_detailed_symbols(self, file_path):
        """Provides detailed information about symbols in a file, including signatures and decorators."""
        if self._is_binary(file_path):
            raise ToolError("Binary file detected.")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            
            details = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = [arg.arg for arg in node.args.args]
                    return_type = ast.unparse(node.returns) if node.returns else "Any"
                    decorators = [ast.unparse(dec) for dec in node.decorator_list]
                    details.append({
                        "name": node.name,
                        "type": "function",
                        "line": node.lineno,
                        "args": args,
                        "return_type": return_type,
                        "decorators": decorators
                    })
                elif isinstance(node, ast.ClassDef):
                    bases = [ast.unparse(base) for base in node.bases]
                    decorators = [ast.unparse(dec) for dec in node.decorator_list]
                    details.append({
                        "name": node.name,
                        "type": "class",
                        "line": node.lineno,
                        "bases": bases,
                        "decorators": decorators
                    })
            return details
        except Exception as e:
            return {"error": str(e)}

    def get_definition(self, symbol_name, file_path=None):
        """Finds the definition of a symbol. If file_path is None, searches the project."""
        files_to_search = [file_path] if file_path else self._get_python_files()
        
        for path in files_to_search:
            if not path or not os.path.exists(path) or self._is_binary(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == symbol_name:
                        return {"path": path, "line": node.lineno, "column": node.col_offset}
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == symbol_name:
                                return {"path": path, "line": node.lineno, "column": target.col_offset}
            except Exception:
                continue
        
        raise ToolError(f"Symbol '{symbol_name}' not found.")

    def get_references(self, symbol_name, file_path=None):
        """Finds all references to a symbol."""
        files_to_search = [file_path] if file_path else self._get_python_files()
        references = []

        for path in files_to_search:
            if not path or not os.path.exists(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Name) and node.id == symbol_name:
                        references.append({"path": path, "line": node.lineno, "column": node.col_offset})
            except Exception:
                continue
        
        return references

    def find_all_calls(self, symbol_name, file_path=None):
        """Finds all calls to a specific function or method."""
        files_to_search = [file_path] if file_path else self._get_python_files()
        calls = []

        for path in files_to_search:
            if not path or not os.path.exists(path) or self._is_binary(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Handle direct calls: func()
                        if isinstance(node.func, ast.Name) and node.func.id == symbol_name:
                            calls.append({"path": path, "line": node.lineno, "column": node.func.col_offset})
                        # Handle method calls: obj.func()
                        elif isinstance(node.func, ast.Attribute) and node.func.attr == symbol_name:
                            calls.append({"path": path, "line": node.lineno, "column": node.func.col_offset})
            except Exception:
                continue
        
        return calls

    def get_imports(self, file_path):
        """Lists all imports in a file."""
        if self._is_binary(file_path):
            return {"error": "Binary file detected."}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({"module": alias.name, "alias": alias.asname})
                elif isinstance(node, ast.ImportFrom):
                    module = node.module if node.module else "__main__"
                    for alias in node.names:
                        imports.append({"module": f"{module}.{alias.name}", "alias": alias.asname})
            return imports
        except Exception as e:
            return {"error": str(e)}

    def find_missing_type_hints(self, file_path):
        """Finds functions and arguments missing type hints."""
        if self._is_binary(file_path):
            return {"error": "Binary file detected."}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            
            missing = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Check arguments
                    for arg in node.args.args:
                        if arg.arg in ("self", "cls"):
                            continue
                        if not arg.annotation:
                            missing.append({
                                "symbol": node.name,
                                "line": node.lineno,
                                "type": "argument",
                                "detail": f"Argument '{arg.arg}' missing type hint"
                            })
                    # Check return type
                    if not node.returns:
                        missing.append({
                            "symbol": node.name,
                            "line": node.lineno,
                            "type": "return",
                            "detail": "Return type missing"
                        })
            return missing
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Code Navigator Tool")
    parser.add_argument("--define", type=str, help="Symbol to find definition for")
    parser.add_argument("--refs", type=str, help="Symbol to find references for")
    parser.add_argument("--symbols", type=str, help="File to list symbols from")
    parser.add_argument("--calls", type=str, help="Function name to find all calls for")
    parser.add_argument("--detailed", type=str, help="File to get detailed symbols from")
    parser.add_argument("--imports", type=str, help="File to list imports from")
    parser.add_argument("--hints", type=str, help="File to check for missing type hints")
    parser.add_argument("--file", type=str, help="Specific file to target (optional)")

    args = parser.parse_args()
    nav = CodeNavigator()

    result = None
    if args.define:
        result = nav.get_definition(args.define, args.file)
    elif args.refs:
        result = nav.get_references(args.refs, args.file)
    elif args.symbols:
        result = nav.list_symbols(args.symbols)
    elif args.calls:
        result = nav.find_all_calls(args.calls, args.file)
    elif args.detailed:
        result = nav.get_detailed_symbols(args.detailed)
    elif args.imports:
        result = nav.get_imports(args.imports)
    elif args.hints:
        result = nav.find_missing_type_hints(args.hints)
    else:
        result = {"error": "No action specified. Use --define, --refs, --symbols, --calls, --detailed, --imports, or --hints."}

    print(json.dumps(result, indent=2))