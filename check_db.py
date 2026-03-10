import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Listar tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tablas:", tables)

if tables:
    # Ver estructura de appointments
    cursor.execute("PRAGMA table_info(appointments)")
    info = cursor.fetchall()
    print("\nEstructura de appointments:")
    for row in info:
        print(f"  {row[1]} ({row[2]})")

conn.close()
