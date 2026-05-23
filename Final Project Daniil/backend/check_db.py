import sqlite3

def check_database():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    # Проверяем все таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Существующие таблицы:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Проверяем содержимое items если таблица существует
    try:
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        print(f"\nКоличество записей в таблице items: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM items LIMIT 3")
            rows = cursor.fetchall()
            print("\nПример данных:")
            for row in rows:
                print(f"  {row}")
    except sqlite3.OperationalError as e:
        print(f"\n❌ Таблица items не существует: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_database()