import sqlite3
import os
import re

DB_NAME = "agent_memory.db"

class AgentMemory:
    def __init__(self, db_path=DB_NAME, reset_db=False):
        self.db_path = db_path
        if reset_db and os.path.exists(self.db_path):
            os.remove(self.db_path)
        self._init_memory_tables()

    def _init_memory_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_knowledge (
                fact_id TEXT PRIMARY KEY,
                fact_content TEXT NOT NULL,
                version INTEGER DEFAULT 1,
                status TEXT DEFAULT 'active',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                FOREIGN KEY(source_id) REFERENCES agent_knowledge(fact_id)
            )
        """)
        
        conn.commit()
        conn.close()

    def teach(self, fact_id: str, content: str, status="active"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO agent_knowledge (fact_id, fact_content, status)
            VALUES (?, ?, ?)
        """, (fact_id, content, status))
        conn.commit()
        conn.close()

    def link_facts(self, source_id: str, relation_type: str, target_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO knowledge_links (source_id, relation_type, target_id)
            VALUES (?, ?, ?)
        """, (source_id, relation_type, target_id))
        conn.commit()
        conn.close()

    # V5: Confidence Decay və Self-Verification ilə Məntiqi Çıxarış
    def infer_with_confidence(self, observation: str):
        print(f"\n[OBSERVATION] Müşahidə daxil oldu: \"{observation}\"")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT fact_id, fact_content FROM agent_knowledge")
        all_facts = cursor.fetchall()
        conn.close()

        matched_fact_id = None
        for fact_id, content in all_facts:
            keywords = [w.lower() for w in re.findall(r'\w+', content)]
            obs_words = [w.lower() for w in re.findall(r'\w+', observation)]
            
            if any(word in keywords for word in obs_words if len(word) > 2):
                matched_fact_id = fact_id
                print(f"[MATCH] Müşahidə yaddaşdakı '{fact_id}' faktı ilə uyğunlaşdı.")
                break

        if not matched_fact_id:
            print("[INFERENCE FAILED] Müşahidəyə uyğun bilik tapılmadı.")
            return []

        deductions = []
        # Başlanğıc inam əmsalı = 1.0 (100%)
        self._traverse_with_decay(matched_fact_id, deductions, set(), initial_confidence=1.0)

        print(f"\n[DEDUCTION RESULT - V5 VERIFIED]")
        for idx, item in enumerate(deductions, 1):
            conf_str = f"{item['confidence'] * 100:.1f}%"
            status_flag = f"[{item['status'].upper()}]"
            print(f"   {idx}. {item['content']} | Confidence: {conf_str} {status_flag}")
            
        return deductions

    def _traverse_with_decay(self, current_id: str, deductions: list, visited: set, initial_confidence: float):
        if current_id in visited:
            return
        visited.add(current_id)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT fact_content, status FROM agent_knowledge WHERE fact_id = ?", (current_id,))
        fact = cursor.fetchone()
        
        cursor.execute("SELECT target_id FROM knowledge_links WHERE source_id = ?", (current_id,))
        links = cursor.fetchall()
        conn.close()

        if fact:
            content, status = fact
            # Konflikt varsa inam əmsalı 50% azaldılır
            current_conf = initial_confidence * (0.5 if status == "conflict" else 1.0)
            deductions.append({
                "fact_id": current_id,
                "content": content,
                "confidence": current_conf,
                "status": status
            })

        for (target_id,) in links:
            # Hər keçiddə inam əmsalı 10% azalır (Decay = 0.90)
            self._traverse_with_decay(target_id, deductions, visited, initial_confidence * 0.90)

if __name__ == "__main__":
    memory = AgentMemory(reset_db=True)
    
    # Faktlar
    memory.teach("port_22", "TCP port 22 is commonly associated with SSH")
    # ssh_service faktını qəsdən konfliktli olaraq qeyd edirik
    memory.teach("ssh_service", "SSH enables secure remote access", status="conflict")
    memory.teach("auth_req", "Remote access requires authentication")
    
    memory.link_facts("port_22", "associated_with", "ssh_service")
    memory.link_facts("ssh_service", "requires", "auth_req")
    
    # V5 Testi
    memory.infer_with_confidence("Port 22 is active")
