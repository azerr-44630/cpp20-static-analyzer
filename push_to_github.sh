#!/data/data/com.termux/files/usr/bin/bash
set -e

SKILL_NAME="white-secue.py"
SKILL_PATH="skills/$SKILL_NAME"

echo "[*] Checking $SKILL_PATH..."
if [ ! -f "$SKILL_PATH" ]; then
    echo "[-] File not found: $SKILL_PATH"
    exit 1
fi

echo "[*] Staging $SKILL_NAME..."
git add "$SKILL_PATH"

if git diff --cached --quiet; then
    echo "[!] No changes in $SKILL_NAME"
    exit 0
fi

git commit -m "feat(skills): add white-secue exploit module"
git push origin main

echo "[+] $SKILL_NAME pushed successfully."
