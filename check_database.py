import sqlite3
import os

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'database', 'ecommerce.db')

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("📊 DATABASE CONTENTS CHECK")
print("=" * 80)

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if not tables:
    print("❌ NO TABLES FOUND - Database might not be initialized")
else:
    print(f"\n✅ Found {len(tables)} tables:\n")
    
    for table_name in tables:
        table = table_name[0]
        print(f"\n{'─' * 80}")
        print(f"📋 TABLE: {table.upper()}")
        print(f"{'─' * 80}")
        
        # Count rows
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"Total Records: {count}")
        
        if count > 0:
            # Get column info
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            col_names = [col[1] for col in columns]
            print(f"Columns: {', '.join(col_names)}\n")
            
            # Show data (limit to first 5 rows)
            cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
            rows = cursor.fetchall()
            
            for i, row in enumerate(rows, 1):
                print(f"  Row {i}: {row}")
            
            if count > 5:
                print(f"  ... and {count - 5} more rows")
        else:
            print("  (No data in this table)")

print("\n" + "=" * 80)
print("✨ Check complete!")
print("=" * 80)

conn.close()
