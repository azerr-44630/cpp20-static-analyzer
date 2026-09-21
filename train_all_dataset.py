import sqlite3
from datetime import datetime

dataset = [
    ("CPP_CRYPT", "DPAPI_DECRYPT", "CryptUnprotectData funksiyası Windows altında istifadəçi sessiyasına bağlı şifrələnmiş verilənləri deşifrə etmək üçün istifadə olunur."),
    ("CPP_CRYPT", "DPAPI_ENCRYPT", "CryptProtectData vasitəsilə verilənlərin istifadəçi sessiyasına bağlı təhlükəsiz şifrələnməsi."),
    ("CPP_CRYPT", "DPAPI_ENTROPY", "CryptUnprotectData zamanı əlavə xüsusi açar (Entropy) istifadə edərək təhlükəsizliyin artırılması."),
    ("CPP_MEMORY", "RAII_WRAPPER", "ScopedDataBlob RAII klassı ilə LocalFree avtomatlaşdırılması və yaddaş sızmasının önlənməsi."),
    ("CPP_CRYPT", "BCRYPT_AES_GCM", "BCryptEncrypt funksiyası ilə CNG arxitekturasında müasir AES-256-GCM şifrələmə tətbiqi."),
    ("CPP_IO", "FILE_BINARY_READ", "Faylların bayt massivi kimi oxunub şifrələmə modullarına ötürülməsi."),
    ("CPP_SECURITY", "TOKEN_ELEVATION", "IsCurrentProcessElevated vasitəsilə prosesin admin və ya istifadəçi səlahiyyətinin yoxlanması."),
    ("CPP_SYS", "REGISTRY_BLOB_READ", "Registry dəyərlərindən şifrələnmiş DATA_BLOB oxunması."),
    ("CPP_MEMORY", "SECURE_ZERO_MEMORY", "SecureZeroMemory ilə həssas şifrələrin RAM-dan bərpa olunmaz şəkildə silinməsi."),
    ("CPP_DB", "SQLITE_BLOB_PROCESS", "SQLite bazasındakı BLOB tipli məlumatların deşifrə modullarına yönləndirilməsi."),
    ("CPP_SYS", "FORMAT_MESSAGE_LOG", "GetLastError kodu vasitəsilə Windows sistem xətalarının mətn formatına çevrilməsi.")
]

def train_database():
    conn = sqlite3.connect("agent_memory.db")
    cursor = conn.cursor()

    # Cədvəl yoxdursa yaradırıq, varsa mövcud strukturu saxlayırıq
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            topic TEXT,
            content TEXT,
            confidence REAL,
            created_at TEXT
        )
    """)

    for cat, top, cont in dataset:
        cursor.execute("""
            INSERT INTO facts (category, topic, content, confidence, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (cat, top, cont, 1.0, str(datetime.now())))

    conn.commit()
    conn.close()
    print(f"✅ Toplam {len(dataset)} C++ / Windows API konsepti 'agent_memory.db' bazasına uğurla yazıldı!")

if __name__ == "__main__":
    train_database()
