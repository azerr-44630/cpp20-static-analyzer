import re

DOMAIN_RE = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b')
IP_RE = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

def extract_target(text):
    ip_match = IP_RE.search(text)
    if ip_match:
        return ip_match.group()
    domain_match = DOMAIN_RE.search(text)
    if domain_match:
        return domain_match.group()
    return None
