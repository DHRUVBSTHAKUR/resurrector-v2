import ast
import os
import json

class RepoMapper:
    def __init__(self, root_dir="./agent_workspace"):
        self.root_dir = root_dir

    def get_signatures(self, file_path):
        """Extracts class and function signatures using AST."""
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read())

        definitions = {
            "classes": [],
            "functions": [],
            "imports": []
        }

        for item in node.body:
            # Extract Functions
            if isinstance(item, ast.FunctionDef):
                args = [arg.arg for arg in item.args.args]
                definitions["functions"].append(f"{item.name}({', '.join(args)})")
            
            # Extract Classes
            elif isinstance(item, ast.ClassDef):
                class_methods = [
                    m.name for m in item.body if isinstance(m, ast.FunctionDef)
                ]
                definitions["classes"].append({
                    "name": item.name,
                    "methods": class_methods
                })
            
            # Extract Imports (to track dependencies)
            elif isinstance(item, (ast.Import, ast.ImportFrom)):
                definitions["imports"].append(ast.dump(item))

        return definitions

    def generate_map(self):
        """Walks the repo and creates a global JSON map."""
        repo_map = {}
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, file), self.root_dir)
                    try:
                        repo_map[rel_path] = self.get_signatures(os.path.join(root, file))
                    except Exception as e:
                        repo_map[rel_path] = f"Error parsing: {str(e)}"
        
        return repo_map

# Simple test execution
if __name__ == "__main__":
    mapper = RepoMapper()
    print(json.dumps(mapper.generate_map(), indent=2))