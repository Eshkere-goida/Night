from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3
from typing import Dict, Any


app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect('warehouse.db')
    conn.row_factory = sqlite3.Row
    return conn

def format_db_row(rows):
    return [dict(row) for row in rows]

def get_stats() -> Dict[str, Any]:
    """Возвращает статистику в виде словаря"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Статистика по секторам
        sectors_data = cursor.execute("SELECT storage_sector, COUNT(*) as total_items FROM items GROUP BY storage_sector").fetchall()
        sectors = format_db_row(sectors_data)
        
        # 2. 5 самых тяжелых предметов
        five_heaviest = cursor.execute(
            "SELECT name, weight FROM items ORDER BY weight DESC LIMIT 5"
        ).fetchall()
        five_heaviest_dicts = format_db_row(five_heaviest)
        
        # 3. Общий вес
        total_weight = cursor.execute(
            "SELECT COALESCE(SUM(weight*quantity), 0) as total_weight FROM items"
        ).fetchone()['total_weight']
        
        # 4. Процент опасных предметов
        total_items = cursor.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        dangerous_count = cursor.execute(
            "SELECT COUNT(*) FROM items WHERE is_dangerous = 1"
        ).fetchone()[0]
        dangerous_percent = (dangerous_count / total_items * 100) if total_items > 0 else 0
        
        return {
            "sectors": sectors,
            "five_heaviest": five_heaviest_dicts,
            "total_weight": float(total_weight), 
            "dangerous_percent": round(dangerous_percent, 2),
            "total_items": total_items,
            "dangerous_count": dangerous_count
        }


@app.get("/items/stats")
async def items_stats():
    
    stats = get_stats()
    return stats


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()