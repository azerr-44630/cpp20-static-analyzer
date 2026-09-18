import sqlite3
import time

class KnowledgeEngine:
    def __init__(self, db_path="agent_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity TEXT NOT NULL,
                attribute TEXT NOT NULL,
                value TEXT NOT NULL,
                fact_type TEXT CHECK(fact_type IN ('OBSERVED', 'INFERRED', 'UNKNOWN')),
                confidence REAL DEFAULT 1.0,
                timestamp REAL
            )
        """)
        conn.commit()
        conn.close()

    def add_fact(self, entity, attribute, value, fact_type="OBSERVED", confidence=1.0):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO facts (entity, attribute, value, fact_type, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (entity, attribute, value, fact_type, confidence, time.time()))
        conn.commit()
        conn.close()

    def query_facts(self, entity=None, fact_type=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "SELECT entity, attribute, value, fact_type, confidence FROM facts WHERE 1=1"
        params = []
        if entity:
            query += " AND entity = ?"
            params.append(entity)
        if fact_type:
            query += " AND fact_type = ?"
            params.append(fact_type)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
