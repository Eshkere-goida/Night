import sqlite3
import os

def init_database():
    # Удаляем старую БД если нужно (осторожно!)
    # if os.path.exists('warehouse.db'):
    #     os.remove('warehouse.db')
    #     print("Старая БД удалена")
    
    connection = sqlite3.connect('warehouse.db')
    cursor = connection.cursor()
    
    # Создаем таблицу items
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
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
    
    # Создаем таблицу cart
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        user_id TEXT,
        item_id INTEGER,
        quantity INTEGER DEFAULT 1,
        PRIMARY KEY (user_id, item_id),
        FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
    )   
    ''')
    
    # Создаем таблицу likes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        item_id INTEGER PRIMARY KEY,
        count INTEGER DEFAULT 0,
        FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
    )
    ''')
    
    connection.commit()
    
    # Проверяем создание
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Созданные таблицы:")
    for table in tables:
        print(f"  ✓ {table[0]}")
    
    connection.close()
    print("\n✅ База данных успешно инициализирована!")

if __name__ == "__main__":
    init_database()