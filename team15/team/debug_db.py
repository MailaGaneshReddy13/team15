import sqlite3
import os

db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print(f"Database file {db_path} not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in database:")
    lms_tables = []
    for table in tables:
        print(f"- {table[0]}")
        if table[0].startswith('lms_'):
            lms_tables.append(table[0])
            
    print(f"\nLMS Tables found: {lms_tables}")
    conn.close()
