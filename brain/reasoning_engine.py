import re
from core.skill_loader import load_skills
from brain.tool_manager import ToolManager

class ReasoningEngine:
    def __init__(self, knowledge_engine):
        self.ke = knowledge_engine
        self.skills = load_skills()
        self._url_tool = ToolManager()

    def _process_single(self, prompt: str, intent_data: dict):
        steps = []
        output_payload = ""

        steps.append({
            "type": "THOUGHT",
            "text": f"Tapşırıq daxil oldu: '{prompt}'"
        })

        prompt_lower = prompt.lower()

        # 1. GitHub Repo İnceleme (ör. github.com/kullanici/repo veya repo oku/bax)
        if "github.com/" in prompt_lower and prompt_lower.count("/") >= 2:
            repo_match = re.search(r'github\.com/([a-zA-Z0-9-]+/[a-zA-Z0-9-_]+)', prompt)
            if repo_match:
                repo_path = repo_match.group(1)
                steps.append({"type": "THOUGHT", "text": f"GitHub deponuz tespit edildi: '{repo_path}'"})
                res = self.skills["repo_inspect"].run(repo_path=repo_path)
                output_payload = res
                steps.append({"type": "OBSERVATION", "text": "Depo README dosyası incelendi."})

        # 2. GitHub Profil Analizi
        elif "github.com/" in prompt_lower or ("github" in prompt_lower and "/" in prompt_lower):
            user_match = re.search(r'github\.com/([a-zA-Z0-9-]+)', prompt)
            username = user_match.group(1) if user_match else prompt
            steps.append({"type": "THOUGHT", "text": f"GitHub profili tespit edildi: '{username}'"})
            res = self.skills["github_osint"].run(username=username)
            output_payload = res
            steps.append({"type": "OBSERVATION", "text": "Profil verileri API üzerinden çekildi."})

        # 3. Sistem Bilgisi Sorgusu
        elif any(k in prompt_lower for k in ["sistem", "termux", "specs", "donanım", "sistem bilgisi"]):
            steps.append({"type": "THOUGHT", "text": "Sistem bilgileri toplanıyor..."})
            res = self.skills["system_info"].run()
            output_payload = res
            steps.append({"type": "OBSERVATION", "text": "Sistem detayları çekildi."})

        # 4. Genel URL İnceleme
        elif re.search(r'(https?://[^\s\]\)]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s\]\)]*)?)', prompt) and ("/" in prompt or "http" in prompt_lower or "oxu" in prompt_lower):
            url_match = re.search(r'(https?://[^\s\]\)]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s\]\)]*)?)', prompt)
            raw_url = url_match.group(0)
            clean_url = self._url_tool.clean_target_url(raw_url)
            steps.append({"type": "THOUGHT", "text": f"Sayfa içeriği çekiliyor: '{clean_url}'"})
            res = self.skills["web_fetch"].run(url=clean_url)
            output_payload = res
            steps.append({"type": "OBSERVATION", "text": "İçerik okundu."})

        # 5. Domain OSINT
        elif any(k in prompt_lower for k in ["osint", "ip", "server", "header", "domen təhlil", "skan", "scan", "yoxla", "test et", "audit"]):
            domains = re.findall(r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', prompt)
            domain = domains[0] if domains else prompt
            steps.append({"type": "THOUGHT", "text": f"Domen OSINT analizi icra olunur: '{domain}'"})
            res = self.skills["domain_osint"].run(domain=domain)
            output_payload = res
            steps.append({"type": "OBSERVATION", "text": "OSINT analizi tamamlandı."})

        # 6. Canlı Web Araması
        else:
            steps.append({"type": "THOUGHT", "text": f"İnternetdə canlı axtarış aparılır: '{prompt}'"})
            search_res = self.skills["web_search"].run(query=prompt)
            output_payload = search_res
            steps.append({"type": "OBSERVATION", "text": "İnternet axtarışı yekunlaşdı."})

        steps.append({"type": "THOUGHT", "text": "Həll tamamlandı."})
        return steps, output_payload

    def generate_thought_trace(self, prompt: str, intent_data: dict, max_steps: int = 5):
        import re as _re
        parts = _re.split(r'\bsonra\b|\bve sonra\b|;', prompt, flags=_re.IGNORECASE)
        parts = [p.strip() for p in parts if p.strip()]

        if len(parts) <= 1:
            return self._process_single(prompt, intent_data)

        parts = parts[:max_steps]
        all_steps = []
        all_outputs = []

        all_steps.append({"type": "THOUGHT", "text": f"Tapşırıq {len(parts)} addıma bölündü."})

        for idx, part in enumerate(parts, 1):
            all_steps.append({"type": "THOUGHT", "text": f"[{idx}/{len(parts)}] addım icra olunur: '{part}'"})
            sub_steps, sub_output = self._process_single(part, intent_data)
            all_steps.extend(sub_steps)
            all_outputs.append(f"--- Addım {idx} nəticəsi ---\n{sub_output}")

        all_steps.append({"type": "THOUGHT", "text": "Bütün addımlar tamamlandı."})
        return all_steps, "\n\n".join(all_outputs)
