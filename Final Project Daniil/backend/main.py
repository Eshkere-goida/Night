from pydantic import BaseModel,Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import medicines
import random

class Medicine(BaseModel):
    id: int = Field(...,gt=0)
    name: str = Field(...,min_length=1,max_length=50)
    medicine_element: str = Field(...,min_length=1,max_length=100)
    price: int = Field(...,gt=0)
    is_prescripted: str = Field(default="Нет")
    
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

@app.get("/medicines", tags = ["Просмотр"])
def get_all_medicines():
    return medicines

@app.get("/medicines/{medicine_id}",tags = ["Просмотр"])
def get_one_medicine(medicine_id : int):
    for med in medicines:
        if med["id"] == medicine_id:
            return med
        
    raise HTTPException(
        status_code=404,
        detail={
            "error":"ItemNotFound",
            "message":f"Предмет с ID{medicine_id} отсутствует в базе данных.",
            "suggestion" : "Попробуйте запросить список всех товаров, чтобы увидеть доступные ID"
        }
    )


@app.post("/medicines",tags = ["Администрирование"], status_code=201)
def create_medicine(medicine: Medicine):
    for existing_med in medicines:
        if existing_med["name"].lower() == medicine.name.lower():
            raise HTTPException(
                status_code = 400,
                detail = f"Ошибка: Объект с названием '{medicine.name}' уже существует!"
            )
            
    new_medicine_dict = medicine.dict()
    
    if len(medicines) > 0:
        new_id = medicines[-1]["id"] + 1
    else:
        new_id = 1
        
    new_medicine_dict["id"] = new_id
    
    medicines.append(new_medicine_dict)
    
    return {"status" : "success", "new_id" : new_id , "added_medicine" : new_medicine_dict}


@app.post("/medicines/apply-sale", tags=["Специальные предложения"])
def apply_sale(percent: int = 10):
    if percent < 1 or percent > 90:
        raise HTTPException(
            status_code=400,
            detail="Процент скидки должен быть в диапазоне от 1 до 90"
        )
    for med in medicines:
        new_price = round(med["price"] * (1- percent/100))
        
        med["price"] = new_price
        
    return {
        "status" : "success",
        "message" : f"Скидка {percent}% применена ко всем товарам!",
        "new_prices" : [i["price"] for i in medicines]
    }
    

@app.get("/items/random", tags=["Просмотр"])
def get_random_medicine():
    random_id = random.randint(0,len(medicines)-1)
    return medicines[random_id]

@app.get("/items/cheap", tags=["Просмотр"])
def get_cheap_medicine():
    cheap_list = []
    for dict in medicines:
        if dict["price"] < 500:
            cheap_list.append(dict)
    return cheap_list

@app.get("/items/count", tags=["Просмотр"])
def get_med_quantity():
    quantity = len(medicines)
    return f"На складе {quantity} товаров."

@app.get("/items/search", tags=["Просмотр"])
def find_by_name(name:str):
    for dict in medicines:
        if dict["name"] == name:
            return dict
    raise HTTPException(
        status_code=404,
        detail=f"Препарата с названием {name} нету на складе."
    )

@app.get("/items/clear-all" , tags=["Администрирование"])
def clear_all():
    medicines.clear()



