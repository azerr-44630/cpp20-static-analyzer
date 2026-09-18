import os
import sys
from ast_engine import scan_code
from auto_fixer import apply_auto_fix
from memory_test import V5MemoryTester
from knowledge_graph import V6KnowledgeGraph

def print_menu():
    print("\n" + "="*50)
    print("   [ cpp20-static-analyzer | Agentic CLI v6.0 ]")
    print("="*50)
    print(" 1 -> C++ Kodunu Skan Et (Analyze)")
    print(" 2 -> Avtomatik Düzəliş Tətbiq Et (Auto-Fix & Log)")
    print(" 3 -> V5 İnam Azalması və Konflikt Testi (Memory Engine)")
    print(" 4 -> Keçmiş Düzəliş Təcrübələrini Göstər (fix_experience)")
    print(" 5 -> V6 Knowledge Graph Analizatoru (Zəncirvari Məntiq)")
    print(" 0 -> Çıxış")
    print("="*50)

def main():
    while True:
        print_menu()
        choice = input("Seçiminiz (0-5): ").strip()
        
        if choice == "1":
            print("\n[+] Kod skan edilir...")
            scan_code()
            
        elif choice == "2":
            print("\n[+] Avtomatik düzəlişlər tətbiq edilir...")
            apply_auto_fix()
            
        elif choice == "3":
            print("\n[+] V5 Yaddaş və İnam Mexanizmi işə düşür...")
            tester = V5MemoryTester()
            tester.run_test_cycle()
            
        elif choice == "4":
            print("\n[+] fix_experience cədvəlindəki təcrübələr oxunur...")
            from auto_fixer import show_fix_history
            show_fix_history()
            
        elif choice == "5":
            print("\n[+] V6 Bilik Qrafı Analizi işə düşür...")
            kg = V6KnowledgeGraph()
            target_key = input("Kanalizasiya üçün Root Node daxil edin (məs: raw_pointer_array): ").strip()
            if not target_key:
                target_key = "raw_pointer_array"
            kg.explain_impact(target_key)
            
        elif choice == "0":
            print("\nProqramdan çıxılır. Sağ olun!")
            sys.exit(0)
        else:
            print("\n[!] Yanlış seçim, yenidən cəhd edin.")

if __name__ == "__main__":
    main()
