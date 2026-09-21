class ReasoningEngine:
    def __init__(self, knowledge_engine):
        self.ke = knowledge_engine

    def generate_thought_trace(self, prompt: str, intent_data: dict):
        steps = []
        steps.append({
            "type": "THOUGHT",
            "text": f"Sorğu daxili yaddaş bazasında axtarılır: '{prompt}'"
        })

        # Bazadan dinamik məlumatların oxunması
        matched_facts = self.ke.search_facts(prompt)

        if matched_facts:
            steps.append({
                "type": "ACTION_PLAN",
                "text": f"Daxili bazadan ({len(matched_facts)}) müvafiq bilik tapıldı. Cavab dinamik olaraq formalaşdırılır."
            })
            
            payload_lines = ["### Agent Yaddaş Bazasından Dinamik Çıxarış:\n"]
            for cat, topic, content in matched_facts:
                payload_lines.append(f"• [{cat} / {topic}]: {content}")
            
            output_payload = "\n".join(payload_lines)
        else:
            steps.append({
                "type": "ACTION_PLAN",
                "text": "Müvafiq daxili bilik tapılmadı. Ümumi təhlil rejiminə keçilir."
            })
            output_payload = f"'{prompt}' haqqında bazada xüsusi fakt tapılmadı. Yeni bilik əlavə etmək üçün təlim skriptlərindən istifadə edin."

        steps.append({
            "type": "THOUGHT",
            "text": "Nəticələr hazırlanaraq birbaşa ekrana ötürüldü."
        })

        return steps, output_payload
