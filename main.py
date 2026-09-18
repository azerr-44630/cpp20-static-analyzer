import os
from auto_fixer import AutoFixer

def show_menu():
    print("\n==========================================")
    print("      si-learn-first | C++ Agent")
    print("==========================================")
    print("1. Qovluğu skan et və hesabat yarat (ast_engine.py)")
    print("2. Son skan nəticələrinə avto-düzəliş tətbiq et (auto_fixer.py)")
    print("3. Bütün testləri icra et (memory_test.py)")
    print("4. Son düzəliş təcrübələrinə bax (Agent Memory)")
    print("0. Çıxış")
    print("==========================================")

def main():
    fixer = AutoFixer()
    
    while True:
        show_menu()
        choice = input("Seçiminizi daxil edin (0-4): ").strip()
        
        if choice == "1":
            print("\n[+] Skan edilən fayl: main.cpp")
            issues = fixer.analyzer.analyze_code(open("main.cpp").read(), "main.cpp")
            if issues:
                print(f"[!] {len(issues)} problem aşkarlandı:")
                for i in issues:
                    print(f"    - Sətir {i['line_number']}: {i['old_code']} ({i['problem_type']})")
            else:
                print("[+] Heç bir problem tapılmadı.")
                
        elif choice == "2":
            print("\n[+] Avtomatik düzəliş tətbiq edilir...")
            fixer.fix_file("main.cpp")
            
        elif choice == "3":
            print("\n[+] Yaddaş və məntiq testləri işə salınır...")
            os.system("python3 memory_test.py")
            
        elif choice == "4":
            import sqlite3
            conn = sqlite3.connect("agent_memory.db")
            cursor = conn.cursor()
            cursor.execute("SELECT problem_type, old_code, fix_applied, confidence, timestamp FROM fix_experience")
            rows = cursor.fetchall()
            conn.close()
            
            print("\n--- Agent Təcrübə Bazası (Fix Experience) ---")
            if not rows:
                print("Hələ heç bir təcrübə qeydə alınmayıb.")
            for r in rows:
                print(f"• Xəta: {r[0]} | Köhnə: {r[1]} ➔ Yeni: {r[2]} | İnam: {r[3]} | Vaxt: {r[4]}")
                
        elif choice == "0":
            print("\n[+] Sistemdən çıxılır. Uğurlar!")
            break
        else:
            print("\n[!] Yanlış seçim, yenidən sınayın.")

if __name__ == "__main__":
    main()
