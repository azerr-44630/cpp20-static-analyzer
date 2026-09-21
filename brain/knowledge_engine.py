import sqlite3

class KnowledgeEngine:
    def __init__(self, db_path="agent_memory.db"):
        self.db_path = db_path

    def search_facts(self, query: str):
        """İstifadəçi sorğusundakı açar sözlərə əsasən bazadan faktları tapır."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        words = query.lower().split()
        results = []
        
        for word in words:
            if len(word) < 3:  # Çox qısa sözləri nəzərə almırıq
                continue
            
            cursor.execute("""
                SELECT category, topic, content FROM facts 
                WHERE LOWER(category) LIKE ? OR LOWER(topic) LIKE ? OR LOWER(content) LIKE ?
            """, (f"%{word}%", f"%{word}%", f"%{word}%"))
            
            rows = cursor.fetchall()
            for r in rows:
                if r not in results:
                    results.append(r)
                    
        conn.close()
        return results
