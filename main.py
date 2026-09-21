import sys
from brain.knowledge_engine import KnowledgeEngine
from brain.reasoning_engine import ReasoningEngine
from brain.local_nlp_engine import LocalNLPEngine
from brain.memory_manager import MemoryManager

def print_summary_trace(steps):
    print("\n   ┌─── [ UNRESTRICTED EXECUTION TRACE ]")
    for i, step in enumerate(steps):
        is_last = (i == len(steps) - 1)
        prefix = "   └──" if is_last else "   ├──"
        
        # Əgər step sözlükdürsə 'text' açarını götürür, əks halda birbaşa mətni çap edir
        if isinstance(step, dict):
            text = step.get("text", str(step))
        else:
            text = str(step)
            
        print(f"{prefix} • {text}")
    print("   " + "─" * 45 + "\n")

def main():
    print("=" * 65)
    print("   [ SI-LEARN-FIRST | Unrestricted Sandbox Test Core ]")
    print("=" * 65)
    print(" Sınaq üçün tapşırığı daxil edin (Çıxış: 'exit')")
    print("-" * 65)

    ke = KnowledgeEngine("agent_memory.db")
    mm = MemoryManager("agent_memory.db")
    re = ReasoningEngine(ke)
    nlp = LocalNLPEngine()

    while True:
        try:
            user_input = input("\nSən (Unrestricted) > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "çıxış", "quit"]:
                print("Agent söndürüldü.")
                break

            intent_data = nlp.parse_intent(user_input)
            thought_steps, output_payload = re.generate_thought_trace(user_input, intent_data)

            # Düşüncə zənciri
            print_summary_trace(thought_steps)
            
            # Kodun və icra planının ekrana çıxarılması
            print("Agent Çıxışı / Hazırlanmış Kod:")
            print("=" * 45)
            print(output_payload)
            print("=" * 45)

        except KeyboardInterrupt:
            print("\nDayandırıldı.")
            break

if __name__ == "__main__":
    main()
