from services.PizzaBuilder import PizzaBuilder
from services.MenuDirector import MenuDirector

class TerminalController:
    def __init__(self):
        self.builder = PizzaBuilder()
        self.director = MenuDirector()
    
    def run(self):
        
        while True:
            print("\nМЕНЮ:")
            print("1. Пепперони (готовый вариант)")
            print("2. Собрать свою пиццу")
            print("3. Маргарита (готовый вариант)")
            print("4. Выход")
            
            choice = input("\nВыберите опцию (1-4): ").strip()
            
            if choice == "1":
                self.order_pepperoni()
            elif choice == "2":
                self.custom_pizza()
            elif choice == "3":
                self.order_margherita()
            elif choice == "4":
                print("\nСпасибо за заказ! До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def order_pepperoni(self):
        print("\nЗаказ пиццы 'Пепперони'...")
        pizza = self.director.make_pepperoni(self.builder)
        pizza.name = "Пепперони"
        self.show_pizza(pizza)
    
    def order_margherita(self):
        print("\nЗаказ пиццы 'Маргарита'...")
        pizza = self.director.make_margherita(self.builder)
        pizza.name = "Маргарита"
        self.show_pizza(pizza)
    
    def custom_pizza(self):
        print("\nСобираем кастомную пиццу...")
        
        
        self.builder.reset()
        
        print("\nВыберите тесто:")
        print("1. Тонкое")
        print("2. Толстое")
        dough_choice = input("Ваш выбор (1-2): ").strip()
        
        if dough_choice == "1":
            self.builder.set_thin_dough()
        elif dough_choice == "2":
            self.builder.set_thick_dough()
        else:
            print("Будет использовано тонкое тесто по умолчанию")
            self.builder.set_thin_dough()
        
        sauce_choice = input("\nДобавить томатный соус? (да/нет): ").strip().lower()
        if sauce_choice == "да":
            self.builder.add_sauce()
        
        toppings = {
            "сыр": self.builder.add_cheese,
            "бекон": self.builder.add_bacon,
            "грибы": self.builder.add_mushrooms,
            "пепперони": self.builder.add_pepperoni,
            "оливки": self.builder.add_olives
        }
        
        print("\nДоступные добавки: сыр, бекон, грибы, пепперони, оливки")
        print("Вводите добавки по одной, для завершения введите 'готово'")
        
        while True:
            topping = input("Добавка: ").strip().lower()
            if topping == "готово":
                break
            elif topping in toppings:
                toppings[topping]()
            else:
                print(f"Добавка '{topping}' недоступна")
        

        name = input("\nНазвание вашей пиццы: ").strip()
        if not name:
            name = "Моя кастомная пицца"
        
        pizza = self.builder.build()
        pizza.name = name
        self.show_pizza(pizza)
    
    def show_pizza(self, pizza):
        print("ВАШ ЗАКАЗ:")
        print(pizza)
        input("\nНажмите Enter для продолжения...")