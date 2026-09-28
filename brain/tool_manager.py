import socket
import re
import requests
import os
import platform
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import unquote, parse_qs, urlparse

class ToolManager:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def execute_tool(self, tool_name: str, param: str) -> str:
        if tool_name == "web_search":
            return self.web_search(param)
        elif tool_name == "web_fetch":
            return self.web_fetch(param)
        elif tool_name == "domain_osint":
            return self.domain_osint(param)
        elif tool_name == "github_osint":
            return self.github_osint(param)
        elif tool_name == "repo_inspect":
            return self.repo_inspect(param)
        elif tool_name == "system_info":
            return self.system_info()
        elif tool_name == "calculator":
            try:
                return f"Nəticə: {eval(param)}"
            except Exception as e:
                return f"Xəta: {e}"
        return "Alət tapılmadı."

    def clean_target_url(self, raw_input: str) -> str:
        http_match = re.search(r'https?://[^\s\]\)]+', raw_input)
        if http_match:
            return http_match.group(0).rstrip(')]}>,')
        
        domain_match = re.search(r'[a-zA-Z0-9-]+\.[a-zA-Z]{2,}[^\s\]\)]*', raw_input)
        if domain_match:
            clean = domain_match.group(0).rstrip(')]}>,')
            return "https://" + clean if not clean.startswith("http") else clean
            
        return raw_input.strip()

    def github_osint(self, username: str) -> str:
        try:
            user = username.replace("https://github.com/", "").replace("github.com/", "").strip("/ ")
            url = f"https://api.github.com/users/{user}"
            resp = requests.get(url, headers=self.headers, timeout=8)
            
            if resp.status_code == 200:
                data = resp.json()
                repos_resp = requests.get(data['repos_url'], headers=self.headers, timeout=8)
                repos_data = repos_resp.json() if repos_resp.status_code == 200 else []
                
                repo_names = [f"  • {r['name']} ({r['language'] or 'Bilinmir'})" for r in repos_data[:10]]
                repo_str = "\n".join(repo_names) if repo_names else "  • Açıq repo tapılmadı."

                output = [
                    f"### GitHub Profil OSINT ({user}):",
                    f"• Ad / Bio: {data.get('name') or 'Qeyd olunmayıb'} | {data.get('bio') or 'Bio yoxdur'}",
                    f"• Yaradılma Tarixi: {data.get('created_at', '')[:10]}",
                    f"• İzləyici / İzlənən: {data.get('followers')} / {data.get('following')}",
                    f"• İctimai Repolar ({data.get('public_repos')} ədəd):\n{repo_str}"
                ]
                return "\n".join(output)
            return f"GitHub istifadəçisi tapılmadı ({user}). Status: {resp.status_code}"
        except Exception as e:
            return f"GitHub OSINT xətası: {e}"

    def repo_inspect(self, repo_path: str) -> str:
        """Kullanıcı/repo şeklinde gelen depoyu inceler. README yoksa dosya ağacını getirir."""
        try:
            clean_path = repo_path.replace("https://github.com/", "").strip("/ ")
            
            # 1. RAW README Denemeleri
            readme_variants = ["main/README.md", "master/README.md", "main/readme.md", "master/readme.md"]
            for variant in readme_variants:
                raw_url = f"https://raw.githubusercontent.com/{clean_path}/{variant}"
                resp = requests.get(raw_url, timeout=5)
                if resp.status_code == 200:
                    return f"### '{clean_path}' README Məzmunu ({variant}):\n\n" + (resp.text[:1500] + "..." if len(resp.text) > 1500 else resp.text)
            
            # 2. README Bulunamadıysa Repo İçeriğini (Dosya Ağacını) Çek
            contents_url = f"https://api.github.com/repos/{clean_path}/contents"
            resp = requests.get(contents_url, headers=self.headers, timeout=8)
            if resp.status_code == 200:
                files = resp.json()
                file_list = [f"  • {item['name']} ({item['type']})" for item in files]
                return f"### '{clean_path}' Reposunda README tapılmadı.\n\n**Repo Fayl Siyahısı:**\n" + "\n".join(file_list)
            
            return f"'{clean_path}' reposuna giriş uğursuz oldu. Status: {resp.status_code}"
        except Exception as e:
            return f"Repo analizi xətası: {e}"

    def system_info(self) -> str:
        try:
            uname = platform.uname()
            cwd = os.getcwd()
            return f"### Sistem Məlumatı:\n• Əməliyyat Sistemi: {uname.system} {uname.release}\n• Arxitektura: {uname.machine}\n• Cari Qovluq: {cwd}"
        except Exception as e:
            return f"Sistem məlumatı alınamadı: {e}"

    def web_search(self, query: str, limit: int = 5) -> str:
        try:
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                results = soup.find_all('div', class_='result__body', limit=limit)
                
                if not results:
                    return f"'{query}' üzrə internetdə açıq məlumat tapılmadı."
                
                output = [f"### Canlı İnternet Axtarış Nəticələri ('{query}'):\n"]
                for idx, res in enumerate(results, 1):
                    title_tag = res.find('a', class_='result__a')
                    snippet_tag = res.find('a', class_='result__snippet')
                    
                    title = title_tag.text.strip() if title_tag else "Başlıq yoxdur"
                    raw_link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else ""
                    clean_link = self.clean_target_url(raw_link)
                    snippet = snippet_tag.text.strip() if snippet_tag else ""
                    
                    output.append(f"{idx}. **{title}**\n   {snippet}\n   Keçid: {clean_link}\n")
                return "\n".join(output)
            else:
                return f"Axtarış xətası (Status kodu: {resp.status_code})"
        except Exception as e:
            return f"Axtarış zamanı xəta: {e}"

    def web_fetch(self, raw_input: str) -> str:
        try:
            url = self.clean_target_url(raw_input)
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                for tag in soup(["script", "style", "nav", "footer", "header", "form", "svg"]):
                    tag.extract()
                
                main_content = soup.find("main") or soup.find("body")
                text = main_content.get_text(separator=' ', strip=True) if main_content else soup.get_text(separator=' ', strip=True)
                clean_text = " ".join(text.split())
                return f"### '{url}' Səhifəsinin Məzmunu:\n\n" + (clean_text[:1500] + "..." if len(clean_text) > 1500 else clean_text)
            return f"Sayta qoşulmaq mümkün olmadı ({url}). Status kodu: {resp.status_code}"
        except Exception as e:
            return f"Sayt oxunarkən xəta: {e}"

    def domain_osint(self, domain: str) -> str:
        try:
            clean = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
            ip_addr = socket.gethostbyname(clean)
            resp = requests.get(f"https://{clean}", headers=self.headers, timeout=8)
            server = resp.headers.get("Server", "Gizlədilib/Bilinmir")
            content_type = resp.headers.get("Content-Type", "Bilinmir")
            
            output = [
                f"### Domen OSINT Analizi ({clean}):",
                f"• IP Ünvanı: {ip_addr}",
                f"• Web Server: {server}",
                f"• Content Type: {content_type}",
                f"• HTTP Cavab Kodu: {resp.status_code}"
            ]
            return "\n".join(output)
        except Exception as e:
            return f"OSINT analizi xətası: {e}"
