import os
import json
from skills.chat_engine import ChatEngine

# Əlavə skill-lər yoxdursa sistemi dayandırmamaq üçün safe-import
try:
    from core.neural_brain import NeuralBrain
except ImportError:
    class NeuralBrain:
        def evaluate(self, command):
            return {"intent": "CHAT", "thought_chain": "🧠 [NeuralBrain]: Söhbət rejimində təhlil edilir."}

class AIAgent:
    def __init__(self, db=None, blocker=None):
        self.db = db
        self.blocker = blocker
        self.chat = ChatEngine()
        self.brain = NeuralBrain()

    def process_command(self, command):
        mind = self.brain.evaluate(command)
        thought_output = mind.get("thought_chain", "") + "\n" + "-"*50
        cmd = command.lower().strip()

        # LLM Təlim əmri
        if cmd.startswith("llm train") or cmd.startswith("öyrət llm"):
            text_to_train = command.replace("llm train", "").replace("öyrət llm", "").strip()
            if not text_to_train:
                text_to_train = "SI-GUARD kiber müdafiə agentidir Termux daxilində avtonom təhlükəsizlik skanları aparır."
            res = self.chat.train_llm(text_to_train)
            return f"{thought_output}\n🧠 {res}"

        # Canlı Söhbət Və Micro-LLM Dialoqu
        reply = self.chat.get_response(command)
        return f"{thought_output}\n💬 {reply}"
