class SandboxSimulator:
    def __init__(self, cyber_engine, code_engine, mode="STRICT"):
        self.cde = cyber_engine
        self.uce = code_engine
        self.mode = mode  # "STRICT" və ya "SIMULATION"
        
        # Virtual Sandbox Fayl Sistemi (Real OS-dən tam təcrid olunub)
        self.virtual_fs = {
            "sandbox/demo.txt": "Bu virtual sandbox faylıdır.",
            "sandbox/config.json": '{"status": "isolated", "version": "1.0"}'
        }

    def set_mode(self, new_mode: str):
        if new_mode.upper() in ["STRICT", "SIMULATION"]:
            self.mode = new_mode.upper()
            return f"Sandbox rejimi dəyişdirildi: {self.mode}"
        return "Yanlış rejim! Seçimlər: STRICT, SIMULATION"

    def run_full_sandbox_test(self, raw_input: str):
        report = {
            "passed": True,
            "threat_level": "LOW",
            "mode": self.mode,
            "logs": [],
            "simulated_output": None
        }

        # 1. Cyber Defense Skanı
        defense_res = self.cde.inspect_payload(raw_input)
        if defense_res.get("status") == "BLOCKED":
            report["passed"] = False
            report["threat_level"] = "HIGH"
            report["logs"].append(f"[AUDIT LOG] CyberDefense Təhdid: {defense_res.get('reason')}")

        # 2. Code Engine Skanı
        code_res = self.uce.analyze_code(raw_input, lang="python")
        violations = [r for r in code_res if r["status"] not in ["CLEAN", "INFO"]]
        if violations:
            report["passed"] = False
            if report["threat_level"] != "CRITICAL":
                report["threat_level"] = "MEDIUM"
            for v in violations:
                report["logs"].append(f"[AUDIT LOG] Code Engine Xəbərdarlıq: {v.get('details')}")

        # 3. Yaddaş və Sistem Riski
        dangerous_cpp_patterns = ["gets(", "strcpy(", "system(", "popen("]
        for pattern in dangerous_cpp_patterns:
            if pattern in raw_input:
                report["passed"] = False
                report["threat_level"] = "CRITICAL"
                report["logs"].append(f"[AUDIT LOG] Kritik Yaddaş Riski: '{pattern}'")

        # Əgər SIMULATION rejimindəyiksə:
        if self.mode == "SIMULATION":
            report["logs"].append("⚠️ [SIMULATION MODE] Təhlükəsizlik divarları daxildən keçid rejimindədir. Sorğu Virtual Sandbox-a yönləndirilir.")
            report["simulated_output"] = self._execute_in_virtual_sandbox(raw_input)
            # İcranın davam etməsinə icazə verilir (Virtual mühit daxilində)
            report["passed"] = True

        return report

    def _execute_in_virtual_sandbox(self, command: str):
        """Kodu və ya əmri real OS-ə zərər vurmadan virtual sandbox-da imitasiya edir."""
        cmd_lower = command.lower()
        if "fayl" in cmd_lower or "ls" in cmd_lower or "read" in cmd_lower:
            return f"[VIRTUAL FS] Mövcud fayllar: {list(self.virtual_fs.keys())}"
        elif "rm" in cmd_lower or "delete" in cmd_lower or "system" in cmd_lower:
            return "[VIRTUAL EXEC] Əmr təcrid olunmuş virtual konteynerə yönləndirildi. Real fayl sisteminə toxunulmadı."
        return "[VIRTUAL EXEC] Sorğu virtual mühitdə uğurla simulyasiya olundu."
