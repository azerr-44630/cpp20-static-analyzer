import re
from brain.memory_manager import MemoryManager

class UniversalCodeEngine:
    def __init__(self, db_path="agent_memory.db"):
        self.mm = MemoryManager(db_path)

    def analyze_code(self, code_or_file: str, lang: str = "python"):
        """Kod sətrini və ya faylı həm sintaktik, həm də öyrənilmiş qaydalara əsasən analiz edir."""
        results = []
        
        # Əgər daxil edilən mətn fayl yoludursa, faylı oxuyaq
        code_content = code_or_file
        if not "\n" in code_or_file and (code_or_file.endswith(".py") or code_or_file.endswith(".cpp")):
            try:
                with open(code_or_file, "r", encoding="utf-8") as f:
                    code_content = f.read()
            except FileNotFoundError:
                return [{"status": "ERROR", "details": f"Fayl tapılmadı: {code_or_file}"}]

        # 1. Sintaksis Analizi (Python üçün)
        if lang.lower() == "python":
            try:
                compile(code_content, "<string>", "exec")
                results.append({"status": "CLEAN", "details": "Python kodu sintaktik olaraq düzgündür."})
            except SyntaxError as e:
                results.append({"status": "SYNTAX_ERROR", "details": f"Sintaksis xətası: {e}"})

        # 2. V2 Memory Engine-dən Öyrənilmiş Qaydaların Yoxlanılması
        rules = self.mm.get_rules()
        for trigger, risk_cat, confidence in rules:
            if trigger.lower() in code_content.lower():
                results.append({
                    "status": "RULE_VIOLATION",
                    "pattern": trigger,
                    "risk_category": risk_cat,
                    "confidence": confidence,
                    "details": f"Öyrənilmiş təhlükəli pattern aşkar edildi: '{trigger}' -> {risk_cat}"
                })

        return results
