import re

def load_allowlist(path="targets.txt"):
    targets = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                targets.add(line)
    return targets

def is_allowed(target, allowlist):
    # dəqiq uyğunluq və ya subdomain uyğunluğu
    target = target.strip().lower()
    for allowed in allowlist:
        allowed = allowed.lower()
        if target == allowed or target.endswith("." + allowed):
            return True
    return False

def check_or_block(target):
    allowlist = load_allowlist()
    if not allowlist:
        print("[!] targets.txt boşdur. Əvvəlcə icazəli hədəf əlavə edin.")
        exit(1)
    if not is_allowed(target, allowlist):
        print(f"[!] '{target}' allowlist-də deyil. Əməliyyat dayandırıldı.")
        exit(1)
    return True
