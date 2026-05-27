import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'warehouse.db')
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
    
   
cursor.execute('''    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        storage_sector INTEGER,
        weight REAL,
        quantity INTEGER,
        price REAL DEFAULT 0,
        is_dangerous INTEGER DEFAULT 0,
        image TEXT
    )
''')
    
    
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        user_id TEXT,
        item_id INTEGER,
        quantity INTEGER DEFAULT 1,
        PRIMARY KEY (user_id, item_id),
        FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
    )   
''')
    
    
cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        item_id INTEGER PRIMARY KEY,
        count INTEGER DEFAULT 0,
        FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
    )
''')
    
connection.commit()
    
