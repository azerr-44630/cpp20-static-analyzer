import sqlite3

DB_NAME = "agent_memory.db"

def add_c20_rules():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    c20_rules = [
        (
            "Modern C++20 Span",
            r"\b[a-zA-Z_]\w*\s*\*\s*[a-zA-Z_]\w*\s*,\s*(?:size_t|int|unsigned|std::size_t)\s+[a-zA-Z_]\w*",
            "MEDIUM",
            "Funksiyalarda xam göstərici (raw pointer) və ölçü (size) arqumentlərinin ayrılıqda ötürülməsi buffer sərhəd xətalarına səbəb ola bilər.",
            "C++20 std::span<T> konteynerindən istifadə edin: void process(std::span<int> data);"
        ),
        (
            "Modern C++20 Formatting",
            r"\b(sprintf|snprintf)\s*\(",
            "LOW",
            "Köhnə C-style sətri formatlama funksiyaları tip təhlükəsizliyini təmin etmir və bufer aşması riski daşıyır.",
            "C++20 tipli təhlükəsiz std::format funksiyasından istifadə edin: auto s = std::format(\"Val: {}\", val);"
        ),
        (
            "Compile-Time Enforcement",
            r"\bconstexpr\s+(?:int|bool|char|double|float|size_t|auto)\s+[a-zA-Z_]\w*\s*\(",
            "LOW",
            "constexpr funksiyaları həmçinin runtime zamanı icra oluna bilər. Mütləq compile-time icrası tələb olunan hallar mövcuddur.",
            "Funksiyanın yalnız kompilyasiya zamanı işləməsini tətbiq etmək üçün C++20 consteval (immediate function) istifadə edin: consteval int get_val() { return 42; }"
        )
    ]

    added_count = 0
    for category, pattern, severity, issue_desc, fix_template in c20_rules:
        cursor.execute("SELECT id FROM local_rules WHERE category = ? AND pattern = ?", (category, pattern))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO local_rules (category, pattern, severity, issue_desc, fix_template)
                VALUES (?, ?, ?, ?, ?)
            """, (category, pattern, severity, issue_desc, fix_template))
            added_count += 1

    conn.commit()
    conn.close()
    print(f"[+] {added_count} yeni C++20 qaydası 'local_rules' cədvəlinə uğurla əlavə olundu.")

if __name__ == "__main__":
    add_c20_rules()
