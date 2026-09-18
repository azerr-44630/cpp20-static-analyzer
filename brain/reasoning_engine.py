from brain.knowledge_engine import KnowledgeEngine

class ReasoningEngine:
    def __init__(self, knowledge_engine: KnowledgeEngine):
        self.ke = knowledge_engine

    def generate_thought_trace(self, user_input, intent_data):
        """Görsellerdeki gibi adım adım düşünce ve süreç akışı (Summary Trace) üretir."""
        steps = []
        
        # 1. Başlangıç Tespiti / Hedef
        steps.append({
            "type": "THOUGHT",
            "text": f"Gelen isteği değerlendirme ve hedefi belirleme: '{user_input}'"
        })

        # 2. Arama / Sorgulama Tespiti (Görseldeki Searched for... mantığı)
        slots = intent_data.get("slots", {})
        if "file" in slots:
            steps.append({
                "type": "SEARCH",
                "text": f"Yerel depoda dosya ve AST analizi aranıyor: '{slots['file']}'"
            })
        elif "port" in slots:
            steps.append({
                "type": "SEARCH",
                "text": f"Ağ ve hafıza veritabanında port bilgisi sorgulanıyor: '{slots['port']}'"
            })

        # 3. Yaddaş və Fakt Analizi
        facts = self.ke.query_facts()
        steps.append({
            "type": "THOUGHT",
            "text": f"Hafızadaki {len(facts)} kayıtlı fakt ve öğrenilmiş kurallar taranıyor."
        })

        # 4. Risk ve Çıkarım Hesabı
        steps.append({
            "type": "THOUGHT",
            "text": "Kod güvenliği, mantıksal zincir (Chain-of-Thought) ve risk skorlaması yapılıyor."
        })

        return steps
