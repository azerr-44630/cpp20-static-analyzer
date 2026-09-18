import sqlite3
from ast_engine import CppASTAnalyzer
from knowledge_graph import V6KnowledgeGraph

DB_NAME = "agent_memory.db"

class V7InferenceEngine:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self.kg = V6KnowledgeGraph(db_path)

    def run_inference(self, directory="."):
        analyzer = CppASTAnalyzer()
        issues = analyzer.analyze_directory(directory)

        print("\n[V7 RULE-BASED INFERENCE ENGINE]")
        print("=" * 60)

        if not issues:
            print("  [✓] Analiz üçün heç bir problem (fakt) tapılmadı.")
            return []

        inferences = []

        for issue in issues:
            issue_type = issue["type"]
            file_loc = f"{issue['file']}:{issue['line']}"
            
            # Bilik qrafından həmin fakt üzrə əlaqələri çəkirik
            traversal = self.kg.traverse_graph(issue_type, max_depth=2)
            
            # Bağlı qovşaqları analiz edirik
            connected_nodes = {t["to"] for t in traversal}
            
            # IF-THEN Qaydaları (Rule Deductions)
            
            # Qayda 1: Raw pointer + manual memory management -> Yüksək Resurs Sızması Riski
            if issue_type == "raw_pointer_array" and "manual_memory_management" in connected_nodes:
                inferences.append({
                    "location": file_loc,
                    "rule_id": "RULE_V7_01",
                    "severity": "CRITICAL",
                    "inference": "Kodda xam pointer massivi var və əl ilə yaddaş idarəetməsi tələb olunur.",
                    "risk": "İstisna (exception) baş verdikdə delete[] ötürüləcək və YADDAŞ SIZMASI olacaq.",
                    "action": "Təcili RAII (std::vector) strukturuna refaktor olunmalıdır."
                })

            # Qayda 2: Exception safety riski varsa -> Təhlükəsizlik cəriməsi
            if "exception_unsafe" in connected_nodes:
                inferences.append({
                    "location": file_loc,
                    "rule_id": "RULE_V7_02",
                    "severity": "WARNING",
                    "inference": "Mövcud struktur Exception-Safe deyil.",
                    "risk": "Çalışma zamanı (runtime) gözlənilməz kəsilmələr və resurs bloklanması.",
                    "action": "Avtomatik destruktor dəstəkli smart-pointer və ya standart konteyner istifadə edin."
                })

        # Çıxarılan nəticələrin nümayişi
        print(f" Cəmi çıxarılan dinamik nəticə sayısı: {len(inferences)}\n")
        for idx, inf in enumerate(inferences, 1):
            print(f" [{idx}] Qayda ID: {inf['rule_id']} | Səviyyə: [{inf['severity']}]")
            print(f"     Məkan : {inf['location']}")
            print(f"     Nəticə: {inf['inference']}")
            print(f"     Risk  : {inf['risk']}")
            print(f"     Qərar : {inf['action']}")
            print("-" * 60)

        return inferences

if __name__ == "__main__":
    engine = V7InferenceEngine()
    engine.run_inference()
