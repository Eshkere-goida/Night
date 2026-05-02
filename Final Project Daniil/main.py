from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import items
import random
import shutil
import os
from datetime import datetime

class Item(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=50)
    storage_sector: int = Field(..., ge=1, le=99)
    weight: float = Field(..., gt=0)
    quantity: int = Field(default=1, gt=0)
    price: int = Field(..., gt=0)
    is_dangerous: bool = Field(default=False)
    image_url: str = Field(default="")

app = FastAPI(
    title="Digital Inventory System",
    description="Система управления складом будущего.",
    version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем папки
os.makedirs("static", exist_ok=True)
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