import os
import sys

# Ana kataloqdan ast_engine-i import edirik
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from ast_engine import CppASTAnalyzer
except ImportError:
    CppASTAnalyzer = None

class UniversalCodeEngine:
    def __init__(self):
        self.cpp_engine = CppASTAnalyzer() if CppASTAnalyzer else None

    def analyze_code(self, code_or_dir: str, language: str):
        lang = language.lower()
        print(f"\n[UNIVERSAL CODE ENGINE] Dil: {lang.upper()} | Analiz başladıldı...")

        if lang in ["cpp", "c++"]:
            if self.cpp_engine:
                return self.cpp_engine.analyze_directory(code_or_dir)
            return "C++ AST Engine tapılmadı."
            
        elif lang == "python":
            # Python üçün daxili AST analizi
            import ast
            try:
                ast.parse(code_or_dir)
                return [{"status": "CLEAN", "details": "Python kodu sintaktik olaraq düzgündür."}]
            except SyntaxError as e:
                return [{"status": "ERROR", "details": f"Python Sintaksis Xətası: {e}"}]

        elif lang in ["javascript", "js", "bash", "go", "rust"]:
            return [{"status": "NOT_IMPLEMENTED", "details": f"{lang} üçün parser hələ inteqrasiya olunub."}]

        return []
