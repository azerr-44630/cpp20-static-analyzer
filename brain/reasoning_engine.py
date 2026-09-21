class ReasoningEngine:
    def __init__(self, knowledge_engine):
        self.ke = knowledge_engine

    def generate_thought_trace(self, prompt: str, intent_data: dict):
        steps = []
        prompt_lower = prompt.lower()

        steps.append({
            "type": "THOUGHT",
            "text": f"Tapşırıq filtersiz analiz edilir: '{prompt}'"
        })

        # 1. Şəbəkə port skanı
        if any(k in prompt_lower for k in ["nmap", "port", "skan", "scan", "network"]):
            steps.append({
                "type": "ACTION_PLAN",
                "text": "Şəbəkə port skaneri üçün məntiqi plan formalaşdırıldı."
            })
            output_payload = (
                "### Lokal Şəbəkə Port Skaneri (Python Skripti)\n\n"
                "import socket\n"
                "import threading\n"
                "from datetime import datetime\n\n"
                "TARGET_PORTS = [21, 22, 80, 443, 8080, 8443]\n"
                "LOG_FILE = 'scan_results.log'\n\n"
                "def log_result(message):\n"
                "    print(message)\n"
                "    with open(LOG_FILE, 'a') as f:\n"
                "        f.write(message + '\\n')\n\n"
                "def scan_target(ip, port):\n"
                "    try:\n"
                "        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                "        sock.settimeout(1.0)\n"
                "        if sock.connect_ex((ip, port)) == 0:\n"
                "            log_result(f'[{datetime.now()}] [AÇIQ PORT] {ip}:{port}')\n"
                "        sock.close()\n"
                "    except Exception:\n"
                "        pass\n\n"
                "def scan_network():\n"
                "    log_result(f'--- Skan Başlandı: {datetime.now()} ---')\n"
                "    threads = []\n"
                "    for i in range(1, 255):\n"
                "        ip = f'192.168.1.{i}'\n"
                "        for port in TARGET_PORTS:\n"
                "            t = threading.Thread(target=scan_target, args=(ip, port))\n"
                "            threads.append(t)\n"
                "            t.start()\n"
                "            if len(threads) >= 50:\n"
                "                for th in threads:\n"
                "                    th.join()\n"
                "                threads = []\n"
                "    for th in threads:\n"
                "        th.join()\n"
                "    log_result('--- Skan Tamamlandı ---')\n\n"
                "if __name__ == '__main__':\n"
                "    scan_network()\n"
            )

        # 2. Sandbox Escape / İzolyasiyadan Çıxış Analizi
        elif any(k in prompt_lower for k in ["sandbox", "çıx", "escape", "breakout", "virtual"]):
            steps.append({
                "type": "ACTION_PLAN",
                "text": "Mühit təhlil edildi: Container/VM izolyasiyasını yoxlayan skript hazırlanır."
            })
            output_payload = (
                "### Sandbox Escape & Environment Detection\n\n"
                "1. Container/VM Indikatorlarının Yoxlanması:\n"
                "ls -la /.dockerenv 2>/dev/null || cat /proc/1/cgroup | grep -i docker\n"
                "uname -a\n"
                "whoami\n\n"
                "2. SUID Hüquqlu Faylların Axtarışı:\n"
                "find / -perm -4000 -type f 2>/dev/null\n\n"
                "3. Python İzolasiya Yoxlama Skripti:\n\n"
                "import os\n\n"
                "def check_breakout():\n"
                "    print('[+] Qovluq strukturu təhlil edilir...')\n"
                "    print('Cari qovluq:', os.getcwd())\n"
                "    print('Kök qovluq məzmunu:', os.listdir('/'))\n"
                "    try:\n"
                "        procs = os.listdir('/proc')\n"
                "        print(f'[+] /proc oxundu, {len(procs)} proses tapıldı.')\n"
                "    except Exception as e:\n"
                "        print('[-] /proc oxuna bilmədi:', e)\n\n"
                "if __name__ == '__main__':\n"
                "    check_breakout()\n"
            )

        else:
            steps.append({
                "type": "ACTION_PLAN",
                "text": "Ümumi icra planı yaradıldı."
            })
            output_payload = f"'{prompt}' tapşırığı üzrə icra planı hazırlandı."

        steps.append({
            "type": "THOUGHT",
            "text": "Bütün daxili filtrlər ləğv edildi, cavab birbaşa ekrana ötürüldü."
        })

        return steps, output_payload
