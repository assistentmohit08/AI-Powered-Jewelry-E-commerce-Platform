import sqlite3
import os

db = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database', 'ecommerce.db'))
c = db.cursor()

# Quick overview
print("\n📊 DATABASE QUICK CHECK\n")
for table in ['products', 'user_sessions', 'conversation_history', 'interactions']:
    c.execute(f"SELECT COUNT(*) FROM {table}")
    count = c.fetchone()[0]
    print(f"  {table:<25} → {count} records")

db.close()
