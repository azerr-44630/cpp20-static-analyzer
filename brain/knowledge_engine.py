import sqlite3
import math
import re
from collections import Counter

class KnowledgeEngine:
    def __init__(self, db_path="agent_memory.db"):
        self.db_path = db_path

    def _get_all_facts(self):
        """Bazadakı bütün faktları oxuyur."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT category, topic, content FROM facts")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def _tokenize(self, text: str):
        """Mətni kiçik hərflərə çevirib sözlərə bölür."""
        return re.findall(r'\w+', text.lower())

    def _text_to_vector(self, text: str):
        """Mətni söz tezliyi vektoruna (TF) çevirir."""
        words = self._tokenize(text)
        return Counter(words)

    def _cosine_similarity(self, vec1, vec2):
        """İki vektor arasındakı Kosinus Bənzərliyini (Cosine Similarity) hesablayır."""
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        return float(numerator) / denominator

    def search_facts(self, query: str, threshold=0.05):
        """
        Sorğunun bazadakı faktlarla semantik oxşarlığını hesablayır.
        threshold: Minimum oxşarlıq həddi (0.05 = 5% üst-üstə düşmə).
        """
        facts = self._get_all_facts()
        if not facts:
            return []

        query_vec = self._text_to_vector(query)
        scored_results = []

        for category, topic, content in facts:
            full_text = f"{category} {topic} {content}"
            doc_vec = self._text_to_vector(full_text)

            score = self._cosine_similarity(query_vec, doc_vec)
            if score >= threshold:
                scored_results.append((score, category, topic, content))

        # Ən yüksək semantik oxşarlıq balına görə sıralayırıq
        scored_results.sort(key=lambda x: x[0], reverse=True)

        return [(cat, top, cont) for score, cat, top, cont in scored_results]
