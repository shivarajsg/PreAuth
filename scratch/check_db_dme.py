import sqlite3
from pathlib import Path

db_path = Path('medrule_engine/governance/data/governance.db')
if not db_path.exists():
    print('medrule_governance.db does not exist')
else:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in c.fetchall()]
    print('Tables in medrule_governance.db:', tables)
    for t in tables:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = c.fetchone()[0]
        
        # Check for CP.MP.107, DME, and hashes
        c.execute(f"PRAGMA table_info({t})")
        cols = [col[1] for col in c.fetchall()]
        matches_cp = 0
        matches_dme = 0
        matches_sha = 0
        for col in cols:
            try:
                c.execute(f"SELECT COUNT(*) FROM {t} WHERE CAST({col} AS TEXT) LIKE '%CP.MP.107%'")
                matches_cp += c.fetchone()[0]
                c.execute(f"SELECT COUNT(*) FROM {t} WHERE CAST({col} AS TEXT) LIKE '%DME%'")
                matches_dme += c.fetchone()[0]
                c.execute(f"SELECT COUNT(*) FROM {t} WHERE CAST({col} AS TEXT) LIKE '%9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29%'")
                matches_sha += c.fetchone()[0]
            except Exception:
                pass
        print(f"  {t}: {cnt} rows | Matches CP.MP.107: {matches_cp} | Matches DME: {matches_dme} | Matches Hash: {matches_sha}")
