import os
import sys
import sqlite3
from ast_engine import DeterministicAnalyzer
from auto_fixer import CppAutoFixer
from add_rules import add_new_rules

TEST_FILE = "unit_test_target.cpp"

TEST_CPP_CODE = """#include <iostream>
#include <cstdio>
#include <cstring>
#include <stdexcept>

class BaseClass {
public:
    BaseClass() {}
    ~BaseClass() {} // Qayda: Non-virtual destructor
    virtual void doSomething() {}
};

class DerivedClass : public BaseClass {
private:
    int* raw_ptr;
    char* buffer;
public:
    DerivedClass() {
        raw_ptr = new int[50]; // Qayda: Raw Pointer
        buffer = (char*)malloc(100 * sizeof(char)); // Qayda: C-Style Memory Allocation
    }

    ~DerivedClass() {
        delete[] raw_ptr; // Qayda: Manual Delete
        free(buffer); // Qayda: C-Style Free
    }

    void doSomething() { // Qayda: Polymorphic Safety (Missing override)
        double temp = 98.6;
        int speed = (int)temp; // Qayda: Unsafe Type Casting

        char dest[20];
        strcpy(dest, "test_buffer"); // Qayda: Buffer Overflow
    }
};

void handleException() {
    try {
        throw std::runtime_error("System error");
    } catch (std::exception e) { // Qayda: Exception Slicing
        std::cout << e.what() << std::endl;
    }
}
"""

def run_test_suite():
    print("================ 🧪 C++ STATIC ANALYSIS & AUTO-FIX TEST SUITE ================\n")
    
    # 0. Qaydaların aktivliyini təmin etmək
    add_new_rules()

    # Test faylını diskə yazmaq
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write(TEST_CPP_CODE)
    
    # 1. AST Skaner Testi
    print("[STEP 1/3] Static Analyzer (ast_engine.py) yoxlanılır...")
    analyzer = DeterministicAnalyzer()
    findings = analyzer.analyze_file(TEST_FILE)
    
    detected_categories = {item["category"] for item in findings}
    print(f"  -> Skaner tərəfindən aşkar edilən zəiflik növləri: {len(detected_categories)}")
    for cat in sorted(detected_categories):
        print(f"     [✓] {cat}")
        
    if len(findings) == 0:
        print("  [X] XƏTA: Skaner zəiflik tapmadı!")
        sys.exit(1)
    print("  -> NƏTİCƏ: AST Skaner Testi KEÇDİ!\n")

    # 2. Auto-Fixer Refaktor Testi
    print("[STEP 2/3] Avto-Düzəldici (auto_fixer.py) işə salınır...")
    fixer = CppAutoFixer()
    fix_applied = fixer.apply_fixes_to_file(TEST_FILE)
    
    if not fix_applied:
        print("  [X] XƏTA: Auto-fixer koda düzəliş etmədi!")
        sys.exit(1)
    
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        fixed_code = f.read()

    # 3. Koda tətbiq edilən transformasiyaların dəqiqliyini yoxlamaq
    print("\n[STEP 3/3] Transformasiya Dəqiqliyi İnspeksiyası:")
    assertions = [
        ("#include <memory>", "#include <memory> başlığı koda daxil edildi"),
        ("virtual ~BaseClass()", "BaseClass destruktoruna 'virtual' əlavə edildi"),
        ("raw_ptr = std::make_unique<int[]>(50);", "new int[] -> std::make_unique<int[]> çevrildi"),
        ("buffer = std::make_unique<char[]>(100);", "malloc() -> std::make_unique<char[]> çevrildi"),
        ("static_cast<int>(temp)", "C-style cast (int)temp -> static_cast<int>(temp) çevrildi"),
    ]

    passed_count = 0
    for code_snippet, label in assertions:
        if code_snippet in fixed_code:
            print(f"  [✓] PASSED: {label}")
            passed_count += 1
        else:
            print(f"  [X] FAILED: {label}")

    # Müvəqqəti test fayllarını təmizləmək
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    if os.path.exists(TEST_FILE + ".bak"):
        os.remove(TEST_FILE + ".bak")

    print(f"\n================ 🎯 TEST İCRA OLUNDU: {passed_count}/{len(assertions)} VERİFİKASİYA KEÇDİ ================")

if __name__ == "__main__":
    run_test_suite()
