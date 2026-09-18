import os
import re

class CppASTAnalyzer:
    def __init__(self):
        self.issues = []

    def analyze_file(self, file_path):
        file_issues = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for idx, line in enumerate(lines, 1):
                # Xam pointer massiv pattern-i: new T[...]
                if re.search(r'\bnew\s+\w+\s*\[', line):
                    issue = {
                        "file": file_path,
                        "line": idx,
                        "type": "raw_pointer_array",
                        "code": line.strip()
                    }
                    file_issues.append(issue)
                    self.issues.append(issue)
        except Exception as e:
            print(f"  [x] Fayl oxunmadı ({file_path}): {e}")
        return file_issues

    def analyze_directory(self, directory="."):
        self.issues = []
        cpp_extensions = (".cpp", ".cc", ".cxx", ".h", ".hpp")
        for root, dirs, files in os.walk(directory):
            if ".git" in root or "node_modules" in root:
                continue
            for file in files:
                if file.endswith(cpp_extensions):
                    file_path = os.path.join(root, file)
                    self.analyze_file(file_path)
        return self.issues

def scan_code(directory="."):
    analyzer = CppASTAnalyzer()
    issues = analyzer.analyze_directory(directory)
    print(f"\n[AST ENGINE] '{directory}' qovluğunda C++ faylları yoxlanılır...")
    if not issues:
        print("  [✓] Heç bir təhlükəli xam pointer massiv pattern-i tapılmadı.")
    else:
        for issue in issues:
            print(f"  [!] Təhlükəli Pattern ({issue['type']}): {issue['file']}:{issue['line']}")
            print(f"      Kod: {issue['code']}")
        print(f"  [!] Skan başa çatdı. Cəmi {len(issues)} problem tapıldı.")
    return issues

if __name__ == "__main__":
    scan_code()
