import sqlite3

DB_NAME = "agent_memory.db"

def setup_rules():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS local_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            pattern TEXT,
            severity TEXT,
            issue_desc TEXT,
            fix_template TEXT
        )
    ''')

    rules = [
        # Virtual Destructor Qaydası
        ("Memory Leak", r"class\s+\w+\s*:[^\{]*public", "HIGH",
         "Polimorfik baza class-da destruktor virtual elan edilməyib.",
         "public:\n    virtual ~ClassName() = default;"),

        # Raw Pointer Allocation Qaydası
        ("Raw Pointer", r"new\s+\w+(\[.*\])?", "MEDIUM",
         "Dinamik yaddaş ayırmaq üçün raw pointer istifadə olunur.",
         "std::unique_ptr və ya std::make_unique istifadə edin."),

        # Copy Assignment & Double Free Qaydası
        ("Rule of 5", r"class\s+\w+[\s\S]*int\*\s+\w+;", "HIGH",
         "Dinamik resurs saxlayan sinifdə Rule of Five reallaşdırılmalıdır.",
         "Copy Constructor və Assignment Operator-da Deep Copy yazılmalıdır.")
    ]

    cursor.executemany('''
        INSERT INTO local_rules (category, pattern, severity, issue_desc, fix_template)
        VALUES (?, ?, ?, ?, ?)
    ''', rules)

    conn.commit()
    conn.close()
    print("[+] Lokal təhlil qaydaları `agent_memory.db` faylına yazıldı.")

if __name__ == "__main__":
    setup_rules()

