import sqlite3
import re
import os
import sys
from datetime import datetime

DB_NAME = "agent_memory.db"
CPP_EXTENSIONS = {".cpp", ".hpp", ".c", ".h", ".cc", ".cxx"}

class CppTokenizer:
    @staticmethod
    def sanitize_code(code: str) -> str:
        code = re.sub(r"//.*", "", code)
        code = re.sub(r"/\*[\s\S]*?\*/", "", code)
        code = re.sub(r'".*?"', '""', code)
        return code

class DeterministicAnalyzer:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self.tokenizer = CppTokenizer()
        self._init_db_schema()

    def _init_db_schema(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_time TEXT NOT NULL,
                file_path TEXT NOT NULL,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                issue_desc TEXT NOT NULL,
                fix_template TEXT NOT NULL,
                count INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def get_rules(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT category, pattern, severity, issue_desc, fix_template FROM local_rules")
        rules = cursor.fetchall()
        conn.close()
        return rules

    def analyze_file(self, file_path: str, rules=None):
        if rules is None:
            rules = self.get_rules()

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
        except Exception as e:
            print(f"[!] Fayl oxunarkən xəta yarandı ({file_path}): {e}")
            return []

        clean_code = self.tokenizer.sanitize_code(code)
        findings = []

        for category, pattern, severity, issue_desc, fix_template in rules:
            matches = re.findall(pattern, clean_code)
            if matches:
                findings.append({
                    "file_path": file_path,
                    "category": category,
                    "severity": severity,
                    "issue": issue_desc,
                    "fix": fix_template,
                    "count": len(matches)
                })
        return findings

    def save_findings_to_db(self, findings, scan_time):
        if not findings:
            return
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        records = [
            (
                scan_time,
                item["file_path"],
                item["category"],
                item["severity"],
                item["issue"],
                item["fix"],
                item["count"]
            )
            for item in findings
        ]

        cursor.executemany("""
            INSERT INTO scan_results (scan_time, file_path, category, severity, issue_desc, fix_template, count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, records)

        conn.commit()
        conn.close()

    def generate_markdown_report(self, output_file="scan_report.md", target_scan_time=None):
        """SQLite-dəki skan nəticələrindən Markdown hesabatı generasiya edir."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if target_scan_time is None:
            cursor.execute("SELECT scan_time FROM scan_results ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if not row:
                print("[!] Hesabat üçün bazada heç bir skan nəticəsi tapılmadı.")
                conn.close()
                return
            target_scan_time = row[0]

        cursor.execute("""
            SELECT file_path, category, severity, issue_desc, fix_template, count
            FROM scan_results
            WHERE scan_time = ?
        """, (target_scan_time,))
        results = cursor.fetchall()
        conn.close()

        if not results:
            print(f"[!] '{target_scan_time}' seansı üçün məlumat tapılmadı.")
            return

        md = []
        md.append("# 🛡️ AST Təhlükəsizlik və Yaddaş Təhlili Hesabatı\n")
        md.append(f"- **Skan Tarixi:** `{target_scan_time}`")
        md.append(f"- **Aşkar Edilən Problem Sayı:** `{len(results)}`")
        md.append("\n---\n")
        md.append("## 📊 Nəticələrin İcmal Cədvəli\n")
        md.append("| Dərəcə | Kateqoriya | Fayl | Halların Sayı |")
        md.append("|---|---|---|---|")

        for file_path, category, severity, issue_desc, fix_template, count in results:
            md.append(f"| **{severity}** | {category} | `{file_path}` | {count} |")

        md.append("\n---\n")
        md.append("## 🔍 Detallı Xətalar və Tövsiyə Olunan Həllər\n")

        for idx, (file_path, category, severity, issue_desc, fix_template, count) in enumerate(results, 1):
            md.append(f"### {idx}. [{severity}] {category}")
            md.append(f"- **Fayl:** `{file_path}`")
            md.append(f"- **Aşkar olunma sayısı:** {count}")
            md.append(f"- **Problem:** {issue_desc}")
            md.append(f"- **Tövsiyə olunan həll:**\n```cpp\n{fix_template}\n```\n")

        report_content = "\n".join(md)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"[+] Markdown hesabatı uğurla yaradıldı: {os.path.abspath(output_file)}")

    def scan_directory(self, target_dir="."):
        abs_target = os.path.abspath(target_dir)
        print(f"[*] Multi-file skan başladı: {abs_target}")
        
        rules = self.get_rules()
        all_findings = []
        scanned_files_count = 0
        scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for root, _, files in os.walk(target_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in CPP_EXTENSIONS:
                    file_path = os.path.join(root, file)
                    scanned_files_count += 1
                    findings = self.analyze_file(file_path, rules)
                    if findings:
                        all_findings.extend(findings)

        print(f"[+] Skan edilən C/C++ faylı: {scanned_files_count}")
        print(f"[+] Tapılan ümumi zəiflik: {len(all_findings)}")

        if all_findings:
            self.save_findings_to_db(all_findings, scan_time)
            print(f"[+] Nəticələr '{self.db_path}' bazasına yazıldı.")
            self.generate_markdown_report(output_file="scan_report.md", target_scan_time=scan_time)

        return all_findings, scanned_files_count

if __name__ == "__main__":
    analyzer = DeterministicAnalyzer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        analyzer.generate_markdown_report()
    else:
        target_path = sys.argv[1] if len(sys.argv) > 1 else "."
        analyzer.scan_directory(target_path)
