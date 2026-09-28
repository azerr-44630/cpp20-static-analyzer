import os

ACCEPT_FILE = ".license_accepted"

def ensure_accepted():
    if os.path.exists(ACCEPT_FILE):
        return True

    print(open("LICENSE_AGREEMENT.txt", encoding="utf-8").read())
    answer = input("\nŞərtləri qəbul edirsinizmi? (bəli/xeyr): ").strip().lower()

    if answer in ("bəli", "beli", "yes", "y"):
        with open(ACCEPT_FILE, "w") as f:
            f.write("accepted")
        return True

    print("Şərtlər qəbul edilmədi. Proqram bağlanır.")
    exit(1)
