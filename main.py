import sys
import os
import subprocess

def show_menu():
    print("================ 🛡️ C++20 OFFLINE AST TOOLKIT ================")
    print("1. Qovluğu skan et və hesabat yarat (ast_engine.py)")
    print("2. Son skan nəticələrinə avto-düzəliş tətbiq et (auto_fixer.py)")
    print("3. Bütün testləri icra et (test_suite.py)")
    print("4. Son skan hesabatına bax (scan_report.md)")
    print("0. Çıxış")
    print("===============================================================")

def main():
    while True:
        show_menu()
        choice = input("Seçiminizi edin (0-4): ").strip()
        if choice == "1":
            path = input("Skan ediləcək qovluq yolu (Varsayılan '.'): ").strip() or "."
            subprocess.run([sys.executable, "ast_engine.py", path])
        elif choice == "2":
            subprocess.run([sys.executable, "auto_fixer.py"])
        elif choice == "3":
            subprocess.run([sys.executable, "test_suite.py"])
        elif choice == "4":
            if os.path.exists("scan_report.md"):
                subprocess.run(["cat", "scan_report.md"])
            else:
                print("[!] Hesabat faylı (scan_report.md) tapılmadı.")
        elif choice == "0":
            print("[+] Çıxış edilir.")
            break
        else:
            print("[!] Yanlış seçim!")
        print("\n")

if __name__ == "__main__":
    main()
