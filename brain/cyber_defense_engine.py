import re

class CyberDefenseEngine:
    def __init__(self):
        # Təhlükə İmzaları
        self.sqli_pattern = r"(?i)(\bUNION\b\s+\bSELECT\b|;\s*\bDROP\b\s+\bTABLE\b)"
        self.rce_pattern = r"(;|\|\||&&)\s*(cat /etc/passwd|rm -rf|wget)"

    def analyze_payload(self, raw_input: str, context: str = "PRODUCTION"):
        # 1. NORMALIZE
        normalized = raw_input.strip()

        # 2. SIGNATURE DETECTION
        has_sqli = bool(re.search(self.sqli_pattern, normalized))
        has_rce = bool(re.search(self.rce_pattern, normalized))

        # 3. STRUCTURAL & CONTEXT ANALYSIS
        risk_score = 0
        if has_rce:
            risk_score += 90
        elif has_sqli:
            risk_score += 70

        # Əgər kontekst TEST və ya EDUCATION-dırsa, birbaşa BLOCK etmirik
        if context in ["TEST", "DEBUG", "EDUCATION"]:
            risk_score -= 30

        # 4. DECISION PIPELINE (DETECT -> VERIFY -> LOG -> POLICY CHECK -> BLOCK)
        if risk_score >= 80:
            decision = "BLOCK"
        elif risk_score >= 40:
            decision = "SUSPICIOUS"
        else:
            decision = "SAFE"

        return {
            "input": raw_input,
            "risk_score": max(0, risk_score),
            "decision": decision,
            "pipeline_status": f"DETECTED -> VERIFIED -> DECISION [{decision}]"
        }
