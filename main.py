import sys
from brain.knowledge_engine import KnowledgeEngine
from brain.reasoning_engine import ReasoningEngine
from brain.cyber_defense_engine import CyberDefenseEngine
from brain.universal_code_engine import UniversalCodeEngine
from brain.local_nlp_engine import LocalNLPEngine
from brain.conversation_engine import DynamicConversationEngine
from brain.memory_manager import MemoryManager
from brain.learning_engine import LearningEngine

def main():
    print("=" * 65)
    print("   [ SI-LEARN-FIRST | V2 Self-Learning & Universal Code Engine ]")
    print("=" * 65)
    print(" Sistem aktivdir. Çıxış üçün 'exit' yazın.")
    print("-" * 65)

    ke = KnowledgeEngine("agent_memory.db")
    mm = MemoryManager("agent_memory.db")
    le = LearningEngine(mm)
    re = ReasoningEngine(ke)
    cde = CyberDefenseEngine()
    uce = UniversalCodeEngine("agent_memory.db")
    nlp = LocalNLPEngine()
    conv = DynamicConversationEngine("agent_memory.db")

    while True:
        try:
            user_input = input("\nSən (User) > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "çıxış", "quit"]:
                print("Agent söndürüldü.")
                break

            # 1. Öyrətmə (TEACH) yoxlanışı
            if "öyrən:" in user_input.lower() or "təhlükəli" in user_input.lower():
                learn_res = le.process_teach_input(user_input)
                if learn_res["status"] == "LEARNED":
                    print(f"Agent [ÖYRƏNDİ] > {learn_res['rule']} (İnam Balı: {learn_res['confidence']})")
                    mm.log_experience(user_input, "RULE_LEARNED", 1.0)
                    continue

            # 2. Universal Code Engine ilə Kod Analizi və Öyrənilmiş Qaydaların Yoxlanışı
            analysis_results = uce.analyze_code(user_input, lang="python")
            has_risk = False
            for res in analysis_results:
                if res["status"] != "CLEAN":
                    has_risk = True
                    print(f"  [UCE UYARI] Status: {res['status']} | Detal: {res.get('details', res)}")

            if has_risk:
                mm.log_experience(user_input, "RULE_VIOLATION_DETECTED", 1.0)
                continue

            # 3. Standart NLP & Dinamik Cavab
            intent_data = nlp.parse_intent(user_input)
            response = conv.generate_dynamic_response(intent_data)
            print(f"Agent          > {response}")

        except KeyboardInterrupt:
            print("\nDayandırıldı.")
            break

if __name__ == "__main__":
    main()
