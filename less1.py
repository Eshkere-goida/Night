# scores = [100,300,500,700]

# print(scores[0:5:1])
# print(scores[1::2])
# print(scores[::-1])


# limit = 10
# numbers = [4,18,9,22,6,30,14,2,40]
# def filter_and_trim(numbers:list[int],limit:int) -> list[int]:
#     result = []
#     for n in numbers:
#         if (n%2==0 and n>limit): result.append(n)
#     result.sort()
#     return result[0:3]
# print(filter_and_trim(numbers,limit))



# def  count_inventory(items:list[int]):
#     inventory = {}
#     for item in items:
#         if item in inventory: 
#             inventory[item] += 1
#         else: 
#             inventory[item] = 1
#     top_item = ""
#     max_count = 0
#     for name,count in inventory.items():
#         if count > max_count:
#             top_item = name
#             max_count = count
#     return inventory,top_item

# loot = ["зелье","стрела","зелье","монета","стрела","стрела"]

# stats,best = count_inventory(loot)

# print(stats)

# print("Больше всего:",best)



class Product:
    def __init__(self,name,price,quantity):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

    def get_total(self) -> float:
        return self.price * self.quantity

    def change_stock(self,amount):
        if self.quantity + amount < 0:
            print(f"Ошибка: на складе недостаточно {self.name}!")
            return False
        else:
            self.quantity += amount
            print(f"Остаток {self.name} обновлен: {self.quantity}")
            return True

    def show(self):
        print(f"{self.name} | Цена:{self.price} р.| Остаток: {self.quantity} шт.| Всего {self.get_total()} р.")



# item = Product("Клавиатура", 1500, 10)

# print(item.show())

# item.change_stock(-3)

# item.change_stock(-10)

# print("Итог:",item.quantity)

        

    
class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self,name,price,quantity):
        prod = Product(name,price,quantity)
        self.products.append(prod)
        print(f"[+] Товар '{name}' успешно добавлен на склад")

    def show_all(self):
        if not self.products:
            print("Склад пуст")
        else:
            for i,item in enumerate(self.products,1):
                print(f"{i}.{item.show()}")

    def update_product_stock(self,name,amount):
        target = name
        for prod in self.products:
            if prod.name.lower() == target.lower():
                prod.change_stock(amount)
                return True
            else:
                print(f"Ошибка: на складе недостаточно товара!")
                return False

    def get_total_warehouse_value(self):
        total = 0
        for prod in self.products:
            total += prod.get_total()
        return total

warehouse = Inventory()

warehouse.add_product("Мышь",1200,10)
warehouse.add_product("Клавиатура",3500,4)

warehouse.show_all()

warehouse.update_product_stock("мышь",-3)
warehouse.update_product_stock("клавиатура",2)
warehouse.update_product_stock("монитор",1)

print(f"Общая стоимость склада: {warehouse.get_total_warehouse_value()} р.")


while True:
    print("Выбери одно из предложенных ")