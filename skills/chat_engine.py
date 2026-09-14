import random
from core.micro_llm import MicroLLM

class ChatEngine:
    """SI-GUARD Canlı Söhbət Və Micro-LLM Generativ Persona Modulu"""
    def __init__(self):
        self.llm = MicroLLM()
        self._auto_train_default_corpus()

        self.greetings = [
            "Salam, dostum! 🛡️ SI-GUARD xidmətindədir. Bu gün əhvalın necədir?",
            "Salam! Kiber-müdafiə perimetri sakitdir. Sən necəsən, nə var nə yox?",
            "Vəleykum salam! Bütün sistemlər qaydasındadır. Söhbətə və ya işə hazıram!"
        ]
        self.how_are_you = [
            "Sistemlərim 100% effektivliklə çalışır! ⚡ Fonda tələləri, faylları və neyron şəbəkəmi izləyirəm. Səndə vəziyyət necədir?",
            "Əlayam! Termux daxilində daxili Micro-LLM neyron şəbəkəmlə özümü çox rahat hiss edirəm. Günün necə keçir?"
        ]

    def _auto_train_default_corpus(self):
        default_data = """
        salam dostum kiber müdafiə sistemi aktivdir təhlükəsizlik tam qorunur.
        si-guard avtonom agentdir kodları skan edir zəiflikləri tapır və sistemləri qoruyur.
        biz birlikdə sistemi daha güclü edirik kiber təhlükəsizlik və kodlaşdırma haqqında danışa bilərik.
        termux mühitində 100 faiz lokal çalışıram heç bir xarici api lazımdır.
        bütün loglar və fayllar nəzarət altındadır hər şey qaydasındadır.
        """
        self.llm.train(default_data, epochs=5)

    def train_llm(self, custom_text):
        return self.llm.train(custom_text, epochs=10)

    def get_response(self, text):
        cmd = text.lower().strip()
        
        if any(w in cmd for w in ["salam", "privet", "hello", "hi"]):
            return random.choice(self.greetings)
        if any(w in cmd for w in ["necəsən", "necesen", "keyf", "nə var nə yox"]):
            return random.choice(self.how_are_you)

        # Standart şablon tapılmadıqda daxili Micro-LLM generasiya edir!
        llm_reply = self.llm.generate(text, max_tokens=20, temperature=0.7)
        if llm_reply and len(llm_reply.split()) > 2:
            return f"🤖 [Micro-LLM Generasiyası]: {llm_reply}"
        
        return "Səni dinləyirəm! Kiber-müdafiə, kodlar və ya sistemin təhlükəsizliyi haqqında söhbət edə bilərik."
