from brain.tool_manager import ToolManager

class ReasoningEngine:
    def __init__(self, knowledge_engine):
        self.ke = knowledge_engine
        self.tool_manager = ToolManager()

    def generate_thought_trace(self, prompt: str, intent_data: dict):
        steps = []
        prompt_lower = prompt.lower()

        steps.append({
            "type": "THOUGHT",
            "text": f"Sorğu analiz edilir və alət ehtiyacı yoxlanılır: '{prompt}'"
        })

        # 1. Alət Çağırış Məntiqi (Tool Execution Router)
        if any(k in prompt_lower for k in ["hesabla", "kalkulyator", "math", "+", "*", "/"]):
            expression = prompt.replace("hesabla", "").strip()
            steps.append({"type": "ACTION_PLAN", "text": f"'calculator' aləti işə salınır: {expression}"})
            output_payload = self.tool_manager.execute_tool("calculator", expression)

        elif any(k in prompt_lower for k in ["sistem", "os", "specs", "mühit"]):
            steps.append({"type": "ACTION_PLAN", "text": "'system_info' aləti işə salınır."})
            output_payload = self.tool_manager.execute_tool("system_info", "")

        elif prompt_lower.startswith("oxu ") or prompt_lower.startswith("read "):
            filepath = prompt.split(" ", 1)[1].strip()
            steps.append({"type": "ACTION_PLAN", "text": f"'file_reader' aləti işə salınır: {filepath}"})
            output_payload = self.tool_manager.execute_tool("file_reader", filepath)

        # 2. Əgər spesifik alət lazımdırsa, Semantik Yaddaş Bazasında Axtarış
        else:
            steps.append({"type": "THOUGHT", "text": "Semantik yaddaş bazasında axtarış aparılır..."})
            matched_facts = self.ke.search_facts(prompt)

            if matched_facts:
                steps.append({"type": "ACTION_PLAN", "text": f"Semantik yaddaşdan ({len(matched_facts)}) fakt tapıldı."})
                payload_lines = ["### Semantik Yaddaş Bazasından Faktlar:\n"]
                for cat, topic, content in matched_facts:
                    payload_lines.append(f"• [{cat} / {topic}]: {content}")
                output_payload = "\n".join(payload_lines)
            else:
                steps.append({"type": "ACTION_PLAN", "text": "Uyğun alət və ya yaddaş faktı tapılmadı."})
                output_payload = f"'{prompt}' barədə məlumat tapılmadı. Mövcud alətlər: {list(self.tool_manager.get_available_tools().keys())}"

        steps.append({
            "type": "THOUGHT",
            "text": "Nəticə generasiya edildi."
        })

        return steps, output_payload
