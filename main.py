import sys
from core.ai_agent import AIAgent

def main():
    print("=" * 55)
    print("🛡️  SI-GUARD (Micro-LLM & Cyber Security Agent) Aktivdir")
    print("Sual verin və ya əmr daxil edin. Çıxış üçün 'exit' yazın.")
    print("=" * 55)
    
    agent = AIAgent()

    while True:
        try:
            user_input = input("\nSI-GUARD > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 SI-GUARD dayandırıldı.")
                break

            response = agent.process_command(user_input)
            print(f"\n{response}")

        except (KeyboardInterrupt, EOFError):
            print("\n👋 Çıxış edildi.")
            break
        except Exception as e:
            print(f"\n❌ Xəta baş verdi: {e}")

if __name__ == "__main__":
    main()
