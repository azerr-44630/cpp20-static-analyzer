import sqlite3
import re
from collections import defaultdict

DB_NAME = "agent_memory.db"

class V8ExperienceLearner:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fix_experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                line_number INTEGER NOT NULL,
                original_code TEXT NOT NULL,
                fixed_code TEXT NOT NULL,
                status TEXT DEFAULT 'SUCCESS',
                confidence_score REAL DEFAULT 1.0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Mövcud cədvəldə sütunların olub-olmadığını yoxlayıb miqrasiya edirik
        cursor.execute("PRAGMA table_info(fix_experience)")
        cols = [c[1] for c in cursor.fetchall()]
        if "status" not in cols:
            cursor.execute("ALTER TABLE fix_experience ADD COLUMN status TEXT DEFAULT 'SUCCESS'")
        if "confidence_score" not in cols:
            cursor.execute("ALTER TABLE fix_experience ADD COLUMN confidence_score REAL DEFAULT 1.0")
            
        conn.commit()
        conn.close()

    def analyze_experiences(self):
        """Keçmiş refaktorinq təcrübələrini statistik olaraq təhlil edir."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT original_code, fixed_code, status, confidence_score FROM fix_experience")
        rows = cursor.fetchall()
        conn.close()

        print("\n[V8 EXPERIENCE-BASED LEARNER] Keçmiş Təcrübələrin Təhlili")
        print("=" * 60)

        if not rows:
            print("  [!] Hələlik heç bir keçmiş fix təcrübəsi qeydə alınmayıb.")
            print("  [!] Təcrübə bazasını zənginləşdirmək üçün əvvəlcə '2 -> Auto-Fix' icra edin.")
            return {}

        patterns = defaultdict(lambda: {"count": 0, "success_count": 0, "examples": []})

        for orig, fixed, status, conf in rows:
            if "new" in orig and "std::vector" in fixed:
                pattern_key = "RAW_POINTER_TO_STD_VECTOR"
            else:
                pattern_key = "GENERIC_REFACTORING"

            patterns[pattern_key]["count"] += 1
            if status == "SUCCESS":
                patterns[pattern_key]["success_count"] += 1
            patterns[pattern_key]["examples"].append((orig, fixed, conf))

        for key, data in patterns.items():
            total = data["count"]
            successes = data["success_count"]
            rate = (successes / total) * 100 if total > 0 else 0
            
            # Təcrübə artdıqca inam dərəcəsi dinamik olaraq yüksəlir
            learned_confidence = min(0.99, round(0.70 + (total * 0.05), 2))

            print(f" Pattern Türü        : {key}")
            print(f" └── Ümumi Tətbiq   : {total} dəfə")
            print(f" └── Uğur Nisbəti   : {rate:.1f}%")
            print(f" └── Öyrənilmiş İnam: {int(learned_confidence * 100)}% (Təcrübə ilə dinamik artır)")
            print("-" * 60)

        return patterns

    def recommend_fix(self, code_snippet):
        """Aşkar edilmiş kod üçün keçmiş uğurlu təcrübələrə əsasən tövsiyə verir."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT original_code, fixed_code, COUNT(*) as frequency
            FROM fix_experience
            WHERE status = 'SUCCESS'
            GROUP BY original_code, fixed_code
            ORDER BY frequency DESC
        """)
        top_fixes = cursor.fetchall()
        conn.close()

        print(f"\n[V8 REFACTOR RECOMMENDATION] Keçmiş Təcrübə Axtarışı:")
        print(f" Kod Parçası: '{code_snippet.strip()}'")
        print("-" * 60)

        for orig, fixed, freq in top_fixes:
            if re.search(r'\bnew\b', code_snippet) and "std::vector" in fixed:
                learned_confidence = min(0.99, round(0.70 + (freq * 0.05), 2))
                print(f"  [✓] Keçmiş Uğurlu Təcrübə Tapıldı (Tətbiq tezliyi: {freq} dəfə)")
                print(f"      Öyrənilmiş Düzəliş : {fixed.strip()}")
                print(f"      Qazanılmış İnam   : {int(learned_confidence * 100)}%")
                return fixed

        print("  [!] Oxşar təcrübə tapılmadı. Standart analitik qaydalar istifadə ediləcək.")
        return None

if __name__ == "__main__":
    learner = V8ExperienceLearner()
    learner.analyze_experiences()
    learner.recommend_fix("int* arr = new int[100];")
