import os
import sqlite3
import re
from ast_engine import CppASTAnalyzer

DB_NAME = "agent_memory.db"

class AutoFixer:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fix_experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                line_number INTEGER NOT NULL,
                original_code TEXT NOT NULL,
                fixed_code TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def fix_file(self, file_path, issues):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            print(f"  [x] Fayl oxunmadı ({file_path}): {e}")
            return

        file_fixed = False
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for issue in issues:
            if issue["file"] != file_path:
                continue
            idx = issue["line"] - 1
            if idx >= len(lines):
                continue
            orig = lines[idx]

            # Xam pointer massivini std::vector-ə keçirən refaktorinq pattern-i
            match = re.search(r'(\w+)\s*\*\s*(\w+)\s*=\s*new\s+(\w+)\s*\[\s*(.*?)\s*\]', orig)
            if match:
                t_type, var_name, elem_type, size_expr = match.groups()
                fixed = f"    std::vector<{elem_type}> {var_name}({size_expr}); // Auto-fixed by V6 Agent\n"
                lines[idx] = fixed
                file_fixed = True

                cursor.execute("""
                    INSERT INTO fix_experience (file_path, line_number, original_code, fixed_code)
                    VALUES (?, ?, ?, ?)
                """, (file_path, issue["line"], orig.strip(), fixed.strip()))
                print(f"  [FIXED] {file_path}:{issue['line']} -> {fixed.strip()}")

        if file_fixed:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            except Exception as e:
                print(f"  [x] Fayla yazılmadı ({file_path}): {e}")

        conn.commit()
        conn.close()

    def run_fixes(self, directory="."):
        analyzer = CppASTAnalyzer()
        issues = analyzer.analyze_directory(directory)
        if not issues:
            print("  [✓] Düzəliş ediləcək problem tapılmadı.")
            return

        files_with_issues = set(i["file"] for i in issues)
        for fp in files_with_issues:
            self.fix_file(fp, issues)

def apply_auto_fix(directory="."):
    fixer = AutoFixer()
    fixer.run_fixes(directory)

def show_fix_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, file_path, line_number, original_code, fixed_code, timestamp FROM fix_experience")
    rows = cursor.fetchall()
    conn.close()

    print("\n[FIX EXPERIENCE HISTORY]")
    print("=" * 60)
    if not rows:
        print("  [!] Hələlik heç bir düzəliş qeydə alınmayıb.")
        return

    for row in rows:
        print(f" ID: {row[0]} | Fayl: {row[1]}:{row[2]} | Vaxt: {row[5]}")
        print(f"   Köhnə: {row[3]}")
        print(f"   Yeni : {row[4]}")
        print("-" * 60)

if __name__ == "__main__":
    apply_auto_fix()
