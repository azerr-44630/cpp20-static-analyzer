import sqlite3
import re

DB_NAME = "agent_memory.db"

class LocalCppAnalyzer:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path

    def analyze_code(self, code_snippet):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT category, pattern, severity, issue_desc, fix_template FROM local_rules")
        rules = cursor.fetchall()

        reports = []
        for category, pattern, severity, issue_desc, fix_template in rules:
            if re.search(pattern, code_snippet):
                reports.append({
                    "category": category,
                    "severity": severity,
                    "issue": issue_desc,
                    "fix_suggestion": fix_template
                })

        conn.close()
        return reports

    def get_cpp_reference(self, keyword):
        """Kənar LLM olmadan lokal bazadan dərslik qaydasını çəkir."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = f"%{keyword}%"
        cursor.execute('''
            SELECT chapter_num, topic, content, best_practice 
            FROM cpp_knowledge 
            WHERE topic LIKE ? OR content LIKE ?
        ''', (query, query))
        
        results = cursor.fetchall()
        conn.close()
        return results

if __name__ == "__main__":
    analyzer = LocalCppAnalyzer()

    # Test üçün problemli C++ kodu
    test_code = """
    class Base {
    public:
        Base() {}
        ~Base() {}
    };

    class Derived : public Base {
        int* data = new int[100];
    };
    """

    print("\n--- LOKAL TƏHLİL NƏTİCƏSİ (LLM-siz) ---")
    issues = analyzer.analyze_code(test_code)
    for idx, item in enumerate(issues, 1):
        print(f"\n[{idx}] Xəbərdarlıq Səviyyəsi: {item['severity']}")
        print(f"    Problem: {item['issue']}")
        print(f"    Tövsiyə olunan Həll:\n{item['fix_suggestion']}")

