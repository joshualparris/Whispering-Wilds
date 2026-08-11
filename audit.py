import os
import ast

def audit():
    tests_dir = "tests/e2e"
    failed = False
    
    for fname in os.listdir(tests_dir):
        if not fname.endswith(".py"):
            continue
            
        path = os.path.join(tests_dir, fname)
        with open(path, "r") as f:
            content = f.read()
            
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module in ["engine.game", "engine.state"]:
                    for n in node.names:
                        if n.name in ["GameEngine", "GameState"]:
                            print(f"FAIL: {fname} imports {n.name}")
                            failed = True
            elif isinstance(node, ast.Import):
                for n in node.names:
                    if "GameEngine" in n.name or "GameState" in n.name:
                        print(f"FAIL: {fname} imports {n.name}")
                        failed = True
                        
            # ANY while loop is an unbounded loop in our test runner
            if isinstance(node, ast.While):
                print(f"FAIL: {fname} contains 'while' loop")
                failed = True
                    
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    print(f"FAIL: {fname} {node.name} contains only 'pass'")
                    failed = True
                    
        if "assert" not in content and "expect" not in content:
            print(f"FAIL: {fname} contains no assertion")
            failed = True
            
        if "/home/josh/" in content:
            print(f"FAIL: {fname} uses /home/josh/")
            failed = True
            
    if failed:
        print("Audit failed.")
        exit(1)
    else:
        print("Audit passed.")

if __name__ == "__main__":
    audit()
