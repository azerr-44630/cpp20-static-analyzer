import sqlite3
import time

class MemoryManager:
    def __init__(self, db_path="agent_memory.db"):
        self.db_path = db_path
        self._init_tables()

    def _init_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Rules Table (Dinamik Öyrənilən Qaydalar)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trigger_pattern TEXT NOT NULL UNIQUE,
                risk_category TEXT NOT NULL,
                confidence REAL DEFAULT 0.90,
                source TEXT DEFAULT 'TEACH',
                created_at REAL
            )
        """)

        # 2. Experience Table (Əvvəlki Qərarların Nəticələri)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_action TEXT NOT NULL,
                decision_made TEXT NOT NULL,
                outcome_score REAL DEFAULT 1.0,
                timestamp REAL
            )
        """)
        
        conn.commit()
        conn.close()

    def add_rule(self, trigger_pattern, risk_category, confidence=0.90, source="TEACH"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO rules (trigger_pattern, risk_category, confidence, source, created_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(trigger_pattern) DO UPDATE SET
                    confidence = MIN(1.0, confidence + 0.05),
                    risk_category = excluded.risk_category
            """, (trigger_pattern.lower(), risk_category, confidence, source, time.time()))
            conn.commit()
            return True
        except Exception as e:
            print(f"[MEMORY ERROR] Qayda yazılmadı: {e}")
            return False
        finally:
            conn.close()

    def get_rules(self, min_confidence=0.5):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT trigger_pattern, risk_category, confidence FROM rules WHERE confidence >= ?", (min_confidence,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def log_experience(self, action, decision, score=1.0):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO experiences (input_action, decision_made, outcome_score, timestamp)
            VALUES (?, ?, ?, ?)
        """, (action, decision, score, time.time()))
        conn.commit()
        conn.close()
