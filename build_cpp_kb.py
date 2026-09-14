import sqlite3
import json
import os

DB_NAME = "agent_memory.db"

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpp_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_num INTEGER,
            chapter_title TEXT,
            topic TEXT,
            content TEXT,
            best_practice TEXT,
            common_pitfall TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpp_code_examples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_num INTEGER,
            topic TEXT,
            code_snippet TEXT
        )
    ''')
    conn.commit()

def seed_knowledge(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cpp_knowledge")
    if cursor.fetchone()[0] > 0:
        print("[!] Bilik bazası artıq doludur. Yenidən yüklənmədi.")
        return

    knowledge_data = [
        (8, "Class və Obyekt Anlayışı", "Access Specifiers", 
         "public (hər yerdən), private (yalnız class daxilindən), protected (varis olan class-lardan). Class-da default private, struct-da public-dir.",
         "Məlumatları private saxlayaraq enkapsulyasiya edin, çıxışı public metodlarla idarə edin.",
         "Private üzvlərə kənardan birbaşa müraciət etməyə çalışmaq."),
        
        (8, "Class və Obyekt Anlayışı", "this Pointer və Const Metodlar",
         "this pointeri cari obyektin ünvanını saxlayır. const üzv funksiyalar obyektin daxili dəyişənlərini modifier edə bilməz.",
         "Obyektin halını (state) dəyişməyən bütün funksiyaları `const` elan edin.",
         "Const obyektlər üzərində non-const funksiyaları çağırmağa çalışmaq."),

        (9, "Konstruktorlar, Destruktorlar, RAII", "RAII və Resource Management",
         "Resource Acquisition Is Initialization: Resursu konstruktorda al, destruktorda azad et. Yaddaş sızmalarının qarşısını alır.",
         "Dinamik resurs idarə edərkən Rule of Five tətbiq edin.",
         "Shallow copy nəticəsində Double Free Error xətası."),

        (10, "Varislik (Inheritance)", "Public Varislik və Çağırış Sırası",
         "Public varislik 'is-a' münasibətini ifadə edir. Obyekt yarandıqda əvvəl Base sonra Derived konstruktoru, silindikdə əks sıra işləyir.",
         "Əksər hallarda public varislikdən istifadə edin.",
         "Base class-ın parametrli konstruktorunu initializer list-də çağırmağı unutmaq."),

        (11, "Polimorfizm və Virtual Funksiyalar", "Dinamik Polimorfizm və Virtual Destruktor",
         "virtual keyword run-time polimorfizm təmin edir (vtable/vptr). Base class destruktoru MÜTLƏQ virtual olmalıdır.",
         "Polimorfik baza class-larda destruktoru `virtual ~Base() = default;` elan edin.",
         "Base pointer vasitəsilə törəmə obyekti silərkən virtual destruktor olmaması səbəbindən yaddaş sızması."),

        (12, "Operator Overloading", "Operator Yükləməsi və C++20 Spaceship Operator",
         "Operatorların öz yarattığımız class-lar üçün davranışını təyin edir. C++20 `<=>` operatoru bütün müqayisələri avtomatlaşdırır.",
         "std::ostream `<<` operatorunu overload edərkən friend funksiyadan istifadə edin.",
         "Built-in tiplərin operatorlarını yükləməyə çalışmaq."),

        (13, "Abstraksiya və SOLID Prinsipləri", "SOLID Prinsipləri və C++ İnterfeysləri",
         "Saf virtual funksiyaları (=0) olan class-lar Abstrakt Class/İnterfeysdir. SOLID prinsipləri daxildir.",
         "Kodu genişlənməyə açıq, dəyişikliyə qapalı (Open/Closed) arxitektura ilə qurun.",
         "İstifadə edilməyən metodlarla böyük mono-interfeyslər yaratmaq.")
    ]

    cursor.executemany('''
        INSERT INTO cpp_knowledge (chapter_num, chapter_title, topic, content, best_practice, common_pitfalls)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', knowledge_data)

    code_data = [
        (8, "Access Specifiers", "class BankHesabi {\nprivate:\n    double balans;\npublic:\n    void depozit(double m) { if(m>0) balans+=m; }\n};"),
        (9, "RAII", "class DinamikMassiv {\nprivate:\n    int* ptr;\npublic:\n    DinamikMassiv(size_t s) : ptr(new int[s]) {}\n    ~DinamikMassiv() { delete[] ptr; }\n};"),
        (11, "Virtual Destructor", "class Base {\npublic:\n    virtual ~Base() = default;\n};"),
        (12, "Spaceship Operator", "#include <compare>\nclass Nokte {\npublic:\n    int x, y;\n    auto operator<=>(const Nokte&) const = default;\n};")
    ]

    cursor.executemany('''
        INSERT INTO cpp_code_examples (chapter_num, topic, code_snippet)
        VALUES (?, ?, ?)
    ''', code_data)

    conn.commit()
    print("[+] C++ OOP Dərslik materialı agent_memory.db bazasına uğurla yazıldı.")

class TermuxAIAgentMemory:
    def __init__(self, db_path=DB_NAME):
        self.conn = sqlite3.connect(db_path)
    
    def get_topic_context(self, topic_keywords):
        cursor = self.conn.cursor()
        query = f"%{topic_keywords}%"
        cursor.execute('''
            SELECT chapter_num, chapter_title, topic, content, best_practice, common_pitfalls 
            FROM cpp_knowledge 
            WHERE topic LIKE ? OR content LIKE ?
        ''', (query, query))
        
        results = cursor.fetchall()
        context = ""
        for r in results:
            context += f"\n--- [Fəsil {r[0]}: {r[1]} - {r[2]}] ---\n"
            context += f"Məzmun: {r[3]}\n"
            context += f"Ən yaxşı praktika: {r[4]}\n"
            context += f"Kritik Xəbərdarlıq: {r[5]}\n"
        return context

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    conn = sqlite3.connect(DB_NAME)
    init_db(conn)
    seed_knowledge(conn)
    conn.close()

    memory = TermuxAIAgentMemory()
    print("\n--- AI Prompt üçün Nümunə Kontekst Axtarışı ('Virtual') ---")
    print(memory.get_topic_context("Virtual"))
    memory.close()

