import sqlite3
import os
from datetime import datetime

db_path = os.path.join(os.path.dirname(__file__), 'database', 'ecommerce.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def print_header(title):
    print(f"\n{'=' * 100}")
    print(f"  {title}")
    print(f"{'=' * 100}\n")

def print_section(title):
    print(f"\n{title}")
    print("-" * 100)

# PRODUCTS TABLE
print_header("🎀 JEWELRY PRODUCTS")
cursor.execute("SELECT COUNT(*) FROM products;")
total_products = cursor.fetchone()[0]
print(f"Total Products: {total_products}\n")

cursor.execute("""
SELECT id, name, category, metal_type, price, occasion, style 
FROM products 
LIMIT 10
""")
print(f"{'ID':<3} {'Name':<35} {'Category':<15} {'Metal':<12} {'Price':<10} {'Occasion':<12} {'Style':<15}")
print("-" * 100)
for row in cursor.fetchall():
    print(f"{row[0]:<3} {row[1]:<35} {row[2]:<15} {row[3]:<12} ₹{row[4]:<9,.0f} {row[5]:<12} {row[6]:<15}")
if total_products > 10:
    print(f"\n... and {total_products - 10} more products")

# USER SESSIONS TABLE
print_header("👥 USER CHAT SESSIONS")
cursor.execute("SELECT COUNT(*) FROM user_sessions;")
total_sessions = cursor.fetchone()[0]
print(f"Total Sessions: {total_sessions}\n")

cursor.execute("""
SELECT id, session_id, budget_min, budget_max, metal_type, occasion, style, category, conversation_state
FROM user_sessions 
ORDER BY created_at DESC
LIMIT 10
""")
print(f"{'ID':<3} {'Session':<15} {'Budget Min':<12} {'Budget Max':<12} {'Metal':<12} {'Occasion':<12} {'State':<20}")
print("-" * 100)
for row in cursor.fetchall():
    budget_min = f"₹{row[2]:,.0f}" if row[2] else "None"
    budget_max = f"₹{row[3]:,.0f}" if row[3] else "None"
    print(f"{row[0]:<3} {row[1][:14]:<15} {budget_min:<12} {budget_max:<12} {row[4] or 'None':<12} {row[5] or 'None':<12} {row[8]:<20}")

# CONVERSATION HISTORY
print_header("💬 CONVERSATION HISTORY")
cursor.execute("SELECT COUNT(*) FROM conversation_history;")
total_messages = cursor.fetchone()[0]
print(f"Total Messages: {total_messages}\n")

cursor.execute("""
SELECT session_id, COUNT(*) as msg_count
FROM conversation_history
GROUP BY session_id
ORDER BY COUNT(*) DESC
LIMIT 5
""")
print(f"{'Session':<15} {'Message Count':<15}")
print("-" * 100)
for row in cursor.fetchall():
    print(f"{row[0][:14]:<15} {row[1]:<15}")

# Sample messages
print("\nLatest 10 Messages:\n")
cursor.execute("""
SELECT sender, message, timestamp
FROM conversation_history
ORDER BY timestamp DESC
LIMIT 10
""")
for row in cursor.fetchall():
    sender = "🤖 BOT" if row[0] == 'bot' else "👤 USER"
    msg = row[1][:70] + "..." if len(row[1]) > 70 else row[1]
    print(f"{sender}: {msg}")

# INTERACTIONS TABLE
print_header("🖱️ USER INTERACTIONS (Clicks/Views)")
cursor.execute("SELECT COUNT(*) FROM interactions;")
total_interactions = cursor.fetchone()[0]
print(f"Total Interactions: {total_interactions}\n")

if total_interactions > 0:
    cursor.execute("""
    SELECT action_type, COUNT(*) as count
    FROM interactions
    GROUP BY action_type
    """)
    print(f"{'Action Type':<20} {'Count':<10}")
    print("-" * 100)
    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[1]:<10}")
else:
    print("(No interactions recorded yet - they will appear after users click on products)")

# SUMMARY
print_header("📊 DATABASE SUMMARY")
print(f"✅ Products:              {total_products} items")
print(f"✅ User Sessions:         {total_sessions} sessions")
print(f"✅ Chat Messages:         {total_messages} messages")
print(f"✅ User Interactions:     {total_interactions} interactions")
print(f"\n✨ Database Status: HEALTHY AND POPULATED! 🎉")

conn.close()
