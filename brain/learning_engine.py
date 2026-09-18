import re
from brain.memory_manager import MemoryManager

class LearningEngine:
    def __init__(self, memory_manager: MemoryManager):
        self.mm = memory_manager

    def process_teach_input(self, text: str):
        """Təbii dildə verilən təlimatdan (TEACH) qayda çıxarır."""
        text_lower = text.lower()
        
        # Pattern Extraction: "X istifadə etmək / təhlükəli / riskli"
        match = re.search(r'([\w\(\)\._]+)\s+(istifadə etmək|təhlükəli|riskli|qadağandır)', text_lower)
        if match:
            target_symbol = match.group(1).strip()
            risk_cat = "CODE_EXECUTION_RISK" if "eval" in target_symbol or "exec" in target_symbol else "SECURITY_WARNING"
            
            # Confidence Engine & Conflict Resolution
            success = self.mm.add_rule(
                trigger_pattern=target_symbol,
                risk_category=risk_cat,
                confidence=0.95,
                source="HUMAN_TEACH"
            )
            
            if success:
                return {
                    "status": "LEARNED",
                    "rule": f"RULE: '{target_symbol}' -> {risk_cat}",
                    "confidence": 0.95
                }

        return {"status": "NO_RULE_EXTRACTED", "details": "Qayda şablonu aşkar edilmədi."}

    def evaluate_code_against_rules(self, code_snippet: str):
        """Öyrənilmiş qaydaları Universal Code Engine üçün aktivləşdirir."""
        rules = self.mm.get_rules()
        detected_risks = []

        for trigger, risk_cat, confidence in rules:
            if trigger in code_snippet.lower():
                detected_risks.append({
                    "pattern": trigger,
                    "risk_category": risk_cat,
                    "confidence": confidence
                })

        return detected_risks
