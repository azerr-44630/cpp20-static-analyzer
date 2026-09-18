import sqlite3
import os
from collections import deque

DB_NAME = "agent_memory.db"

class V6KnowledgeGraph:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self._init_graph_tables()
        self._seed_cpp20_knowledge()

    def _init_graph_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(agent_knowledge)")
        cols = [col[1] for col in cursor.fetchall()]
        if cols and "key_name" not in cols:
            cursor.execute("DROP TABLE agent_knowledge")

        cursor.execute("PRAGMA table_info(knowledge_links)")
        link_cols = [col[1] for col in cursor.fetchall()]
        if link_cols and "source_key" not in link_cols:
            cursor.execute("DROP TABLE knowledge_links")

        conn.commit()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_name TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL,
                category TEXT DEFAULT 'general'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_key TEXT NOT NULL,
                target_key TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                weight REAL DEFAULT 1.0,
                UNIQUE(source_key, target_key, relation_type)
            )
        """)
        conn.commit()
        conn.close()

    def _seed_cpp20_knowledge(self):
        nodes = [
            ("raw_pointer_array", "Xam göstərici ilə dinamik massiv ayrılması (new T[])", "vulnerability"),
            ("manual_memory_management", "Əl ilə yaddaş idarəetməsi (delete[] tələbi)", "risk"),
            ("memory_leak", "Yaddaş sızması (Memory Leak) riski", "impact"),
            ("exception_unsafe", "İstisna təhlükəsizliyinin (Exception Safety) olmaması", "impact"),
            ("std_vector", "std::vector<T> RAII konteyneri", "solution"),
            ("automatic_cleanup", "Avtomatik resurs azad edilməsi (Destruktur)", "benefit"),
            ("cache_locality", "Davamlı yaddaş bloku və Cəş uyğunluğu", "benefit")
        ]

        links = [
            ("raw_pointer_array", "manual_memory_management", "REQUIRES", 1.0),
            ("manual_memory_management", "memory_leak", "CAUSES_RISK", 0.9),
            ("manual_memory_management", "exception_unsafe", "CAUSES_RISK", 0.85),
            ("raw_pointer_array", "std_vector", "RECOMMENDS_FIX", 1.0),
            ("std_vector", "automatic_cleanup", "PROVIDES", 0.95),
            ("std_vector", "cache_locality", "PROVIDES", 0.9)
        ]

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for key, desc, cat in nodes:
            cursor.execute("""
                INSERT INTO agent_knowledge (key_name, description, category)
                VALUES (?, ?, ?)
                ON CONFLICT(key_name) DO UPDATE SET description=excluded.description
            """, (key, desc, cat))

        for src, tgt, rel, w in links:
            cursor.execute("""
                INSERT INTO knowledge_links (source_key, target_key, relation_type, weight)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(source_key, target_key, relation_type) DO UPDATE SET weight=excluded.weight
            """, (src, tgt, rel, w))

        conn.commit()
        conn.close()

    def traverse_graph(self, start_key: str, max_depth: int = 2):
        """İkiistiqamətli (Bidirectional) BFS alqoritmi ilə həm səbəbləri, həm də nəticələri tapır."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        visited = set()
        queue = deque([(start_key, 0)])
        traversal_results = []

        while queue:
            current_key, depth = queue.popleft()

            if depth >= max_depth or current_key in visited:
                continue

            visited.add(current_key)

            # 1. İrəliyə doğru əlaqələr (Outgoing: current -> target)
            cursor.execute("""
                SELECT l.target_key, k.description, l.relation_type, l.weight, 'OUT' as direction
                FROM knowledge_links l
                JOIN agent_knowledge k ON l.target_key = k.key_name
                WHERE l.source_key = ?
            """, (current_key,))
            outgoing = cursor.fetchall()

            # 2. Geriyə doğru əlaqələr (Incoming: source -> current)
            cursor.execute("""
                SELECT l.source_key, k.description, l.relation_type, l.weight, 'IN' as direction
                FROM knowledge_links l
                JOIN agent_knowledge k ON l.source_key = k.key_name
                WHERE l.target_key = ?
            """, (current_key,))
            incoming = cursor.fetchall()

            for tgt_key, desc, rel, weight, direction in outgoing:
                traversal_results.append({
                    "from": current_key,
                    "direction": direction,
                    "relation": rel,
                    "to": tgt_key,
                    "target_desc": desc,
                    "weight": weight,
                    "depth": depth + 1
                })
                if tgt_key not in visited:
                    queue.append((tgt_key, depth + 1))

            for src_key, desc, rel, weight, direction in incoming:
                traversal_results.append({
                    "from": current_key,
                    "direction": direction,
                    "relation": f"CAUSED_BY ({rel})",
                    "to": src_key,
                    "target_desc": desc,
                    "weight": weight,
                    "depth": depth + 1
                })
                if src_key not in visited:
                    queue.append((src_key, depth + 1))

        conn.close()
        return traversal_results

    def explain_impact(self, problem_type: str):
        results = self.traverse_graph(problem_type, max_depth=2)
        
        print(f"\n[V6 KNOWLEDGE GRAPH ANALYZER] Root Node: '{problem_type}'")
        print("=" * 60)

        if not results:
            print("  [!] Bu problem üçün qraf əlaqəsi tapılmadı.")
            return

        for step in results:
            indent = "  " * step["depth"]
            print(f"{indent}└── [{step['relation']}] ➔ {step['to']} (İnam/Ağırlıq: {int(step['weight']*100)}%)")
            print(f"{indent}    Məfhum: {step['target_desc']}")

if __name__ == "__main__":
    kg = V6KnowledgeGraph()
    kg.explain_impact("memory_leak")
