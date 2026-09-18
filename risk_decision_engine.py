import sqlite3
from ast_engine import CppASTAnalyzer
from knowledge_graph import V6KnowledgeGraph
from inference_engine import V7InferenceEngine
from experience_learner import V8ExperienceLearner

DB_NAME = "agent_memory.db"

class V9RiskDecisionEngine:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self.kg = V6KnowledgeGraph(db_path)
        self.inference_engine = V7InferenceEngine(db_path)
        self.learner = V8ExperienceLearner(db_path)

    def evaluate_and_decide(self, directory="."):
        analyzer = CppASTAnalyzer()
        issues = analyzer.analyze_directory(directory)

        print("\n[V9 RISK & DECISION ENGINE] Risk Qiymətləndirilməsi Və Avtonom Qərar Matrixi")
        print("=" * 65)

        if not issues:
            print("  [✓] Heç bir risk faktoru aşkar edilmədi. Sistem təhlükəsizdir.")
            return []

        decisions = []

        for issue in issues:
            loc = f"{issue['file']}:{issue['line']}"
            code = issue['code']
            issue_type = issue['type']

            # 1. Bazatörəli Risk Balı Hesablanması
            base_risk = 70 if issue_type == "raw_pointer_array" else 40
            
            # 2. Bilik Qrafındakı Derivativ Təsirlərin Riskə Əlavəsi
            graph_impact = self.kg.traverse_graph(issue_type, max_depth=2)
            risk_multiplier = 1.0 + (len(graph_impact) * 0.05)
            calculated_risk = min(100, int(base_risk * risk_multiplier))

            # 3. V8-dən Öyrənilmiş İnam Səviyyəsinin Alınması
            rec_fix = self.learner.recommend_fix(code)
            confidence = 0.75 if rec_fix else 0.50

            # 4. Agent Qərar Matrixi (Decision Matrix)
            if calculated_risk >= 75 and confidence >= 0.70:
                decision = "AUTO_FIX_RECOMMENDED"
                action_plan = "Kritik risk və yüksək təcrübə inamı var. Avtomatik refaktorinq təhlükəsizdir."
            elif calculated_risk >= 75 and confidence < 0.70:
                decision = "HUMAN_APPROVAL_REQUIRED"
                action_plan = "Kritik risk var, lakin təcrübə inamı azdır. Mühəndis təsdiqi tələb olunur."
            else:
                decision = "LOG_AND_MONITOR"
                action_plan = "Aşağı/orta riskli fakt. Sadəcə xəbərdarlıq loglanmalıdır."

            decisions.append({
                "location": loc,
                "code": code,
                "risk_score": calculated_risk,
                "confidence": confidence,
                "decision": decision,
                "action_plan": action_plan
            })

        print("\n" + "=" * 65)
        print(" [V9 AGENT YEKUN QƏRAR MATRIXİ NƏTİCƏLƏRİ]")
        print("=" * 65)

        for idx, dec in enumerate(decisions, 1):
            print(f" [{idx}] Məkan   : {dec['location']}")
            print(f"     Kod      : {dec['code']}")
            print(f"     Risk Balı: {dec['risk_score']}/100 | Öyrənilmiş İnam: {int(dec['confidence']*100)}%")
            print(f"     Qərar    : [{dec['decision']}]")
            print(f"     Tədbir   : {dec['action_plan']}")
            print("-" * 65)

        return decisions

if __name__ == "__main__":
    engine = V9RiskDecisionEngine()
    engine.evaluate_and_decide()
