import sys
from ast_engine import CppASTAnalyzer
from auto_fixer import AutoFixer
from knowledge_graph import V6KnowledgeGraph
from inference_engine import V7InferenceEngine
from experience_learner import V8ExperienceLearner
from risk_decision_engine import V9RiskDecisionEngine

class V10NaturalLanguageInterface:
    def __init__(self, db_path="agent_memory.db"):
        self.db_path = db_path
        self.analyzer = CppASTAnalyzer()
        self.fixer = AutoFixer(db_path)
        self.kg = V6KnowledgeGraph(db_path)
        self.inference = V7InferenceEngine(db_path)
        self.learner = V8ExperienceLearner(db_path)
        self.risk_engine = V9RiskDecisionEngine(db_path)

    def interpret_command(self, text: str):
        text = text.lower()
        print(f"\n[V10 NLI AGENT] Sorğu emal olunur: '{text}'")
        print("-" * 50)

        if "salam" in text:
            print("  [i] Aleykum salam! C++ statik analizatoru hazırdır. Necə kömək edə bilərəm?")
        elif "analiz" in text or "scan" in text or "yoxla" in text:
            issues = self.analyzer.analyze_directory(".")
            print(f"  [✓] Skan tamamlandı. Tapılan problem sayısı: {len(issues)}")
            for i in issues:
                print(f"      - {i['file']}:{i['line']} -> {i['type']}")
        elif "düzəlt" in text or "fix" in text or "refaktor" in text:
            self.fixer.run_fixes(".")
            print("  [✓] Avtomatik düzəliş əməliyyatı icra olundu.")
        elif "bilik" in text or "qraf" in text or "graph" in text:
            self.kg.explain_impact("raw_pointer_array")
        elif "risk" in text or "qərar" in text or "decision" in text:
            self.risk_engine.evaluate_and_decide(".")
        elif "təcrübə" in text or "learning" in text or "öyrən" in text:
            self.learner.analyze_experiences()
        elif "kömək" in text or "komek" in text or "help" in text or "yardım" in text:
            print("  [i] İstifadə edə biləcəyiniz təbii dil əmrləri:")
            print("      - 'kodu analiz et və ya yoxla'")
            print("      - 'xətaları düzəlt'")
            print("      - 'bilik qrafını göstər'")
            print("      - 'risk qiymətləndirməsi apar'")
            print("      - 'keçmiş təcrübələri təhlil et'")
        else:
            print("  [?] Bu sorğunu başa düşmədim. 'kömək' yazaraq əmrləri görə bilərsiniz.")

    def interactive_chat(self):
        print("\n[V10 NATURAL LANGUAGE INTERFACE - CHAT MODE]")
        print("Agentlə təbii dildə ünsiyyətə başlaya bilərsiniz. Çıxış üçün 'exit' yazın.")
        print("=" * 60)
        while True:
            prompt = input("\nSən (User) > ").strip()
            if prompt.lower() in ["exit", "çıxış", "qayıt"]:
                break
            if prompt:
                self.interpret_command(prompt)

if __name__ == "__main__":
    nli = V10NaturalLanguageInterface()
    nli.interactive_chat()
