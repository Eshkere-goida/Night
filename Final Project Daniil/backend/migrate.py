import sqlite3
from database import items

def migrate():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    for item in items:
        query = '''
        INSERT INTO items(id,name,storage_sector,weight,quantity,is_dangerous,image)
        VALUES  (?,?,?,?,?,?,?)'''
        
        image_path = item.get('image','/static/img/default.jpg')
        
        values = (
            item['id'],
            item['name'],
            item['storage_sector'],
            item['weight'],
            item['quantity'],
            1 if item['is_dangerous'] else 0,
            image_path
        )
        
        try:
            cursor.execute(query,values)
            print(f"Товар '{item['name']} успешно перенесен.")
        except sqlite3.IntegrityError:
            print(f"Товар с ID {item['id']} уже существует в базе данных!")
    
    conn.commit()
    conn.close()
    
    print("Миграция данных завершена!")
    
if __name__ == "__main__":
    migrate()    
        
    