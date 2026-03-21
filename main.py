from pydantic import BaseModel,Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import items
import random

class Item(BaseModel):
    id: int = Field(...,gt=0)
    name: str = Field(...,min_length=1,max_length=50)
    weight: int = Field(...,gt=0)
    price: int = Field(...,gt=0)
    is_dangerous: bool = Field(default=False)
    
app = FastAPI(
    title="Digital Inventory System",
    description="Система управления складом будущего. Позволяет добавлять, искать и фильтровать объекты в реальнои времени.",
    version="1.0.0"
)

app.add_middleware (
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/items", tags = ["Просмотр"])
def get_all_items():
    return items

@app.get("/medicines/{medicine_id}",tags = ["Просмотр"])
def get_one_item(item_id : int):
    for item in items:
        if items["id"] == item_id:
            return item
        
    raise HTTPException(
        status_code=404,
        detail={
            "error":"ItemNotFound",
            "message":f"Предмет с ID{item_id} отсутствует в базе данных.",
            "suggestion" : "Попробуйте запросить список всех товаров, чтобы увидеть доступные ID"
        }
    )


@app.post("/items",tags = ["Администрирование"], status_code=201)
def create_item(item: Item):
    if item.weight > 2000:
        raise HTTPException(
            status_code=404,
            detail="Склад не рассчитан на такой вес. Максимум: 2000 кг."
        )
    for existing_med in items:
        if existing_med["name"].lower() == item.name.lower():
            raise HTTPException(
                status_code = 400,
                detail = f"Ошибка: Объект с названием '{item.name}' уже существует!"
            )
            
    new_medicine_dict = item.model_dump()
    
    if len(items) > 0:
        new_id = items[-1]["id"] + 1
    else:
        new_id = 1
        
    new_medicine_dict["id"] = new_id
    
    items.append(new_medicine_dict)
    
    return {"status" : "success", "new_id" : new_id , "added_medicine" : new_medicine_dict}


@app.post("/medicines/apply-sale", tags=["Специальные предложения"])
def apply_sale(percent: int = 10):
    if percent < 1 or percent > 90:
        raise HTTPException(
            status_code=400,
            detail="Процент скидки должен быть в диапазоне от 1 до 90"
        )
    for med in items:
        new_price = round(med["price"] * (1- percent/100))
        
        med["price"] = new_price
        
    return {
        "status" : "success",
        "message" : f"Скидка {percent}% применена ко всем товарам!",
        "new_prices" : [i["price"] for i in items]
    }
    

@app.get("/items/random", tags=["Просмотр"])
def get_random_medicine():
    random_id = random.randint(0,len(items)-1)
    return items[random_id]

@app.get("/items/cheap", tags=["Просмотр"])
def get_cheap_medicine():
    cheap_list = []
    for dict in items:
        if dict["price"] < 500:
            cheap_list.append(dict)
    return cheap_list

@app.get("/items/count", tags=["Просмотр"])
def get_items_count():
    total_count = len(items)
    return {
        "total":total_count,
        "message" : f"На данный момент в базе данных {total_count} ззаписей"
    }
@app.get("/items/search", tags=["Просмотр"])
def find_by_name(name:str):
    for dict in items:
        if dict["name"] == name:
            return dict
    raise HTTPException(
        status_code=404,
        detail=f"Предмета с названием {name} нету на складе."
    )

@app.get("/items/clear-all" , tags=["Администрирование"])
def clear_all():
    items.clear()
    
    
@app.put("/medicines/{medicine_id}",tags=["Администрирование"])
def update_medicine(medicine_id: int, updated_medicine: Item):
    for i,medicine in enumerate(items):
        if medicine["id"] == medicine_id:
            new_data = updated_medicine.model_dump()
            new_data["id"] = medicine_id
            items[i] = new_data
            return {"message" : "Данные обновлены","medicine":new_data}
        
    raise HTTPException(
        status_code=404,
        detail="Невозможно обновить: предмет не найден."
    )
    
@app.delete("items/{item_id}", tags=['Администрирование'])
def delete_item(item_id:int, confirm:bool = False):
    for i,item in enumerate(items):
        if item["id"] == item_id:
            if item.get("is_dangerous") == True and confirm == False:
                raise HTTPException(
                    status_code = 403,
                    detail = "Внимание: товар опасен! Подтвердите удаление (confirm = True)"
                    
                )
            deleted_item = item.pop(i)
            return {
                "status" : "success",
                "message" : f"Объект '{deleted_item['name']}' утилизирован."
            }
    raise HTTPException(
        status_code = 404,
        detail = "Объект не найден."
    )
            
@app.patch("/items/{item_id}/add_stock", tags=["Администрирование"])
def add_stock(item_id:int,amount:int):
    for item in items:
        if item["id"] == item_id:
            item["quantity"] += amount
            return {
                "message":f"Запас обновлен. Теперь на складе: {item['quantity']}"
            }
        raise HTTPException(
            status_code=404,
            detail="Товар не найден."
        )
        
    

