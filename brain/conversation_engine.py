import random
from brain.knowledge_engine import KnowledgeEngine

class DynamicConversationEngine:
    def __init__(self, db_path="agent_memory.db"):
        self.ke = KnowledgeEngine(db_path)
        self.history = []

    def generate_dynamic_response(self, intent_data):
        intent = intent_data["intent"]
        slots = intent_data["slots"]
        text = intent_data["raw_text"]

        # 1. Agent daxili yaddaşını və vəziyyətini oxuyur (Self-Awareness)
        facts = self.ke.query_facts()
        observed_count = len([f for f in facts if f[3] == 'OBSERVED'])
        inferred_count = len([f for f in facts if f[3] == 'INFERRED'])

        # 2. Status sorğuları ("necəsən?", "nə var nə yox?") üçün daxili təhlil
        if intent == "GREETING" or "necesen" in text.lower():
            status_thoughts = [
                f"Yaddaş bazamı təhlil etdim. Hazırda {observed_count} müşahidə olunmuş fakt və {inferred_count} deduktiv nəticə üzərində işləyirəm.",
                f"Sistem aktivdir. Son əməliyyatlarda {len(self.history)} dialoq addımı yadda saxlanılıb.",
                f"Lokal mühit sabitdir. Yaddaş bazamda toplam {len(facts)} fakt mövcuddur, yeni tapşırığa hazıram."
            ]
            return random.choice(status_thoughts)

        # 3. Mənasız və ya ümumi yazılar üçün faktlardan dinamik cavab yığımı
        elif intent == "GENERAL_CHAT":
            if facts:
                sample_fact = random.choice(facts)
                return f"Səni dinləyirəm. Yaddaşımdakı son faktlardan biri: [{sample_fact[0]}] -> {sample_fact[1]}: {sample_fact[2]}. Bu barədə işləyək, yoxsa kodu analiz edək?"
            return f"Daxil etdiyin '{text}' ifadəsini emal etdim. Hələ ki, bu barədə konkret qayda yoxdur, ammma yaddaşıma qeyd ala bilərəm."

        # 4. Digər intent-lər üçün dinamik kontekst
        return f"Sorğunu emal edirəm. Niyyət: {intent}. İşlənməli slot parametrləri: {slots if slots else 'Yoxdur'}."
