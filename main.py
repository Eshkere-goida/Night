from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price:str
    status: str

app = FastAPI()

app.add_middleware (
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

inventory = [
    {"id":1,"name":"Скафандр Марс-1","price":450,"status":"В наличии"},
    {"id":2,"name":"Кислородный баллон","price":80,"status":"Мало"},
    {"id":3,"name":"Набор инструментов","price":120,"status":"В наличии"}
]

@app.get("/items")
def get_all_items(max_price: int=None):
    if max_price is None:
        return inventory
    filtered_items = []
    for item in inventory:
        if item["price"] <= max_price:
            filtered_items.append(item)
    return filtered_items


@app.post("/items")
def add_item (item:Item):
    new_item_dict = item.dict()
    new_item_dict["id"] = len(inventory)+1

    inventory.append(new_item_dict)
    return {"message":"Товар успешно добавлен","item":new_item_dict}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global inventory
    inventory = [item for item in inventory if item["id"] != item_id]
    return {"status":"success","message" : f"Товар {item_id} удален"}
