import re
from difflib import SequenceMatcher

class LocalNLPEngine:
    def __init__(self):
        self.intents = {
            "ANALYZE_CODE": ["analiz et", "kodu yoxla", "scan code", "analiz", "yoxla"],
            "FIX_CODE": ["düzəlt", "fix code", "refaktor", "xətanı aradan qaldır"],
            "CHECK_DEFENSE": ["təhlükəsizlik", "risk", "exploit", "hücum", "cyber defense", "bloke"],
            "QUERY_KNOWLEDGE": ["bilik", "fakt", "knowledge", "port", "ssh"],
            "GREETING": ["salam", "necəsən", "hello", "hi", "salut"]
        }

    def parse_intent(self, text: str):
        text_lower = text.lower()
        best_intent = "UNKNOWN"
        max_score = 0.0

        for intent, patterns in self.intents.items():
            for pat in patterns:
                score = SequenceMatcher(None, text_lower, pat).ratio()
                if pat in text_lower:
                    score = max(score, 0.85)
                if score > max_score:
                    max_score = score
                    best_intent = intent

        # Slot-Filling (Parametrlərin çıxarılması, məs: port nömrəsi, fayl adı)
        slots = {}
        port_match = re.search(r'\bport\s*(\d+)\b', text_lower)
        if port_match:
            slots["port"] = port_match.group(1)
            
        file_match = re.search(r'([\w\-\/]+\.(py|cpp|js|go))', text)
        if file_match:
            slots["file"] = file_match.group(1)

        return {
            "intent": best_intent if max_score > 0.4 else "GENERAL_CHAT",
            "confidence": max_score,
            "slots": slots,
            "raw_text": text
        }
