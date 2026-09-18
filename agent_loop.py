import sqlite3
import os
import re
from ast_engine import CppASTAnalyzer

DB_NAME = "agent_memory.db"

class AgentCore:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self.analyzer = CppASTAnalyzer(db_path)
        self._init_cpp_knowledge()

    def _init_cpp_knowledge(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # C++ qaydalarını yaddaşa yükləyirik
        cpp_facts = [
            ("raw_pointer_array", "Raw pointer array allocation detected: use std::vector or std::array"),
            ("vector_fix", "Replace raw array with std::vector for automatic memory management"),
            ("c_style_cast", "C-style cast detected: use static_cast or reinterpret_cast in modern C++")
        ]
        
        for f_id, content in cpp_facts:
            cursor.execute("INSERT OR REPLACE INTO agent_knowledge (fact_id, fact_content) VALUES (?, ?)", (f_id, content))
            
        # Əlaqələr
        links = [
            ("raw_pointer_array", "recommended_fix", "vector_fix")
        ]
        
        for src, rel, tgt in links:
            cursor.execute("INSERT INTO knowledge_links (source_id, relation_type, target_id) VALUES (?, ?, ?)", (src, rel, tgt))
            
        conn.commit()
        conn.close()

    def run_agentic_analysis(self, cpp_code: str):
        print("=== 1. C++ KODUNUN AST TƏHLİLİ ===")
        issues = self.analyzer.analyze_code(cpp_code)
        
        if not issues:
            print("[+] Kodda heç bir köhnəlmiş/təhlükəli struktur tapılmadı.")
            return

        print(f"[!] {len(issues)} ədəd potensial problem aşkarlandı:\n")

        print("=== 2. YADDAŞDAN BİLİKLƏRİN VƏ NƏTİCƏLƏRİN ÇIXARILMASI (INFERENCE) ===")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for idx, issue in enumerate(issues, 1):
            p_type = issue["problem_type"]
            old_code = issue["old_code"]
            
            print(f"[{idx}] Tapılan Xəta: '{old_code}' (Sətir {issue['line_number']})")
            
            # Yaddaşdan xətaya uyğun qaydanı alırıq
            cursor.execute("SELECT fact_content FROM agent_knowledge WHERE fact_id = ?", (p_type,))
            fact = cursor.fetchone()
            
            if fact:
                print(f"    🧠 Yaddaş Qaydası: {fact[0]}")
            
            # Əlaqəli məsləhəti/düzəlişi alırıq
            cursor.execute("""
                SELECT k.fact_content 
                FROM knowledge_links l 
                JOIN agent_knowledge k ON l.target_id = k.fact_id 
                WHERE l.source_id = ?
            """, (p_type,))
            fix_suggestion = cursor.fetchone()
            
            if fix_suggestion:
                print(f"    💡 Məntiqi Təklif: {fix_suggestion[0]}")
            print("-" * 50)

        conn.close()

if __name__ == "__main__":
    agent = AgentCore()
    
    # Test üçün C++ kodu
    sample_cpp_code = """
    #include <iostream>

    int main() {
        int* arr = new int[50];
        float x = (float)10;
        return 0;
    }
    """
    
    agent.run_agentic_analysis(sample_cpp_code)
