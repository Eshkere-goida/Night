import sqlite3
import shutil
import csv
import os
from io import StringIO

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

# Раздача статических файлов (картинки, HTML-страницы)
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


class ItemUpdate(BaseModel):
    name: str
    storage_sector: int
    weight: float
    quantity: int
    is_dangerous: bool
    image: str | None = None


def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'warehouse.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def format_db_row(rows):
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────
# СТАТИСТИКА (ETL — Компонент 1)
# ─────────────────────────────────────────────

def get_stats() -> Dict[str, Any]:
    """Считает агрегаты прямо в SQLite, без загрузки в память Python."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
            if not cursor.fetchone():
                return {
                    "sectors": [], "five_heaviest": [],
                    "total_weight": 0, "dangerous_percent": 0,
                    "total_items": 0, "dangerous_count": 0
                }

            # Распределение по секторам
            sectors_data = cursor.execute(
                "SELECT storage_sector, COUNT(*) as total_items FROM items GROUP BY storage_sector"
            ).fetchall()

            # Топ-5 самых тяжёлых
            five_heaviest = cursor.execute(
                "SELECT name, weight FROM items ORDER BY weight DESC LIMIT 5"
            ).fetchall()

            # Абсолютный тоннаж
            total_weight_row = cursor.execute(
                "SELECT COALESCE(SUM(weight * quantity), 0) as total_weight FROM items"
            ).fetchone()
            total_weight = total_weight_row['total_weight'] if total_weight_row else 0

            # Процент опасных
            total_items = cursor.execute("SELECT COUNT(*) FROM items").fetchone()[0]
            dangerous_count = cursor.execute(
                "SELECT COUNT(*) FROM items WHERE is_dangerous = 1"
            ).fetchone()[0]
            dangerous_percent = round((dangerous_count / total_items * 100), 2) if total_items > 0 else 0

            return {
                "sectors": format_db_row(sectors_data),
                "five_heaviest": format_db_row(five_heaviest),
                "total_weight": float(total_weight),
                "dangerous_percent": dangerous_percent,
                "total_items": total_items,
                "dangerous_count": dangerous_count
            }
    except Exception as e:
        print(f"Ошибка в get_stats: {e}")
        return {
            "sectors": [], "five_heaviest": [],
            "total_weight": 0, "dangerous_percent": 0,
            "total_items": 0, "dangerous_count": 0
        }


@app.get("/items/stats", tags=["Статистика"])
async def get_items_stats():
    return get_stats()


@app.get("/items/count", tags=["Статистика"])
def get_items_count():
    """Быстрый счётчик для шапки сайта."""
    with get_db_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    return {"total": total}



# ─────────────────────────────────────────────
# ETL — Компонент 2: CSV-экспорт
# ─────────────────────────────────────────────

@app.get("/items/export/csv", tags=["ETL / Экспорт"])
def export_items_csv():
    """
    Экспортирует все товары в CSV-файл.
    Браузер автоматически скачает файл warehouse_export.csv.
    """
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM items").fetchall()

    # Сериализация в буфер в памяти (без записи на диск)
    output = StringIO()
    writer = csv.writer(output, delimiter=';')

    # Заголовки колонок
    writer.writerow(['ID', 'Название', 'Сектор', 'Вес', 'Количество', 'Опасен', 'Изображение'])

    for row in rows:
        writer.writerow([
            row['id'],
            row['name'],
            row['storage_sector'],
            row['weight'],
            row['quantity'],
            'Да' if row['is_dangerous'] else 'Нет',
            row['image'] or ''
        ])

    csv_content = output.getvalue()

    return Response(
        content=csv_content.encode('utf-8-sig'),  # utf-8-sig = BOM для Excel
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=warehouse_export.csv"
        }
    )


# ─────────────────────────────────────────────
# ТОВАРЫ
# ─────────────────────────────────────────────

@app.get("/items", tags=["Товары"])
def get_all_items():
    with get_db_connection() as conn:
        items = conn.execute("SELECT * FROM items").fetchall()
        result = format_db_row(items)
        for item in result:
            likes_data = conn.execute(
                "SELECT count FROM likes WHERE item_id = ?", (item['id'],)
            ).fetchone()
            item['likes'] = likes_data['count'] if likes_data else 0
    return result


@app.get("/items/search", tags=["Товары"])
def search_items(name: str):
    """Поиск по названию (без учёта регистра)."""
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM items WHERE LOWER(name) LIKE LOWER(?)",
            (f"%{name}%",)
        ).fetchall()
    return format_db_row(rows)


@app.get("/items/{item_id}", tags=["Просмотр"])
def get_one_item(item_id: int):
    with get_db_connection() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Товар не найден")
        result = dict(item)
        likes_data = conn.execute(
            "SELECT count FROM likes WHERE item_id = ?", (item_id,)
        ).fetchone()
        result['likes'] = likes_data['count'] if likes_data else 0
    return result


@app.post("/items", status_code=201, tags=["Товары"])
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
            UPDATE items SET name=?, storage_sector=?, weight=?, quantity=?, is_dangerous=?, image=?
            WHERE id=?
        ''', (
            updated_item.name,
            updated_item.storage_sector,
            updated_item.weight,
            updated_item.quantity,
            int(updated_item.is_dangerous),
            updated_item.image,
            item_id
        ))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Товар не найден")
    return {"message": "Данные обновлены"}


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
        item = cursor.execute(
            "SELECT is_dangerous FROM items WHERE id = ?", (item_id,)
        ).fetchone()
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


# ─────────────────────────────────────────────
# КОРЗИНА
# ─────────────────────────────────────────────

@app.get("/cart", tags=["Корзина"])
def get_my_cart(user_id: str):
    with get_db_connection() as conn:
        query = '''
            SELECT items.*, cart.quantity as cart_quantity
            FROM cart
            JOIN items ON cart.item_id = items.id
            WHERE cart.user_id = ?
        '''
        items = conn.execute(query, (user_id,)).fetchall()
    return format_db_row(items)


@app.post("/cart/add/{item_id}", tags=["Корзина"])
def add_to_cart(item_id: int, user_id: str):
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO cart (user_id, item_id, quantity) VALUES (?, ?, 1)
            ON CONFLICT(user_id, item_id) DO UPDATE SET quantity = quantity + 1
        ''', (user_id, item_id))
        conn.commit()
    return {"status": "success"}


@app.delete("/cart/clear", tags=["Корзина"])
def clear_cart(user_id: str):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()
    return {"message": "Корзина очищена"}
