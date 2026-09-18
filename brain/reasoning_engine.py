from brain.knowledge_engine import KnowledgeEngine

class ReasoningEngine:
    def __init__(self, knowledge_engine: KnowledgeEngine):
        self.ke = knowledge_engine

    def think_and_deduce(self):
        """Faktlar arasında əlaqə quraraq addım-addım düşüncə zənciri formalaşdırır."""
        facts = self.ke.query_facts()
        thoughts = []
        inferences = []

        # Faktları strukturlaşdırma
        ports = [f[2] for f in facts if f[1] == "open_port"]
        services = [f[2] for f in facts if f[1] == "service"]

        thoughts.append(f"Düşüncə 1: Açıq portlar yoxlanılır... Tapıldı: {ports if ports else 'Heç biri'}")
        thoughts.append(f"Düşüncə 2: İşləyən xidmətlər təhlil olunur... Tapıldı: {services if services else 'Heç biri'}")

        # Zəncirvari məntiq (Deduction Loop)
        if "22" in ports and "ssh" in services:
            confidence = 0.95
            self.ke.add_fact("SYSTEM", "exposure_risk", "CRITICAL_SSH_EXPOSURE", fact_type="INFERRED", confidence=confidence)
            inferences.append({
                "fact": "SSH Portu 22 Xarici Təhlükəyə Açqıdır",
                "confidence": confidence,
                "reasoning": "Port 22 və SSH xidmətinin eyni anda OBSERVED olması risk yaradır."
            })
            thoughts.append("Düşüncə 3: ZƏNCİRVARİ NƏTİCƏ -> SSH Giriş Riski Çıxarıldı və Yaddaşa Yazıldı.")

        return {
            "thought_process": thoughts,
            "inferences": inferences
        }
