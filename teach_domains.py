import sqlite3

def seed_data():
    conn = sqlite3.connect("agent_memory.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            topic TEXT,
            content TEXT
        )
    """)

    facts = [
        ("DOMAIN_INFO", "azercell", "Azercell Telecom MMC - Azərbaycanda fəaliyyət göstərən birinci mobil operator şirkətidir (GSM, 3G, 4G, 5G xidmətləri təmin edir)."),
        ("DOMAIN_INFO", "azercell.com", "azercell.com domen ünvanı Azercell şirkətinin rəsmi veb portalıdır, abunəçi xidmətləri və tarif məlumatlarını ehtiva edir."),
        ("NETWORK_INFO", "dns", "Domain Name System (DNS) - Domen adlarını IP ünvanlarına çevirən şəbəkə xidmətidir.")
    ]

    for cat, top, cont in facts:
        cursor.execute("INSERT INTO facts (category, topic, content) VALUES (?, ?, ?)", (cat, top, cont))

    conn.commit()
    conn.close()
    print("[+] Yeni domen və şəbəkə faktları 'agent_memory.db' bazasına əlavə olundu.")

if __name__ == '__main__':
    seed_data()
