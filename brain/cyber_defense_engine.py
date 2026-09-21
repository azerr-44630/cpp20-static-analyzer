import re

class CyberDefenseEngine:
    def __init__(self):
        # Təhlükəli pattern-lər və injection siyahısı
        self.blocked_patterns = [
            r"(\bDROP\b|\bDELETE\b|\bINSERT\b).*\bFROM\b", # Basic SQLi
            r"<script.*?>.*?</script>",                   # XSS
            r"(\bexec\b|\beval\b|\bsystem\b)\s*\(",        # Command Injection
            r"\.\./\.\./",                                 # Path Traversal
            r"(\bunion\b.*\bselect\b)"                    # SQLi Union
        ]

    def inspect_payload(self, raw_input: str):
        """Gələn sorğunu kiber-təhlükələrə qarşı skan edir."""
        for pattern in self.blocked_patterns:
            if re.search(pattern, raw_input, re.IGNORECASE):
                return {
                    "status": "BLOCKED",
                    "reason": f"Təhlükəli pattern aşkar edildi: {pattern}"
                }
        
        return {
            "status": "CLEAN",
            "reason": "Payload təhlükəsizdir."
        }
