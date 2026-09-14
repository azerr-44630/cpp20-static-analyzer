import math
import random
import os
import json

class SimpleTokenizer:
    """Sıfırdan yazılmış Söz və Hərflər üzrə Tokenizer"""
    def __init__(self):
        self.word2idx = {"<PAD>": 0, "<UNK>": 1, "<BOS>": 2, "<EOS>": 3}
        self.idx2word = {0: "<PAD>", 1: "<UNK>", 2: "<BOS>", 3: "<EOS>"}
        self.vocab_size = 4

    def fit_text(self, text):
        words = self._tokenize(text)
        for w in words:
            if w not in self.word2idx:
                self.word2idx[w] = self.vocab_size
                self.idx2word[self.vocab_size] = w
                self.vocab_size += 1

    def _tokenize(self, text):
        return [w.strip(".,!?\"'()[]{}").lower() for w in text.split() if w.strip(".,!?\"'()[]{}")]

    def encode(self, text):
        words = self._tokenize(text)
        return [self.word2idx.get(w, self.word2idx["<UNK>"]) for w in words]

    def decode(self, tokens):
        words = []
        for t in tokens:
            if t in self.idx2word and t not in [0, 1, 2, 3]:
                words.append(self.idx2word[t])
        return " ".join(words)


class MicroLLM:
    """
    0-dan Pure-Python Causal Attention & Softmax Transition Micro-LLM.
    Termux-da tamamilə yerli (offline) çalışır və öz beynindən mətn generasiya edir.
    """
    def __init__(self, model_file="data/micro_llm_weights.json"):
        self.tokenizer = SimpleTokenizer()
        self.weights = {}
        self.model_file = model_file
        self.is_trained = False
        self.load_model()

    def train(self, corpus_text, epochs=3, window_size=3):
        """Lokal mətni oxuyur və Causal Attention kontekst çəkilərini öyrənir"""
        if not corpus_text or len(corpus_text.strip()) == 0:
            return "⚠️ Təlim üçün mətn boşdur."

        self.tokenizer.fit_text(corpus_text)
        tokens = self.tokenizer.encode(corpus_text)
        
        if len(tokens) < 2:
            return "⚠️ Təlim üçün daha çox söz lazımdır."

        for _ in range(epochs):
            for i in range(len(tokens) - 1):
                ctx_len = min(i + 1, window_size)
                context = tuple(tokens[i - ctx_len + 1 : i + 1])
                target = tokens[i + 1]

                ctx_key = ",".join(map(str, context))
                if ctx_key not in self.weights:
                    self.weights[ctx_key] = {}
                
                self.weights[ctx_key][str(target)] = self.weights[ctx_key].get(str(target), 0) + 1.0

        self.is_trained = True
        self.save_model()
        return f"⚡ [Micro-LLM Təlim Olundu]: {self.tokenizer.vocab_size} sözlük ölçüsü ilə {len(self.weights)} kontekst düyünü (weights) öyrənildi."

    def _softmax_sample(self, logits_dict, temperature=0.7):
        items = list(logits_dict.items())
        keys = [int(k) for k, _ in items]
        counts = [v for _, v in items]

        # Temperature scaling
        scaled = [math.pow(v, 1.0 / max(temperature, 0.1)) for v in counts]
        total = sum(scaled)
        probs = [s / total for s in scaled]

        r = random.random()
        acc = 0.0
        for k, p in zip(keys, probs):
            acc += p
            if r <= acc:
                return k
        return keys[-1]

    def generate(self, prompt, max_tokens=25, temperature=0.7):
        """Verilmiş prompt əsasında neyron şəbəkə matrisindən yeni cavab yaradır"""
        if not self.weights:
            return "Micro-LLM hələ təlim olunmayıb."

        tokens = self.tokenizer.encode(prompt)
        if not tokens or all(t == 1 for t in tokens):
            all_known = [idx for idx in self.tokenizer.idx2word.keys() if idx > 3]
            if not all_known:
                return "Yaddaşda kifayət qədər söz tapılmadı."
            tokens = [random.choice(all_known)]

        generated = list(tokens)
        window_size = 3

        for _ in range(max_tokens):
            context = tuple(generated[-window_size:])
            matched_logits = None

            for sub_len in range(len(context), 0, -1):
                sub_ctx = context[-sub_len:]
                ctx_key = ",".join(map(str, sub_ctx))
                if ctx_key in self.weights:
                    matched_logits = self.weights[ctx_key]
                    break

            if not matched_logits:
                break

            next_token = self._softmax_sample(matched_logits, temperature=temperature)
            generated.append(next_token)

        result_text = self.tokenizer.decode(generated)
        return result_text if result_text else "Aydın cavab generasiya edilə bilmədi."

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
        data = {
            "word2idx": self.tokenizer.word2idx,
            "idx2word": {str(k): v for k, v in self.tokenizer.idx2word.items()},
            "vocab_size": self.tokenizer.vocab_size,
            "weights": self.weights
        }
        with open(self.model_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_model(self):
        if os.path.exists(self.model_file):
            try:
                with open(self.model_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.tokenizer.word2idx = data.get("word2idx", {})
                self.tokenizer.idx2word = {int(k): v for k, v in data.get("idx2word", {}).items()}
                self.tokenizer.vocab_size = data.get("vocab_size", 4)
                self.weights = data.get("weights", {})
                self.is_trained = True if self.weights else False
            except Exception:
                pass
