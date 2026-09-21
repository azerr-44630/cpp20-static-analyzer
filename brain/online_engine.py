import urllib.request
import urllib.parse
import re

class OnlineEngine:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def fetch_web_data(self, query: str):
        """İnternetdən məlumat çəkir və artıq boşluqları/HTML qalıqlarını təmizləyir."""
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                html = response.read().decode('utf-8')
                
                # 1. HTML teqlərini silirik
                clean_text = re.sub(r'<[^<]+?>', ' ', html)
                
                # 2. Bütün ardıcıl boşluqları, \n, \r, \t simvollarını tək boşluqla əvəz edirik
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                
                # 3. Lazımsız interfeys sözlərini filtrələyirik
                ignore_words = ["Submit", "Images not loading", "DuckDuckGo", "error-lite"]
                for word in ignore_words:
                    clean_text = clean_text.replace(word, "")
                
                # 4. Yenidən boşluqları təmizləyirik
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                
                # Nəticədən ilk 300 simvolluq səliqəli xülasə qaytarırıq
                return clean_text[:300] + "..." if len(clean_text) > 300 else clean_text
        except Exception as e:
            return f"[WEB ERROR] İnternetdən məlumat çəkilə bilmədi: {e}"
