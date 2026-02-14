import sqlite3
import os
import shutil

# 1. Connect to DB
db_path = 'db.sqlite3'
if not os.path.exists(db_path):
    print("DB not found!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 2. Get list of LMS tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'lms_%';")
tables = cursor.fetchall()

# 3. Drop tables
print("Dropping tables...")
for table in tables:
    table_name = table[0]
    print(f"Dropping {table_name}...")
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# 4. Clear django_migrations for 'lms'
print("Clearing migration history...")
cursor.execute("DELETE FROM django_migrations WHERE app='lms'")

conn.commit()
conn.close()
print("Database cleaned.")

# 5. Delete migration files
migrations_dir = os.path.join('lms', 'migrations')
if os.path.exists(migrations_dir):
    for filename in os.listdir(migrations_dir):
        if filename != '__init__.py' and filename != '__pycache__':
            file_path = os.path.join(migrations_dir, filename)
            print(f"Deleting {file_path}")
            os.remove(file_path)

print("Migration files deleted.")
