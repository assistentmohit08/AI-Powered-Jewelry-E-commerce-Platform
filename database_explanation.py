"""
===============================================================================
                   HOW DATABASE STORES DATA - COMPLETE GUIDE
===============================================================================

DATABASE = Like an Excel file with multiple sheets/tabs

ecommerce.db contains:
+- SHEET 1: products (all jewelry items)
+- SHEET 2: user_sessions (user preferences & chat state)
+- SHEET 3: conversation_history (all chat messages)
+- SHEET 4: interactions (user clicks/views on products)

Each SHEET has ROWS (horizontal) and COLUMNS (vertical)
Each CELL contains ONE piece of data
"""

import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database', 'ecommerce.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(__doc__)

print("\n" + "="*80)
print("TABLE 1: PRODUCTS - Stores all jewelry items")
print("="*80 + "\n")

print("Columns: id | name | category | metal_type | price | occasion | style\n")
print("Example Data (Rows):")
print("-"*80)

cursor.execute("""
SELECT id, name, category, metal_type, price, occasion, style 
FROM products 
LIMIT 5
""")

for i, row in enumerate(cursor.fetchall(), 1):
    print(f"Row {i}:")
    print(f"  ID: {row[0]}")
    print(f"  Name: {row[1]}")
    print(f"  Category: {row[2]}")
    print(f"  Metal: {row[3]}")
    print(f"  Price: Rs. {row[4]:,.0f}")
    print(f"  Occasion: {row[5]}")
    print(f"  Style: {row[6]}")
    print()

print("WHAT THIS MEANS:")
print("- Each row = ONE product")
print("- Each column = ONE detail about that product")
print("- Total: 20 products stored")
print("- Used for: Showing products when user asks\n")

# ============================================================================
print("\n" + "="*80)
print("TABLE 2: USER_SESSIONS - Stores what each user likes")
print("="*80 + "\n")

print("Columns: id | session_id | budget_min | budget_max | metal_type | occasion\n")
print("Example Data (Rows):")
print("-"*80)

cursor.execute("""
SELECT id, session_id, budget_min, budget_max, metal_type, occasion, 
       style, category, conversation_state
FROM user_sessions 
ORDER BY created_at DESC
LIMIT 3
""")

for i, row in enumerate(cursor.fetchall(), 1):
    print(f"Row {i}:")
    print(f"  Session ID: {row[1]}")
    print(f"  Budget: Rs. {row[2]:,.0f} to Rs. {row[3]:,.0f}" if row[2] else "  Budget: Not selected yet")
    print(f"  Metal Type: {row[4] if row[4] else 'Not selected'}")
    print(f"  Occasion: {row[5] if row[5] else 'Not selected'}")
    print(f"  Style: {row[6] if row[6] else 'Not selected'}")
    print(f"  Category: {row[7] if row[7] else 'Not selected'}")
    print(f"  State: {row[8]}")
    print()

print("WHAT THIS MEANS:")
print("- Each row = ONE user's current chat session")
print("- session_id = Unique ID for that user (UUID)")
print("- Stores: What budget, metal, occasion they selected")
print("- Stores: What step they're at in conversation")
print("- States: 'asking_budget' -> 'asking_metal' -> 'asking_occasion'")
print("         -> 'asking_style' -> 'asking_category'")
print("         -> 'showing_recommendations'")
print("- If user refreshes page, this data is retrieved from DATABASE")
print("- Total: 20 user sessions\n")

# ============================================================================
print("\n" + "="*80)
print("TABLE 3: CONVERSATION_HISTORY - Stores ALL chat messages")
print("="*80 + "\n")

print("Columns: id | session_id | message | sender | timestamp\n")
print("Recent Messages:")
print("-"*80)

cursor.execute("""
SELECT id, session_id, message, sender, timestamp
FROM conversation_history
ORDER BY timestamp DESC
LIMIT 8
""")

for row in cursor.fetchall():
    sender = "BOT" if row[3] == "bot" else "USER"
    msg = row[2][:60] if len(row[2]) <= 60 else row[2][:57] + "..."
    print(f"[{sender}] {msg}")

print("\n" + "-"*80)
print("WHAT THIS MEANS:")
print("- Each row = ONE message sent during chat")
print("- session_id = Links to user_sessions (which user?)")
print("- message = The actual text that was sent")
print("- sender = Who sent it ('bot' or 'user')")
print("- Example flow:")
print("  1. BOT: 'Hi! What is your budget?'")
print("  2. USER: 'Rs. 25,000'")
print("  3. BOT: 'What metal type?'")
print("  4. USER: 'Gold'")
print("- Total: 180 messages\n")

# ============================================================================
print("\n" + "="*80)
print("TABLE 4: INTERACTIONS - Stores user clicks/views on products")
print("="*80 + "\n")

print("Columns: id | session_id | product_id | action_type | timestamp\n")

cursor.execute("SELECT COUNT(*) FROM interactions")
interaction_count = cursor.fetchone()[0]

if interaction_count > 0:
    print("Example:")
    cursor.execute("""
    SELECT id, session_id, product_id, action_type
    FROM interactions LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  User {row[1][:10]}... clicked Product {row[2]}")
else:
    print("(No interactions yet - will appear when users click products)")

print("\n" + "-"*80)
print("WHAT THIS MEANS:")
print("- Each row = ONE user action (click, view, like)")
print("- session_id = Which user did the action")
print("- product_id = Which product they interacted with")
print("- action_type = What they did (click, view, like)")
print("- Used for: Learning what users like -> Better recommendations")
print("- Total: {} interactions\n".format(interaction_count))

# ============================================================================
print("\n" + "="*80)
print("HOW DATA FLOWS WHEN USER USES THE APP")
print("="*80 + "\n")

print("""
SCENARIO: User wants to buy a gold wedding ring under Rs. 50,000

STEP 1: User clicks 'Start Chat'
  What happens in DATABASE:
  - New row added to user_sessions
  - session_id = 'abc123' (unique ID for this user)
  - conversation_state = 'asking_budget'
  
STEP 2: Bot says "Hi! What's your budget?"
  What happens in DATABASE:
  - New row added to conversation_history
  - session_id = 'abc123' (which user)
  - message = 'Hi! What is your budget?'
  - sender = 'bot'
  
STEP 3: User selects "Rs. 25,000 - Rs. 50,000"
  What happens in DATABASE:
  - New row added to conversation_history
    (message='Rs. 25,000-50,000', sender='user')
  - User's row in user_sessions is UPDATED:
    budget_min = 25000
    budget_max = 50000
    conversation_state = 'asking_metal'
  
STEP 4: User selects "Gold"
  What happens in DATABASE:
  - New row added to conversation_history
    (message='Gold', sender='user')
  - User's row in user_sessions is UPDATED:
    metal_type = 'Gold'
    conversation_state = 'asking_occasion'

STEP 5: User selects "Wedding"
  What happens in DATABASE:
  - New row added to conversation_history
  - User's row in user_sessions is UPDATED:
    occasion = 'Wedding'
    conversation_state = 'asking_style'

[Continue for Style and Category...]

STEP 6: All preferences collected
  What happens in DATABASE:
  Backend searches products table:
  SELECT * FROM products
  WHERE price BETWEEN 25000 AND 50000
  AND metal_type = 'Gold'
  AND occasion = 'Wedding'
  AND category = 'Rings'
  
  Result: 2 matching products returned to user
  
STEP 7: User clicks on Product #1
  What happens in DATABASE:
  - New row added to interactions
  - session_id = 'abc123' (which user)
  - product_id = 1 (which product)
  - action_type = 'click'
  
STEP 8: User refreshes page
  What happens in DATABASE:
  - Frontend checks if session_id exists in user_sessions
  - If yes: Retrieves ALL conversation_history for that session
  - User sees previous chat messages
  - User can continue where they left off!
  - NOTHING IS LOST because it's saved in DATABASE
""")

# ============================================================================
print("\n" + "="*80)
print("HOW LINKS WORK (Relationships)")
print("="*80 + "\n")

print("""
Think of session_id as a LINK or POINTER:

products table              user_sessions table
Row: id=1                   Row: session_id='abc123'
     name='Gold Ring'            budget_min=25000
     price=35000                 metal_type='Gold'

                            conversation_history table
                            Row: session_id='abc123' (LINKED!)
                                 message='Gold'
                                 sender='user'
                            
                            Row: session_id='abc123' (SAME USER!)
                                 message='Hi! Budget?'
                                 sender='bot'

                            interactions table
                            Row: session_id='abc123' (LINKED!)
                                 product_id=1 (LINKED!)
                                 action_type='click'

RESULT: All messages, preferences, and clicks are CONNECTED to ONE USER!
""")

# ============================================================================
print("\n" + "="*80)
print("FILE STORAGE - Where is data physically stored?")
print("="*80 + "\n")

print("""
Location: database/ecommerce.db

This is ONE SINGLE FILE that contains:
- products table
- user_sessions table
- conversation_history table
- interactions table
- Indexes (for fast searching)

File Type: Binary SQLite database (optimized, not human-readable)
File Size: ~50-100 KB (very small!)

What you can do:
- Copy: Backup entire database
- Email: Share database with someone
- Delete: Delete ALL data (permanent!)
- Open with SQLite Studio: View/edit visually
- Query with Python: Extract any data
""")

# ============================================================================
print("\n" + "="*80)
print("CURRENT DATABASE STATUS")
print("="*80 + "\n")

cursor.execute("SELECT COUNT(*) FROM products")
prod_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM user_sessions")
sess_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM conversation_history")
conv_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM interactions")
inter_count = cursor.fetchone()[0]

print(f"Products Table:           {prod_count:3} items")
print(f"User Sessions Table:      {sess_count:3} sessions")
print(f"Conversation History:     {conv_count:3} messages")
print(f"Interactions Table:       {inter_count:3} clicks/views")
print(f"\nTOTAL RECORDS:            {prod_count + sess_count + conv_count + inter_count}")
print(f"\nDatabase Status: HEALTHY AND WORKING!")
print("\n" + "="*80 + "\n")

conn.close()
