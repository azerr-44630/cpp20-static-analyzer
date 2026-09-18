import os
from brain.knowledge_engine import KnowledgeEngine
from brain.reasoning_engine import ReasoningEngine
from brain.cyber_defense_engine import CyberDefenseEngine
from brain.universal_code_engine import UniversalCodeEngine

def test_brain_modules():
    print("=" * 60)
    print(" [Sİ-LEARN-FIRST] BRAIN MODULES INTEGRATION TEST")
    print("=" * 60)

    # 1. Knowledge Engine Testi
    print("\n1. KnowledgeEngine Test edilir...")
    ke = KnowledgeEngine("agent_memory.db")
    ke.add_fact("SYSTEM", "open_port", "22", fact_type="OBSERVED", confidence=1.0)
    ke.add_fact("SYSTEM", "service", "ssh", fact_type="OBSERVED", confidence=1.0)
    observed_facts = ke.query_facts(fact_type="OBSERVED")
    print(f"   [✓] Bazadan oxunan OBSERVED fakt sayı: {len(observed_facts)}")

    # 2. Reasoning Engine Testi
    print("\n2. ReasoningEngine (Çıxarış Mühərriki) Test edilir...")
    re = ReasoningEngine(ke)
    inferences = re.evaluate_inferences()
    print(f"   [✓] Çıxarılan INFERRED fakt sayı: {len(inferences)}")
    for inf in inferences:
        print(f"       -> Nəticə: {inf['fact']} | Əsas: {inf['basis']}")

    # 3. Cyber Defense Engine Testi
    print("\n3. CyberDefenseEngine Test edilir...")
    cde = CyberDefenseEngine()
    test_cases = [
        ("SELECT * FROM users", "PRODUCTION"),
        ("1; DROP TABLE users; --", "PRODUCTION"),
        ("1; DROP TABLE users; --", "TEST"), # Test kontekstində risk azalmalıdır
        ("normal_user_input_data", "PRODUCTION")
    ]
    
    for payload, ctx in test_cases:
        res = cde.analyze_payload(payload, context=ctx)
        print(f"   [İnput]: {payload[:25]}... | [Kontekst]: {ctx} | [Qərar]: {res['decision']} (Risk: {res['risk_score']})")

    # 4. Universal Code Engine Testi
    print("\n4. UniversalCodeEngine Test edilir...")
    uce = UniversalCodeEngine()
    py_result = uce.analyze_code("x = 10", "python")
    print(f"   [✓] Python Kod Analizi: {py_result}")

    print("\n" + "=" * 60)
    print(" BÜTÜN TESTLƏR UĞURLA BAŞA ÇATDI!")
    print("=" * 60)

if __name__ == "__main__":
    test_brain_modules()
