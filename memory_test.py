import sqlite3

DB_NAME = "agent_memory.db"

class V5MemoryTester:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_name TEXT UNIQUE,
                description TEXT,
                category TEXT DEFAULT 'general'
            )
        """)
        conn.commit()
        conn.close()

    def calculate_confidence(self, steps, has_conflict=False):
        """
        V5 Confidence Decay alqoritmi:
        - Başlanğıc inam: 100% (1.0)
        - Hər addım: -10% (-0.10)
        - Konflikt aşkar edildikdə: 50% cərimə (* 0.5)
        """
        confidence = 1.0 - (steps * 0.10)
        if confidence < 0.0:
            confidence = 0.0
            
        if has_conflict:
            confidence *= 0.5
            
        return round(confidence, 2)

    def run_test_cycle(self):
        print("\n[V5 MEMORY ENGINE] İnam Azalması və Konflikt Testi İşə Düşür...")
        print("=" * 60)
        
        test_cases = [
            {"fact": "Birbaşa Yaddaş Çıxarışı (1 Addım)", "steps": 1, "conflict": False},
            {"fact": "Əlaqəli Zəncirvari Məntiq (3 Addım)", "steps": 3, "conflict": False},
            {"fact": "Ziddiyyətli Qaydalar Aşkar Edildi (2 Addım + Konflikt)", "steps": 2, "conflict": True},
            {"fact": "Dərin Mühakimə Zənciri (5 Addım + Konflikt)", "steps": 5, "conflict": True},
        ]

        for idx, tc in enumerate(test_cases, 1):
            conf = self.calculate_confidence(tc["steps"], tc["conflict"])
            status = "TƏSDİQLƏNDİ (Verified)" if conf >= 0.5 else "RƏDD EDİLDİ (Aşağı İnam)"
            
            print(f" Test #{idx}: {tc['fact']}")
            print(f"   └── Addım Sayı: {tc['steps']} | Konflikt: {tc['conflict']}")
            print(f"   └── Hesablanmış İnam: {int(conf * 100)}%")
            print(f"   └── Agent Qərarı: [{status}]\n")

        print("  [✓] V5 Özünü-Yoxlama (Self-Verification) dövrəsi tamamlandı.")

if __name__ == "__main__":
    tester = V5MemoryTester()
    tester.run_test_cycle()
