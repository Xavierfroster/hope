import sqlite3
import datetime
import os
from hope.configuration import settings as config

def init_db():
    if not os.path.exists(config.LEARNING_DIR):
        os.makedirs(config.LEARNING_DIR)
    
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    # History table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            query TEXT,
            response TEXT
        )
    ''')
    
    # Preferences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Contacts table for emails and whatsapp
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            name TEXT PRIMARY KEY,
            email TEXT,
            phone TEXT
        )
    ''')

    # Ensure phone column exists for users upgrading from older versions
    try:
        cursor.execute("ALTER TABLE contacts ADD COLUMN phone TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists
    
    conn.commit()
    conn.close()

def log_conversation(query, response):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (timestamp, query, response) VALUES (?, ?, ?)", 
                   (datetime.datetime.now(), query, response))
    conn.commit()
    conn.close()

def set_preference(key, value):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()

def get_preference(key, default=None):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else default

def get_recent_history(limit=5):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT query, response FROM history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_history(keyword):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT query, response FROM history WHERE query LIKE ? OR response LIKE ? ORDER BY id DESC", 
                   (f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def count_actions(keyword):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM history WHERE query LIKE ?", (f'%{keyword}%',))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def save_contact(name, email):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, email) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET email=excluded.email", (name.lower(), email.lower()))
    conn.commit()
    conn.close()

def get_contact(name):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM contacts WHERE name = ?", (name.lower(),))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_phone(name, phone):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET phone=excluded.phone", (name.lower(), phone))
    conn.commit()
    conn.close()

def get_phone(name):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT phone FROM contacts WHERE name = ?", (name.lower(),))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Initialize on import
init_db()
