import sqlite3

DB_NAME = "agent_memory.db"

def add_new_rules():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS local_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            pattern TEXT NOT NULL,
            severity TEXT NOT NULL,
            issue_desc TEXT NOT NULL,
            fix_template TEXT NOT NULL
        )
    """)

    new_rules = [
        (
            "C-Style Memory Management",
            r"\b(malloc|calloc|realloc|free)\s*\(",
            "HIGH",
            "C-style yaddaş idarəetmə funksiyalarından istifadə C++ obyekt ömrünü və konstruktor/destruktor zəncirini pozur.",
            "std::make_unique, std::make_shared və ya std::vector kimi C++ RAII konteynerləri istifadə edin."
        ),
        (
            "Buffer Overflow Vulnerability",
            r"\b(strcpy|strcat|sprintf|gets)\s*\(",
            "CRITICAL",
            "Sərhəd yoxlaması aparmayan təhlükəsiz C-string funksiyaları bufer aşması (Buffer Overflow) zəifliyi yaradır.",
            "std::string, std::string_view və ya snprintf kimi təhlükəsiz alternativlərdən istifadə edin."
        ),
        (
            "Unsafe Type Casting",
            r"\((?:int|float|double|char|void\*?|[A-Z]\w*\*?)\)\s*[a-zA-Z0-9_]+",
            "MEDIUM",
            "C-style cast növlərin idarə olunmasını zəiflədir və tipi gizli şəkildə dəyişərək runtime xətalarına səbəb olur.",
            "C++ explicit cast-lardan istifadə edin: static_cast, reinterpret_cast və ya const_cast."
        ),
        (
            "Polymorphic Safety",
            r"virtual\s+\w+\s+\w+\s*\([^)]*\)\s*(?!.*override)\s*;",
            "MEDIUM",
            "Törəmə sinifdə virtual funksiya elan edilərkən 'override' açar sözü buraxılıb.",
            "İmzanın uyğunluğunu təmin etmək və metod gizlənməsinin qarşısını almaq üçün funksiyanın sonuna 'override' əlavə edin."
        ),
        (
            "Exception Slicing",
            r"catch\s*\(\s*(?:std::)?exception\s+\w+\s*\)",
            "MEDIUM",
            "İstisnanı qiymətə görə tutmaq (catch by value) 'Object Slicing' yaradır və polimorfik istisna təfərrüatlarını silir.",
            "İstisnanı konstant referansla tutun: catch (const std::exception& e)"
        )
    ]

    added_count = 0
    for category, pattern, severity, issue_desc, fix_template in new_rules:
        cursor.execute("SELECT id FROM local_rules WHERE category = ? AND pattern = ?", (category, pattern))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO local_rules (category, pattern, severity, issue_desc, fix_template)
                VALUES (?, ?, ?, ?, ?)
            """, (category, pattern, severity, issue_desc, fix_template))
            added_count += 1

    conn.commit()
    conn.close()
    print(f"[+] {added_count} yeni C++ təhlükəsizlik qaydası 'local_rules' cədvəlinə uğurla əlavə olundu.")

if __name__ == "__main__":
    add_new_rules()
