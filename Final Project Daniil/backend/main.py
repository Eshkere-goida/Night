import sqlite3
import shutil
from fastapi import FastAPI, HTTPException, UploadFile,File,Form,Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


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
    conn = sqlite3.connect('warehouse.db')
    conn.row_factory = sqlite3.Row
    return conn

def format_db_row(rows):
    return [dict(row) for row in rows]



@app.get("/items", tags=["Просмотр"])
def get_all_items():
    with get_db_connection() as conn:
        items = conn.execute("SELECT * FROM items").fetchall()
        return format_db_row(items)
    

@app.get("/items/{item_id}", tags=["Просмотр"])
def get_one_item(item_id: int):
    with get_db_connection() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?",(item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404,detail="Товар не найден")
        return dict(item)

@app.post("/items", tags=["Администрирование"], status_code=201)
async def create_item(
    name: str = Form(...),
    storage_sector: int = Form(...),
    weight: float = Form(0.0),
    quantity: int = Form(...),
    is_dangerous: bool = Form(False),
    image_file: UploadFile = File(...)
):
    file_path = f"static/img/{image_file.filename}"
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(image_file.file,buffer)
    with get_db_connection() as conn:
        conn.execute('''
        INSERT INTO items (name,storage_sector,weight,quantity,is_dangerous,image)
        VALUES (?,?,?,?,?,?)
                     ''',(name,storage_sector,weight,quantity,int(is_dangerous),f"/{file_path}"))        
        conn.commit()
    return {"message":"Успешно добавлено!"}

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
    
    
@app.delete("/items/{item_id}", tags=["Администрирование"])
def delete_item(item_id: int, confirm: bool = Query(False)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        item = cursor.execute("SELECT is_dangerous FROM items WHERE id=?",(item_id,)).fetchone()
        
        if not item:
            raise HTTPException(status_code=404, detail="Товар не найден")

        if item['is_dangerous'] == 1 and not confirm:
            raise HTTPException (
                status_code=400,
                detail="Удаление опасного груза требует подтверждения(confirm=true)!"
            )
        cursor.execute("DELETE FROM items WHERE id = ?",(item_id,))
        conn.commit()
    return {"message" : "Успешно удалено"}

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
    

@app.get("/cart",tags=["Корзина"])
def get_my_cart(user_id:str):
    with get_db_connection() as conn:
        query = '''
        SELECT items.*, cart.quantity as cart_quantity FROM cart
        JOIN items ON cart.item_id = items.id WHERE cart.user_id = ?
    '''
    items = conn.execute(query,(user_id,)).fetchall()
    return format_db_row(items)

@app.delete("/cart/clear",tags=["Корзина"])
def clear_cart(user_id: str):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()
    return {"message": " Корзина очищена"}






