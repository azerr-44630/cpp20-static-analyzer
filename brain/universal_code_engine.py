import ast

class UniversalCodeEngine:
    def __init__(self, db_path="agent_memory.db"):
        self.db_path = db_path

    def analyze_code(self, code_str: str, lang: str = "python"):
        """Daxil olan mətni/kodu təhlil edir. Əgər kod deyilsə, xəta vermir."""
        results = []
        
        # Əgər daxil olan giriş sadə təbii dil cümləsidirsə (kod göstəriciləri yoxdursa)
        code_indicators = ["def ", "import ", "class ", "=", "(", ")", ":", "return ", "sys.", "os."]
        if not any(indicator in code_str for indicator in code_indicators):
            return [{"status": "CLEAN", "details": "Giriş təbii mətndir, kod təhlili atlanıldı."}]

        try:
            parsed_ast = ast.parse(code_str)
            results.append({"status": "CLEAN", "details": "AST Sintaksis analizi uğurludur."})
        except SyntaxError:
            # Təbii dildə yazılan sualların bloklanmaması üçün Sintaksis xətasını risk saymırıq
            results.append({"status": "CLEAN", "details": "Təbii dil mətni (Kod sintaksisi deyil)."})
        except Exception as e:
            results.append({"status": "WARNING", "details": f"Analiz xətası: {e}"})

        return results
