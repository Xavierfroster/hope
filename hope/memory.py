import sqlite3
import datetime
import os
from hope import config

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
    
    # Learned Data (replacing JSONs eventually)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            trigger TEXT PRIMARY KEY,
            response TEXT,
            type TEXT -- 'phrase' or 'alias'
        )
    ''')
    
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

# Initialize on import
init_db()
