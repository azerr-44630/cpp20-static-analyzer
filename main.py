import sys
from brain.knowledge_engine import KnowledgeEngine
from brain.reasoning_engine import ReasoningEngine
from brain.cyber_defense_engine import CyberDefenseEngine
from brain.universal_code_engine import UniversalCodeEngine
from brain.local_nlp_engine import LocalNLPEngine
from brain.conversation_engine import DynamicConversationEngine
from brain.memory_manager import MemoryManager
from brain.learning_engine import LearningEngine

def print_summary_trace(steps):
    """Görsellerdeki Düşünme / Summary akışını terminalde şık şekilde çizer."""
    print("\n   ┌─── [ Summary / Düşünce Akışı ]")
    for i, step in enumerate(steps):
        is_last = (i == len(steps) - 1)
        prefix = "   └──" if is_last else "   ├──"
        
        if step["type"] == "SEARCH":
            icon = "🌐 Searched for:"
        else:
            icon = "•"
            
        print(f"{prefix} {icon} {step['text']}")
    print("   " + "─" * 45 + "\n")

def main():
    print("=" * 65)
    print("   [ SI-LEARN-FIRST | Advanced Thinking & Summary Mode ]")
    print("=" * 65)
    print(" Düşünce izleme modu aktivdir. Çıkış: 'exit'")
    print("-" * 65)

    ke = KnowledgeEngine("agent_memory.db")
    mm = MemoryManager("agent_memory.db")
    le = LearningEngine(mm)
    re = ReasoningEngine(ke)
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

            # 1. NLP & Intent Parsing
            intent_data = nlp.parse_intent(user_input)

            # 2. Görseldeki gibi Düşünme Adımlarını (Summary) Oluştur ve Bas
            thought_steps = re.generate_thought_trace(user_input, intent_data)
            print_summary_trace(thought_steps)

            # 3. Öğretme (TEACH) İşlemi
            if "öyrən:" in user_input.lower() or "təhlükəli" in user_input.lower():
                learn_res = le.process_teach_input(user_input)
                if learn_res["status"] == "LEARNED":
                    print(f"Agent [ÖYRƏNDİ] > {learn_res['rule']} (İnam Balı: {learn_res['confidence']})\n")
                    mm.log_experience(user_input, "RULE_LEARNED", 1.0)
                    continue

            # 4. Universal Code Engine Kontrolü
            analysis_results = uce.analyze_code(user_input, lang="python")
            has_risk = False
            for res in analysis_results:
                if res["status"] != "CLEAN":
                    has_risk = True
                    print(f"  [UCE RISK] {res.get('details', res)}")

            if has_risk:
                mm.log_experience(user_input, "RULE_VIOLATION_DETECTED", 1.0)
                continue

            # 5. Yanıt Üretimi
            response = conv.generate_dynamic_response(intent_data)
            print(f"Agent > {response}")

        except KeyboardInterrupt:
            print("\nDayandırıldı.")
            break

if __name__ == "__main__":
    main()
