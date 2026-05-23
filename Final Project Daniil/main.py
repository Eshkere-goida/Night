Implement Like System for Warehouse App
Вот полная реализация системы лайков-кликера, основанная на вашем конспекте.

1. Обновлённый init_db.py (добавлена таблица likes)
python
import sqlite3

# 1. Подключаемся к файлу (если его нет, он создастся автоматически)
connection = sqlite3.connect('warehouse.db')

# 2. Создаем "курсор" --- это наш инструмент для выполнения команд
cursor = connection.cursor()

# 3. Пишем SQL-запрос для создания таблицы товаров
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

# 4. Создаём таблицу для корзины (многие ко многим)
cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    user_id TEXT,
    item_id INTEGER,
    quantity INTEGER DEFAULT 1,
    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
)
''')

# 5. ★ ЗВЕЗДОЧКА ★ Создаём таблицу для лайков-кликера
cursor.execute('''
CREATE TABLE IF NOT EXISTS likes (
    item_id INTEGER PRIMARY KEY,
    count INTEGER DEFAULT 0,
    FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

print("База данных успешно создана! (включая таблицу likes)")
2. Обновлённый main.py (добавлен эндпоинт /items/{item_id}/like)
python
import sqlite3
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Склад на SQLite")

# Настройка CORS и статики
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

# Модель данных для обновления
class ItemUpdate(BaseModel):
    name: str
    storage_sector: int
    weight: float
    quantity: int
    is_dangerous: bool
    image: str | None = None

# Функция подключения к БД
def get_db_connection():
    conn = sqlite3.connect('warehouse.db')
    conn.row_factory = sqlite3.Row
    return conn

# Вспомогательный форматировщик
def format_db_row(rows):
    return [dict(row) for row in rows]


# --- МЕТОДЫ ДЛЯ ТОВАРОВ (CRUD) ---

@app.get("/items", tags=["Товары"])
def get_all_items():
    with get_db_connection() as conn:
        items = conn.execute("SELECT * FROM items").fetchall()
        result = format_db_row(items)
        
        # ★ Добавляем количество лайков к каждому товару
        for item in result:
            likes_data = conn.execute("SELECT count FROM likes WHERE item_id = ?", (item['id'],)).fetchone()
            item['likes'] = likes_data['count'] if likes_data else 0
        
        return result

@app.get("/items/{item_id}", tags=["Товары"])
def get_one_item(item_id: int):
    with get_db_connection() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        result = dict(item)
        likes_data = conn.execute("SELECT count FROM likes WHERE item_id = ?", (item_id,)).fetchone()
        result['likes'] = likes_data['count'] if likes_data else 0
        
        return result

@app.post("/items", tags=["Товары"], status_code=201)
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
        
        # ★ Автоматически создаём запись о лайках для нового товара
        conn.execute("INSERT INTO likes (item_id, count) VALUES (?, 0)", (item_id,))
        conn.commit()
    
    return {"message": "Успешно добавлено"}

@app.put("/items/{item_id}", tags=["Товары"])
def update_item(item_id: int, updated_item: ItemUpdate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE items
            SET name = ?, storage_sector = ?, weight = ?, quantity = ?, is_dangerous = ?, image = ?
            WHERE id = ?
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

@app.delete("/items/{item_id}", tags=["Товары"])
def delete_item(item_id: int, confirm: bool = Query(False)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Проверяем статус опасности товара
        item = cursor.execute("SELECT is_dangerous FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        if item["is_dangerous"] == 1 and not confirm:
            raise HTTPException(
                status_code=400,
                detail="Удаление опасного груза требует подтверждения (confirm=true)!"
            )
        
        # ★ Запись в likes удалится автоматически благодаря ON DELETE CASCADE
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
    
    return {"message": "Успешно удалено"}


# ★★★ СИСТЕМА ЛАЙКОВ-КЛИКЕРА (ЗАДАНИЕ СО ЗВЕЗДОЧКОЙ) ★★★

@app.post("/items/{item_id}/like", tags=["Лайки"])
def add_like(item_id: int):
    """
    Эндпоинт для кликер-системы лайков.
    При каждом запросе увеличивает счётчик лайков для товара на 1.
    Использует UPSERT (INSERT ON CONFLICT) для автоматического создания записи.
    """
    with get_db_connection() as conn:
        # Проверяем, существует ли товар
        item = conn.execute("SELECT id FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        # ★ UPSERT: если запись есть — обновляем, если нет — создаём
        conn.execute('''
            INSERT INTO likes (item_id, count) 
            VALUES (?, 1)
            ON CONFLICT(item_id) DO UPDATE SET count = count + 1
        ''', (item_id,))
        
        conn.commit()
        
        # Получаем обновлённое количество лайков
        result = conn.execute("SELECT count FROM likes WHERE item_id = ?", (item_id,)).fetchone()
        new_count = result['count'] if result else 0
    
    return {"item_id": item_id, "likes": new_count}


# --- МЕТОДЫ ДЛЯ КОРЗИНЫ ---

@app.post("/cart/add/{item_id}", tags=["Корзина"])
def add_to_cart(item_id: int, user_id: str):
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO cart (user_id, item_id, quantity) VALUES (?, ?, 1)
            ON CONFLICT(user_id, item_id) DO UPDATE SET quantity = quantity + 1
        ''', (user_id, item_id))
        conn.commit()
    
    return {"status": "success"}

@app.get("/cart", tags=["Корзина"])
def get_cart(user_id: str):
    with get_db_connection() as conn:
        query = '''
            SELECT items.*, cart.quantity as cart_quantity
            FROM cart
            JOIN items ON cart.item_id = items.id
            WHERE cart.user_id = ?
        '''
        items = conn.execute(query, (user_id,)).fetchall()
        result = format_db_row(items)
        
        # Добавляем лайки к каждому товару в корзине
        for item in result:
            likes_data = conn.execute("SELECT count FROM likes WHERE item_id = ?", (item['id'],)).fetchone()
            item['likes'] = likes_data['count'] if likes_data else 0
        
        return result

@app.delete("/cart/clear", tags=["Корзина"])
def clear_cart(user_id: str):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()
    
    return {"message": "Корзина очищена"}
3. Фронтенд: добавляем лайки в HTML и JavaScript
Добавьте в карточку товара (HTML):
html
<div class="card" data-item-id="{{ item.id }}">
    <img src="{{ item.image }}" alt="{{ item.name }}">
    <h3>{{ item.name }}</h3>
    <p>Сектор: {{ item.storage_sector }}</p>
    <p>Вес: {{ item.weight }} кг</p>
    <p>Количество: {{ item.quantity }}</p>
    
    <!-- ★ Блок лайков-кликера ★ -->
    <div class="likes-section">
        <button class="like-button" onclick="handleLike({{ item.id }})">
            ❤️
        </button>
        <span class="likes-count" id="likes-{{ item.id }}">
            {{ item.likes | default(0) }}
        </span>
        <span class="likes-label">лайков</span>
    </div>
    
    <button onclick="addToCart({{ item.id }})">В корзину</button>
</div>
Добавьте CSS (стили для кнопки лайка):
css
.likes-section {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 10px 0;
    padding: 5px;
    background: #f5f5f5;
    border-radius: 20px;
}

.like-button {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    transition: transform 0.2s ease;
    padding: 0 5px;
}

.like-button:hover {
    transform: scale(1.2);
}

.like-button:active {
    transform: scale(0.95);
}

.likes-count {
    font-size: 18px;
    font-weight: bold;
    color: #e74c3c;
    min-width: 30px;
    text-align: center;
}

.likes-label {
    font-size: 14px;
    color: #666;
}
Добавьте JavaScript (script.js):
javascript
// ★ Функция для обработки лайков (кликер)
async function handleLike(itemId) {
    try {
        const response = await fetch(`/items/${itemId}/like`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка при отправке лайка');
        }
        
        const data = await response.json();
        
        // Мгновенно обновляем счётчик на странице
        const likesSpan = document.getElementById(`likes-${itemId}`);
        if (likesSpan) {
            // Небольшая анимация при клике
            likesSpan.style.transform = 'scale(1.3)';
            setTimeout(() => {
                likesSpan.style.transform = 'scale(1)';
            }, 200);
            
            likesSpan.textContent = data.likes;
        }
        
        console.log(`Товар ${itemId} получил лайк! Теперь: ${data.likes}`);
        
    } catch (error) {
        console.error('Ошибка при лайке:', error);
        alert('Не удалось поставить лайк. Попробуйте позже.');
    }
        }os.makedirs("static", exist_ok=True)
os.makedirs("static/img", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/items", tags=["Просмотр"])
def get_all_items():
    return items

@app.get("/items/{item_id}", tags=["Просмотр"])
def get_one_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", tags=["Администрирование"], status_code=201)
async def create_item(
    name: str = Form(...),
    storage_sector: int = Form(...),
    quantity: int = Form(...),
    weight: float = Form(0.0),
    price: int = Form(...),  # Добавляем обязательное поле price
    is_dangerous: bool = Form(False),
    image_file: UploadFile = File(...)
):
    try:
        # Проверяем что файл загружен
        if not image_file:
            raise HTTPException(status_code=400, detail="Файл изображения обязателен")
        
        # Создаем уникальное имя файла
        file_extension = os.path.splitext(image_file.filename)[1]
        unique_filename = f"{datetime.now().timestamp()}{file_extension}"
        file_path = f"static/img/{unique_filename}"
        
        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        
        # Генерируем новый ID
        new_id = items[-1]["id"] + 1 if items else 1
        
        # Создаем новый предмет
        new_item = {
            "id": new_id,
            "name": name,
            "storage_sector": storage_sector,
            "weight": weight,
            "quantity": quantity,
            "price": price,  # Используем цену из формы
            "is_dangerous": is_dangerous,
            "image_url": f"/{file_path}"
        }
        
        items.append(new_item)
        return new_item
        
    except Exception as e:
        print(f"Ошибка при создании предмета: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items/random", tags=["Просмотр"])
def get_random_item():
    if not items:
        raise HTTPException(status_code=404, detail="Нет товаров")
    return random.choice(items)

@app.get("/items/cheap", tags=["Просмотр"])
def get_cheap_items():
    return [item for item in items if item["price"] < 500]

@app.get("/items/count", tags=["Просмотр"])
def get_items_count():
    return {"total": len(items)}

@app.get("/items/search", tags=["Просмотр"])
def find_by_name(name: str):
    for item in items:
        if item["name"].lower() == name.lower():
            return item
    raise HTTPException(status_code=404, detail="Товар не найден")

@app.post("/items/apply-sale", tags=["Специальные предложения"])
def apply_sale(percent: int = 10):
    if percent < 1 or percent > 90:
        raise HTTPException(status_code=400, detail="Процент скидки должен быть от 1 до 90")
    
    for item in items:
        item["price"] = round(item["price"] * (1 - percent/100))
    
    return {"message": f"Скидка {percent}% применена"}

@app.delete("/items/clear-all", tags=["Администрирование"])
def clear_all():
    items.clear()
    return {"message": "Все товары удалены"}

@app.put("/items/{item_id}", tags=["Администрирование"])
def update_item(item_id: int, updated_item: Item):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items[i] = updated_item.model_dump()
            return {"message": "Обновлено"}
    raise HTTPException(status_code=404, detail="Товар не найден")

@app.delete("/items/{item_id}", tags=["Администрирование"])
def delete_item(item_id: int, confirm: bool = False):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            if item.get("is_dangerous") and not confirm:
                raise HTTPException(status_code=403, detail="Опасный товар! Подтвердите удаление")
            deleted = items.pop(i)
            return {"message": f"{deleted['name']} удален"}
    raise HTTPException(status_code=404, detail="Товар не найден")

@app.patch("/items/{item_id}/add_stock", tags=["Администрирование"])
def add_stock(item_id: int, amount: int):
    for item in items:
        if item["id"] == item_id:
            item["quantity"] += amount
            return {"message": f"Теперь на складе: {item['quantity']}"}
    raise HTTPException(status_code=404, detail="Товар не найден")
