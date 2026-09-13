class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

    def get_total(self) -> float:
        return self.price * self.quantity

    def change_stock(self, amount) -> bool:
        if self.quantity + amount < 0:
            print(f"Ошибка: на складе недостаточно товара {self.name}!")
            return False
        else:
            self.quantity += amount
            print(f"Остаток {self.name} обновлен: {self.quantity} шт.")
            return True

    def show(self):
        print(f"{self.name} | Цена: {self.price} р. | Остаток: {self.quantity} шт. | Всего: {self.get_total()} р.")


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, name, price, quantity):
        # Проверяем, нет ли уже товара с таким именем
        for prod in self.products:
            if prod.name.lower() == name.lower():
                prod.price = float(price)
                prod.quantity += int(quantity)
                print(f"[+] Товар '{prod.name}' уже существует. Остаток увеличен на {quantity} шт. Цена обновлена.")
                return
        
        prod = Product(name, price, quantity)
        self.products.append(prod)
        print(f"[+] Товар '{name}' успешно добавлен на склад.")

    def show_all(self):
        if not self.products:
            print("\n[!] Склад пуст.")
        else:
            print("\n--- Список товаров на складе ---")
            for i, item in enumerate(self.products, 1):
                print(f"{i}. ", end="")
                item.show()

    def update_product_stock(self, name, amount) -> bool:
        for prod in self.products:
            if prod.name.lower() == name.lower():
                return prod.change_stock(amount)
        
        print(f"Ошибка: товар '{name}' не найден на складе!")
        return False

    def get_total_warehouse_value(self) -> float:
        total = 0
        for prod in self.products:
            total += prod.get_total()
        return total


# ==========================================
# Инициализация и цикл интерактивного меню
# ==========================================

# 1. Инициируем менеджер склада
warehouse = Inventory()

# 2. Добавляем 2 стартовые позиции для автоматизации тестов
warehouse.add_product("Мышь", 1200, 10)
warehouse.add_product("Клавиатура", 3500, 4)

# 3. Активируем цикл событий
while True:
    # 4. Визуальный перечень команд
    print("\n" + "="*40)
    print(" СИСТЕМА «СКЛАД АДМИНИСТРАТОРА»")
    print("="*40)
    print("1. Показать все товары")
    print("2. Добавить новый товар")
    print("3. Изменить остаток товара")
    print("4. Аудит (Общая стоимость склада)")
    print("5. Выход")
    print("="*40)

    # 5. Организуем прием выбора пользователя с нормализацией
    choice = input("Выберите пункт меню (1-5): ").strip()

    # 6. Логика ветвления
    if choice == "1":
        # Просмотр
        warehouse.show_all()

    elif choice == "2":
        # Создание нового товара с валидацией числовых полей в try / except
        print("\n--- Добавление нового товара ---")
        name = input("Введите название товара: ").strip()
        if not name:
            print("Ошибка: название товара не может быть пустым.")
            continue

        try:
            price = float(input("Введите цену товара (р.): ").strip())
            quantity = int(input("Введите стартовое количество (шт.): ").strip())
            
            if price < 0 or quantity < 0:
                print("Ошибка: цена и количество не могут быть отрицательными.")
                continue
                
            warehouse.add_product(name, price, quantity)
        except ValueError:
            print("Ошибка: цена должна быть числом, а количество — целым числом!")

    elif choice == "3":
        # Обновление остатка по имени с защитой от ввода букв
        print("\n--- Изменение остатка товара ---")
        name = input("Введите точное название товара: ").strip()
        
        try:
            amount = int(input("Введите изменение остатка (например, -3 для списания или 5 для прихода): ").strip())
            warehouse.update_product_stock(name, amount)
        except ValueError:
            print("Ошибка: количество для изменения должно быть целым числом!")

    elif choice == "4":
        # Аналитика
        total_value = warehouse.get_total_warehouse_value()
        print(f"\n[Аналитика] Общая стоимость всех товаров на складе: {total_value:.2f} р.")

    elif choice == "5":
        # Прощание и разрыв цикла
        print("\nРабота завершена. Всего доброго!")
        break

    else:
        # Обработка невалидных пунктов меню
        print("\n[!] Некорректный выбор. Пожалуйста, введите цифру от 1 до 5.")
