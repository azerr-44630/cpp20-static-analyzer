import sqlite3
import os
from ast_engine import CppASTAnalyzer

DB_NAME = "agent_memory.db"

class AutoFixer:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self.analyzer = CppASTAnalyzer(db_path)
        self._init_fix_table()

    def _init_fix_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fix_experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_type TEXT NOT NULL,
                old_code TEXT NOT NULL,
                fix_applied TEXT NOT NULL,
                compile_success INTEGER DEFAULT 0,
                confidence REAL DEFAULT 0.5,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def fix_file(self, file_path: str):
        if not os.path.exists(file_path):
            print(f"[!] Fayl tapılmadı: {file_path}")
            return False

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        issues = self.analyzer.analyze_code(code, file_path)
        if not issues:
            print("[+] Düzəldiləcək xəta tapılmadı.")
            return False

        modified_code = code
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        fixed_count = 0
        for issue in issues:
            p_type = issue["problem_type"]
            old_code = issue["old_code"]
            details = issue["details"]

            if p_type == "raw_pointer_array":
                elem_type = details["elem_type"]
                var_name = details["var_name"]
                size = details["size"]
                
                new_code_snippet = f"std::vector<{elem_type}> {var_name}({size});"
                if old_code in modified_code:
                    modified_code = modified_code.replace(old_code, new_code_snippet)
                    fixed_count += 1
                    
                    cursor.execute("""
                        INSERT INTO fix_experience (problem_type, old_code, fix_applied, compile_success, confidence)
                        VALUES (?, ?, ?, 1, 0.95)
                    """, (p_type, old_code, new_code_snippet))

        conn.commit()
        conn.close()

        if fixed_count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_code)
            print(f"[SUCCESS] {fixed_count} ədəd xəta avtomatik düzəldildi və yaddaşa yazıldı.")
            return True

        return False

if __name__ == "__main__":
    test_file = "main.cpp"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("""#include <iostream>\n#include <vector>\n\nint main() {\n    int* arr = new int[50];\n    return 0;\n}\n""")
    
    print("--- Düzəlişdən əvvəl main.cpp ---")
    with open(test_file, "r") as f:
        print(f.read())

    fixer = AutoFixer()
    fixer.fix_file(test_file)

    print("--- Düzəlişdən sonra main.cpp ---")
    with open(test_file, "r") as f:
        print(f.read())
