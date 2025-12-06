from repositories.MySQLLogisticsRepository import MySQLLogisticsRepository
from services.LogisticsService import LogisticsService
from domain.Plane import Plane
from domain.Truck import Truck
from domain.Ship import Ship
from domain.listeners.DriverDBListener import DriverDBListener
from domain.listeners.ManagerDBListener import ManagerDBListener
from domain.listeners.LogListener import LogListener


class AppController:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin',
            'database': 'test'
        }
        self.repository = MySQLLogisticsRepository(**self.db_config)
        
        self.driver_listener = DriverDBListener(self.repository)
        self.manager_listener = ManagerDBListener(self.repository)
        self.log_listener = LogListener()


    def run(self):
        while True:
            print("Добро пожаловать в Logistics Corp!")
            print("Мы доставим ваш груз куда угодно.")
   
            
            print("\nВведите данные для доставки:")
            from_city = input("Откуда (город, страна): ")
            to_city = input("Куда (город, страна): ")
            
            print("\nВыберите способ доставки:")
            print("1. Грузовик (road)")
            print("2. Корабль (sea)")
            print("3. Самолет (air)")
            
            choice = input("Ваш выбор (1/2/3 или road/sea/air): ").lower()
            
            if choice == '1' or choice == 'road':
                processor = Truck()
                transport_type = "road"
            elif choice == '2' or choice == 'sea':
                processor = Ship()
                transport_type = "sea"
            elif choice == '3' or choice == 'air':
                processor = Plane()
                transport_type = "air"
            else:
                print("Неверный выбор! Попробуйте снова.")
                continue
            
            try:
                weight = float(input("Вес груза (кг): "))
                distance = float(input("Расстояние (км): "))
                express_choice = input("Тип доставки (1 - Стандарт, 2 - Экспресс): ")
                if express_choice == '2':
                    is_express = True  
                else:
                    is_express = False
            except ValueError:
                print("Ошибка ввода числовых значений!")
                continue
            
            service = LogisticsService(self.repository, processor)
            
            service.events.subscribe(self.driver_listener)
            service.events.subscribe(self.manager_listener)
            service.events.subscribe(self.log_listener)
            
            price = service.calculate_price(distance, weight, is_express)
            
            print(f"РАСЧЕТ СТОИМОСТИ")
            print(f"Маршрут: {from_city} -> {to_city}")
            print(f"Расстояние: {distance} км")
            print(f"Вес: {weight} кг")
            print(f"Тип доставки: {'Экспресс' if is_express else 'Стандарт'}")
            print(f"Итоговая стоимость: {price:.2f} руб.")
            
            ans = input("\nОформить заказ? (y/n): ").lower()
            if ans == 'n':
                print("Операция отменена.")
                continue
            
            
            comment = input("Оставьте комментарий к заказу: ")
            service.confirm_order(transport_type,from_city,to_city,distance,weight,price,is_express,comment)
            
            another = input("\nОформить еще один заказ? (y/n): ").lower()
            if another != 'y':
                print("Спасибо за использование Logistics Corp! До свидания.")
                break