import sqlite3

connection = sqlite3.connect('warehouse.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    storage_sector INTEGER,
    weight REAL,
    quantity INTEGER,
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
    item_id INTEGER,
    count INTEGER,
    FOREIGN KEY (item_id) REFERENCES items(id)
    )''')

connection.commit()
connection.close()

print("База данных успешно создана!")
