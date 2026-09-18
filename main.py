import sys
from brain.knowledge_engine import KnowledgeEngine
from brain.reasoning_engine import ReasoningEngine
from brain.cyber_defense_engine import CyberDefenseEngine
from brain.universal_code_engine import UniversalCodeEngine
from brain.local_nlp_engine import LocalNLPEngine
from brain.conversation_engine import DynamicConversationEngine

def main():
    print("=" * 65)
    print("   [ SI-LEARN-FIRST | Dynamic Reasoning Brain v6.5 ]")
    print("=" * 65)
    print(" Şablon cavablar ləğv olundu. Agent dinamik düşüncə rejiminə keçdi.")
    print("-" * 65)

    ke = KnowledgeEngine("agent_memory.db")
    re = ReasoningEngine(ke)
    cde = CyberDefenseEngine()
    uce = UniversalCodeEngine()
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

            # 1. NLP & Slot Parsing
            intent_data = nlp.parse_intent(user_input)
            intent = intent_data["intent"]

            # 2. Düşünmə Mərhələsi (Reasoning Execution)
            reasoning_result = re.think_and_deduce()

            # 3. Cavabın Dinamik Sintezi
            response = conv.generate_dynamic_response(intent_data)

            print(f"\n[AGENT DÜŞÜNCƏ PROSESİ]:")
            for t in reasoning_result["thought_process"]:
                print(f"  🧠 {t}")

            print(f"\nAgent > {response}")
            conv.history.append(user_input)

        except KeyboardInterrupt:
            print("\nDayandırıldı.")
            break

if __name__ == "__main__":
    main()
