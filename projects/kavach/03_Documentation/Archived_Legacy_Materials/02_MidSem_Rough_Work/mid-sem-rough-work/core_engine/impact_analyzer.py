"""
KAVACH AST Dependency Graph & Blast-Radius Engine.
Statically parses Python modules into AST call graphs to compute
downstream regression blast radius and transitive caller-callee impacts.
"""

import ast
import os
from typing import Dict, List, Set, Any

class CodebaseCallGraph(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.functions: Set[str] = set()
        self.classes: Set[str] = set()
        self.calls: Set[str] = set()
        self.imports: Dict[str, str] = {}
        self.current_function: str = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.add(node.name)
        prev = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.functions.add(node.name)
        prev = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        if func_name:
            self.calls.add(func_name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            for alias in node.names:
                self.imports[alias.name] = node.module
        self.generic_visit(node)

class ASTImpactAnalyzer:
    """
    Constructs multi-file dependency graph and calculates transitive blast-radius.
    """
    def __init__(self, root_dir: str = None):
        self.root_dir = root_dir
        self.file_graphs: Dict[str, CodebaseCallGraph] = {}
        self.function_locations: Dict[str, str] = {}  # func -> filename
        self.callee_to_callers: Dict[str, Set[str]] = {}  # func -> set(calling_files)
        if root_dir and os.path.isdir(root_dir):
            self.scan_directory(root_dir)

    def analyze_source_code(self, filename: str, code: str):
        """Analyzes a single source string and registers its AST node relations."""
        try:
            tree = ast.parse(code)
            graph = CodebaseCallGraph(filename)
            graph.visit(tree)
            self.file_graphs[filename] = graph

            for fn in graph.functions:
                self.function_locations[fn] = filename

            for call in graph.calls:
                if call not in self.callee_to_callers:
                    self.callee_to_callers[call] = set()
                self.callee_to_callers[call].add(filename)
        except SyntaxError:
            pass

    def scan_directory(self, directory: str):
        """Recursively parses all python files in directory."""
        for root, _, files in os.walk(directory):
            for f in files:
                if f.endswith(".py"):
                    full_path = os.path.join(root, f)
                    try:
                        with open(full_path, "r", encoding="utf-8") as fp:
                            content = fp.read()
                            rel_path = os.path.relpath(full_path, directory)
                            self.analyze_source_code(rel_path, content)
                    except Exception:
                        pass

    def compute_blast_radius(self, modified_file: str, target_function: str = None) -> Dict[str, Any]:
        """
        Computes transitive affected callers and downstream modules.
        """
        affected_files: Set[str] = set()
        affected_functions: Set[str] = set()

        # Direct file impact
        affected_files.add(modified_file)

        # If specific function is modified, find all direct callers
        if target_function and target_function in self.callee_to_callers:
            callers = self.callee_to_callers[target_function]
            affected_files.update(callers)
            affected_functions.add(target_function)

        # Check imports across other files
        base_mod = os.path.splitext(os.path.basename(modified_file))[0]
        for f_name, graph in self.file_graphs.items():
            if f_name == modified_file:
                continue
            for imp_name, imp_mod in graph.imports.items():
                if imp_mod == base_mod or imp_mod.endswith(f".{base_mod}"):
                    affected_files.add(f_name)

        # Calculate blast radius metric (0.0 to 1.0)
        total_files = max(1, len(self.file_graphs))
        blast_percentage = round((len(affected_files) / total_files) * 100, 1)

        # Risk severity
        if blast_percentage > 50 or "auth" in modified_file.lower() or "db" in modified_file.lower():
            risk_level = "HIGH"
        elif blast_percentage > 20:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "modified_file": modified_file,
            "target_function": target_function,
            "affected_files": sorted(list(affected_files)),
            "affected_functions": sorted(list(affected_functions)),
            "blast_percentage": blast_percentage,
            "risk_level": risk_level,
            "total_repo_files": total_files
        }

if __name__ == "__main__":
    analyzer = ASTImpactAnalyzer()
    
    code_db = """
def get_db_connection():
    return "db_conn"

def execute_query(sql):
    conn = get_db_connection()
    return f"results for {sql}"
"""
    code_auth = """
from db_connector import execute_query

def authenticate_user(username, token):
    res = execute_query(f"SELECT * FROM users WHERE user='{username}'")
    return res is not None
"""
    code_api = """
from auth_service import authenticate_user

def login_endpoint(user, token):
    if authenticate_user(user, token):
        return {"status": "success"}
    return {"status": "unauthorized"}
"""
    analyzer.analyze_source_code("db_connector.py", code_db)
    analyzer.analyze_source_code("auth_service.py", code_auth)
    analyzer.analyze_source_code("api.py", code_api)

    print("--- BLAST RADIUS FOR MODIFYING execute_query in db_connector.py ---")
    blast = analyzer.compute_blast_radius("db_connector.py", target_function="execute_query")
    print(blast)
