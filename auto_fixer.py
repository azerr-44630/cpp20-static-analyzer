import sqlite3
import re
import os
import sys

DB_NAME = "agent_memory.db"

class CppAutoFixer:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path

    def ensure_memory_header(self, code: str) -> str:
        """Koda `#include <memory>` başlığını əlavə edir."""
        if "#include <memory>" not in code:
            if "#include" in code:
                code = re.sub(r"(#include\s+<[^>]+>\n)", r"\1#include <memory>\n", code, count=1)
            else:
                code = "#include <memory>\n" + code
        return code

    def fix_virtual_destructor(self, code: str) -> str:
        """Polimorfik və ya virtual metodu olan bütün siniflərdə destruktorlara `virtual` əlavə edir."""
        def process_class(match):
            class_decl = match.group(1)
            class_body = match.group(2)
            
            # Sinifdə virtual funksiya varsa və ya başqa sinifdən miras alınıbsa
            if "virtual" in class_body or ":" in class_decl:
                def replace_destructor(d_match):
                    indent = d_match.group(1)
                    dest_sig = d_match.group(2)
                    full_str = d_match.group(0)
                    if "virtual" not in full_str:
                        return f"{indent}virtual {dest_sig}"
                    return full_str

                class_body = re.sub(
                    r"([ \t]*)(~[A-Za-z0-9_]+\s*\([^)]*\))",
                    replace_destructor,
                    class_body
                )
            return f"{class_decl}{class_body}"

        pattern = r"(class\s+[A-Za-z0-9_]+[^{]*\{)([\s\S]*?\};)"
        return re.sub(pattern, process_class, code)

    def fix_raw_pointers_and_delete(self, code: str) -> str:
        """Raw pointer və manual delete əməliyyatlarını std::make_unique ilə əvəz edir."""
        code = re.sub(
            r"(\w+)\s*=\s*new\s+(\w+)\[(.*?)\];",
            r"\1 = std::make_unique<\2[]>(\3);",
            code
        )
        code = re.sub(
            r"(\w+)\s*=\s*new\s+(\w+)\((.*?)\);",
            r"\1 = std::make_unique<\2>(\3);",
            code
        )
        code = re.sub(r"^\s*delete\[\]\s+\w+;\n?", "", code, flags=re.MULTILINE)
        code = re.sub(r"^\s*delete\s+\w+;\n?", "", code, flags=re.MULTILINE)
        return code

    def fix_c_style_memory(self, code: str) -> str:
        """malloc/calloc/free əməliyyatlarını RAII və std::make_unique ilə əvəz edir."""
        code = re.sub(
            r"(\w+)\s*=\s*(?:\(\s*\w+\s*\*\s*\))?\s*malloc\s*\(\s*(.*?)\s*\*\s*sizeof\s*\(\s*(\w+)\s*\)\s*\);",
            r"\1 = std::make_unique<\3[]>(\2);",
            code
        )
        code = re.sub(
            r"(\w+)\s*=\s*(?:\(\s*\w+\s*\*\s*\))?\s*malloc\s*\(\s*sizeof\s*\(\s*(\w+)\s*\)\s*\);",
            r"\1 = std::make_unique<\2>();",
            code
        )
        code = re.sub(r"^\s*free\s*\(\s*\w+\s*\);\n?", "", code, flags=re.MULTILINE)
        return code

    def fix_c_style_casts(self, code: str) -> str:
        """C-style cast əməliyyatlarını static_cast ilə əvəz edir."""
        primitive_types = r"int|float|double|char|bool|size_t|uint32_t|int32_t|long|short"
        code = re.sub(
            rf"\(\s*({primitive_types})\s*\)\s*([a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*|\-\>[a-zA-Z_]\w*)?)",
            r"static_cast<\1>(\2)",
            code
        )
        return code

    def apply_fixes_to_file(self, file_path: str):
        if not os.path.exists(file_path):
            print(f"[!] Fayl tapılmadı: {file_path}")
            return False

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            original_code = f.read()

        modified_code = original_code
        modified_code = self.ensure_memory_header(modified_code)
        modified_code = self.fix_virtual_destructor(modified_code)
        modified_code = self.fix_raw_pointers_and_delete(modified_code)
        modified_code = self.fix_c_style_memory(modified_code)
        modified_code = self.fix_c_style_casts(modified_code)

        if modified_code != original_code:
            backup_path = file_path + ".bak"
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(original_code)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_code)

            print(f"[+] Refaktor uğurla tətbiq edildi: {file_path}")
            print(f"[+] Ehtiyat nüsxə yaradıldı: {backup_path}")
            return True
        else:
            print(f"[*] Düzəliş edilməli xəta tapılmadı və ya fayl artıq yenilənib: {file_path}")
            return False

    def fix_latest_scan_results(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT file_path FROM scan_results WHERE scan_time = (SELECT MAX(scan_time) FROM scan_results)")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("[!] Bazada düzəldilməli fayl tapılmadı.")
            return

        for (file_path,) in rows:
            self.apply_fixes_to_file(file_path)

if __name__ == "__main__":
    fixer = CppAutoFixer()
    if len(sys.argv) > 1:
        fixer.apply_fixes_to_file(sys.argv[1])
    else:
        fixer.fix_latest_scan_results()
