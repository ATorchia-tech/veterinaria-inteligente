import sqlite3
import json

DB = 'app.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
print('tables:', tables)

rows = cur.execute("PRAGMA table_info('appointments');").fetchall()
cols = [dict(zip(['cid','name','type','notnull','dflt_value','pk'], row)) for row in rows]
print('appointments columns:')
print(json.dumps(cols, indent=2, ensure_ascii=False))

conn.close()
