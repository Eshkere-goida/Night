import sqlite3
import shutil
from fastapi import FastAPI, HTTPException, UploadFile,File,Form,Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этот код выполняется при запуске сервера
    print("🔄 Инициализация базы данных...")
    
    # Проверяем и создаем таблицы если нужно
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Проверяем существование таблицы items
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        if not cursor.fetchone():
            print("📋 Создание таблиц...")
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
            
            conn.commit()
            print("✅ Таблицы созданы")
        else:
            print("✅ Таблицы уже существуют")
    
    yield
    # Этот код выполняется при остановке сервера
    print("👋 Завершение работы сервера")

app = FastAPI(
    title="Digital Inventory System",
    description="Система управления складом будущего.",
    version="1.1.6"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ItemUpdate(BaseModel):
    name: str
    storage_sector: int
    weight: float 
    quantity: int
    is_dangerous: bool
    image: str | None = None
    
def get_db_connection():
    db_path = 'warehouse.db'
    print(f"🔍 Подключение к БД: {os.path.abspath(db_path)}")  # Отладка
    print(f"📁 Файл существует: {os.path.exists(db_path)}")   # Отладка
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def format_db_row(rows):
    return [dict(row) for row in rows]

def get_stats() -> Dict[str, Any]:
    """Возвращает статистику в виде словаря"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Проверяем существование таблицы
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
            if not cursor.fetchone():
                print("❌ Таблица items не найдена!")
                return {
                    "sectors": [],
                    "five_heaviest": [],
                    "total_weight": 0,
                    "dangerous_percent": 0,
                    "total_items": 0,
                    "dangerous_count": 0
                }
            
            # 1. Статистика по секторам
            sectors_data = cursor.execute(
                "SELECT storage_sector, COUNT(*) as total_items FROM items GROUP BY storage_sector"
            ).fetchall()
            sectors = format_db_row(sectors_data)
            
            # 2. 5 самых тяжелых предметов
            five_heaviest = cursor.execute(
                "SELECT name, weight FROM items ORDER BY weight DESC LIMIT 5"
            ).fetchall()
            five_heaviest_dicts = format_db_row(five_heaviest)
            
            # 3. Общий вес
            total_weight_result = cursor.execute(
                "SELECT COALESCE(SUM(weight*quantity), 0) as total_weight FROM items"
            ).fetchone()
            total_weight = total_weight_result['total_weight'] if total_weight_result else 0
            
            # 4. Процент опасных предметов
            total_items_result = cursor.execute("SELECT COUNT(*) FROM items").fetchone()
            total_items = total_items_result[0] if total_items_result else 0
            
            dangerous_count_result = cursor.execute(
                "SELECT COUNT(*) FROM items WHERE is_dangerous = 1"
            ).fetchone()
            dangerous_count = dangerous_count_result[0] if dangerous_count_result else 0
            
            dangerous_percent = (dangerous_count / total_items * 100) if total_items > 0 else 0
            
            return {
                "sectors": sectors,
                "five_heaviest": five_heaviest_dicts,
                "total_weight": float(total_weight),
                "dangerous_percent": round(dangerous_percent, 2),
                "total_items": total_items,
                "dangerous_count": dangerous_count
            }
    except Exception as e:
        print(f"❌ Ошибка в get_stats: {e}")
        import traceback
        traceback.print_exc()
        return {
            "sectors": [],
            "five_heaviest": [],
            "total_weight": 0,
            "dangerous_percent": 0,
            "total_items": 0,
            "dangerous_count": 0
        }
        
@app.get("/items/stats", tags=["Статистика"])
async def get_items_stats():
    stats = get_stats()
    return stats


@app.get("/stats-page", response_class=HTMLResponse, tags=["Страницы"])
async def stats_page():
    """Страница со статистикой"""
    with open("templates/stats.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/items", tags=["Товары"])
def get_all_items():
    with get_db_connection() as conn:
        items = conn.execute("SELECT * FROM items").fetchall()
        result = format_db_row(items)
        
        for item in result:
            likes_data = conn.execute("SELECT count FROM likes WHERE item_id = ?", (item['id'],)).fetchone()
            item['likes'] = likes_data['count'] if likes_data else 0
        
        return result

@app.get("/cart",tags=["Корзина"])
def get_my_cart(user_id:str):
    with get_db_connection() as conn:
        query = '''
        SELECT items.*, cart.quantity as cart_quantity FROM cart
        JOIN items ON cart.item_id = items.id WHERE cart.user_id = ?
    '''
    items = conn.execute(query,(user_id,)).fetchall()
    return format_db_row(items)


@app.get("/debug/db", tags=["Отладка"])
def debug_database():
    """Проверка подключения к БД"""
    import os
    db_path = 'warehouse.db'
    
    result = {
        "db_file_exists": os.path.exists(db_path),
        "db_absolute_path": os.path.abspath(db_path),
        "tables": [],
        "items_count": 0
    }
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            result["tables"] = [row[0] for row in cursor.fetchall()]
            
            if "items" in result["tables"]:
                cursor.execute("SELECT COUNT(*) FROM items")
                result["items_count"] = cursor.fetchone()[0]
    except Exception as e:
        result["error"] = str(e)
    
    return result

@app.get("/items/{item_id}", tags=["Просмотр"])
def get_one_item(item_id: int):
    with get_db_connection() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?",(item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404,detail="Товар не найден")
        return dict(item)
    
    

async def create_item(
    name: str = Form(...),
    storage_sector: int = Form(...),
    weight: float = Form(...),
    quantity: int = Form(...),
    is_dangerous: bool = Form(False),
    image_file: UploadFile = File(...)
):
    file_path = f"static/img/{image_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    with get_db_connection() as conn:
        cursor = conn.execute('''
            INSERT INTO items (name, storage_sector, weight, quantity, is_dangerous, image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, storage_sector, weight, quantity, int(is_dangerous), f"/{file_path}"))
        
        item_id = cursor.lastrowid
        
        
        conn.execute("INSERT INTO likes (item_id, count) VALUES (?, 0)", (item_id,))
        conn.commit()
    
    return {"message": "Успешно добавлено"}


@app.put("/items/{item_id}", tags=["Администрирование"])
def update_item(item_id: int, updated_item: ItemUpdate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE items
            SET name = ?, storage_sector = ?,weight = ?,quantity = ?,is_dangerous = ?, image = ?
            WHERE id = ?
            ''',(
                updated_item.name,
                updated_item.storage_sector,
                updated_item.weight,
                updated_item.quantity,
                int(updated_item.is_dangerous),
                item_id
            ))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Товар не найден")
    return {"message":"Данные обновлены"}
    
@app.post("/items/{item_id}/like", tags=["Лайки"])
def add_like(item_id: int):
    
    with get_db_connection() as conn:
        
        item = conn.execute("SELECT id FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        
        conn.execute('''
            INSERT INTO likes (item_id, count) 
            VALUES (?, 1)
            ON CONFLICT(item_id) DO UPDATE SET count = count + 1
        ''', (item_id,))
        
        conn.commit()
        
    
        result = conn.execute("SELECT count FROM likes WHERE item_id = ?", (item_id,)).fetchone()
        new_count = result['count'] if result else 0
    
    return {"item_id": item_id, "likes": new_count}

    
@app.delete("/items/{item_id}", tags=["Товары"])
def delete_item(item_id: int, confirm: bool = Query(False)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
    
        item = cursor.execute("SELECT is_dangerous FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        if item["is_dangerous"] == 1 and not confirm:
            raise HTTPException(
                status_code=400,
                detail="Удаление опасного груза требует подтверждения (confirm=true)!"
            )
        
        
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
    
    return {"message": "Успешно удалено"}



    

    

@app.post("/cart/add/{item_id}",tags=["Корзина"])
def add_to_cart(item_id:int,user_id:str):
    
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO cart (user_id,item_id,quantity) VALUES (?,?,1)
            ON CONFLICT(user_id, item_id) DO UPDATE SET quantity = quantity + 1
            ''', (user_id,item_id))
        conn.commit()
        
    return {
        "status":"success",
    }
    


@app.delete("/cart/clear",tags=["Корзина"])
def clear_cart(user_id: str):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()
    return {"message": " Корзина очищена"}






