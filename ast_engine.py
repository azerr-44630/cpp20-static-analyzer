import sqlite3
import re
import os

DB_NAME = "agent_memory.db"

class CppASTAnalyzer:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path

    def analyze_code(self, code: str, file_path: str = "main.cpp"):
        issues = []
        lines = code.split("\n")

        # 1. Raw Pointer Array Allocation
        raw_ptr_pattern = r"(\w+)\s*\*\s*(\w+)\s*=\s*new\s+(\w+)\s*\[\s*(.*?)\s*\];"
        for line_idx, line in enumerate(lines, 1):
            match = re.search(raw_ptr_pattern, line)
            if match:
                ptr_type, var_name, elem_type, size = match.groups()
                issues.append({
                    "file_path": file_path,
                    "line_number": line_idx,
                    "problem_type": "raw_pointer_array",
                    "old_code": match.group(0),
                    "details": {
                        "ptr_type": ptr_type,
                        "var_name": var_name,
                        "elem_type": elem_type,
                        "size": size
                    },
                    "confidence": 0.95
                })

        # 2. C-Style Cast
        c_cast_pattern = r"\(\s*(int|float|double|char|bool|size_t)\s*\)\s*([a-zA-Z_]\w*)"
        for line_idx, line in enumerate(lines, 1):
            match = re.search(c_cast_pattern, line)
            if match:
                target_type, var_name = match.groups()
                issues.append({
                    "file_path": file_path,
                    "line_number": line_idx,
                    "problem_type": "c_style_cast",
                    "old_code": match.group(0),
                    "details": {
                        "target_type": target_type,
                        "var_name": var_name
                    },
                    "confidence": 0.90
                })

        # 3. C-Style Malloc Allocation
        malloc_pattern = r"(\w+)\s*=\s*(?:\(\s*\w+\s*\*\s*\))?\s*malloc\s*\(\s*(.*?)\s*\);"
        for line_idx, line in enumerate(lines, 1):
            match = re.search(malloc_pattern, line)
            if match:
                var_name, size_expr = match.groups()
                issues.append({
                    "file_path": file_path,
                    "line_number": line_idx,
                    "problem_type": "c_style_malloc",
                    "old_code": match.group(0),
                    "details": {
                        "var_name": var_name,
                        "size_expr": size_expr
                    },
                    "confidence": 0.92
                })

        return issues

    def analyze_file(self, file_path: str):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
        return self.analyze_code(code, file_path)

if __name__ == "__main__":
    analyzer = CppASTAnalyzer()
    print("[+] ast_engine.py Agentic Loop strukturuna hazır vəziyyətə gətirildi.")
