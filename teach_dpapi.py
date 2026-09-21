import sqlite3
from datetime import datetime

def train_agent_dpapi():
    conn = sqlite3.connect("agent_memory.db")
    cursor = conn.cursor()

    # Köhnə uyğunsuz cədvəli silib yenidən düzgün struktursa yaradırıq
    cursor.execute("DROP TABLE IF EXISTS facts")
    
    cursor.execute("""
        CREATE TABLE facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            topic TEXT,
            content TEXT,
            confidence REAL,
            created_at TEXT
        )
    """)

    dpapi_knowledge = [
        ("CPP_SECURITY", "DPAPI_DECRYPT", "CryptUnprotectData funksiyası Windows altında istifadəçi sessiyasına bağlı şifrələnmiş verilənləri deşifrə etmək üçün istifadə olunur."),
        ("CPP_MEMORY", "LOCAL_FREE", "Windows API tərəfindən CryptUnprotectData vasitəsilə ayrılmış DATA_BLOB.pbData yaddaşı LocalFree() funksiyası ilə azad edilməlidir."),
        ("CPP_STRUCTURE", "DATA_BLOB", "DATA_BLOB obyekti cbData (ölçü) və pbData (bayt göstəricisi) sahələrindən ibarət Windows şifrələmə strukturudur.")
    ]

    for category, topic, content in dpapi_knowledge:
        cursor.execute("""
            INSERT INTO facts (category, topic, content, confidence, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (category, topic, content, 1.0, str(datetime.now())))

    conn.commit()
    conn.close()
    print("✅ Cədvəl yeniləndi. DPAPI və C++ yaddaş idarəetmə bilikləri 'agent_memory.db' bazasına uğurla yazıldı!")

if __name__ == "__main__":
    train_agent_dpapi()
