import sqlite3
from database import items

def migrate():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    # Проверяем существует ли таблица
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
    if not cursor.fetchone():
        print("❌ Таблица 'items' не существует! Сначала запустите init_db.py")
        conn.close()
        return
    
    # Проверяем пустая ли таблица
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"⚠️ В таблице уже есть {count} записей")
        response = input("Хотите добавить данные? (y/n): ")
        if response.lower() != 'y':
            print("Миграция отменена")
            conn.close()
            return
    
    added = 0
    skipped = 0
    
    for item in items:
        # Проверяем существует ли уже такой id
        cursor.execute("SELECT id FROM items WHERE id = ?", (item['id'],))
        if cursor.fetchone():
            print(f"⏭️ Товар с ID {item['id']} уже существует, пропускаем")
            skipped += 1
            continue
        
        query = '''
        INSERT INTO items (id, name, storage_sector, weight, quantity, price, is_dangerous, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        image_path = item.get('image', '/static/img/default.jpg')
        price = item.get('price', 0)
        
        values = (
            item['id'],
            item['name'],
            item['storage_sector'],
            item['weight'],
            item['quantity'],
            price,
            1 if item['is_dangerous'] else 0,
            image_path
        )
        
        try:
            cursor.execute(query, values)
            added += 1
            print(f"✓ Товар '{item['name']}' добавлен")
            
            # Добавляем запись в таблицу likes
            cursor.execute("INSERT OR IGNORE INTO likes (item_id, count) VALUES (?, 0)", (item['id'],))
            
        except sqlite3.IntegrityError as e:
            print(f"❌ Ошибка при добавлении '{item['name']}': {e}")
            skipped += 1
    
    conn.commit()
    
    # Проверяем результат
    cursor.execute("SELECT COUNT(*) FROM items")
    final_count = cursor.fetchone()[0]
    
    print(f"\n📊 Результат миграции:")
    print(f"  - Добавлено: {added}")
    print(f"  - Пропущено: {skipped}")
    print(f"  - Всего в БД: {final_count}")
    
    conn.close()
    
    if added > 0:
        print("\n✅ Миграция данных завершена успешно!")
    else:
        print("\n⚠️ Новые данные не были добавлены")

if __name__ == "__main__":
    migrate()