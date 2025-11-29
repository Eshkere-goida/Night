from repositories.MySQLLogisticsRepository import MySQLLogisticsRepository
from services.LogisticsService import LogisticsService
from domain.Plane import Plane
from domain.Truck import Truck
from domain.Ship import Ship

class AppController:
    def __init__(self):
       
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin', 
            'database': 'test' 
        }
        self.repository = MySQLLogisticsRepository(**self.db_config)
    
    def get_all_data(self,weight,distance,is_express):
        weight = float(input("Вес груза(кг): "))
        distance = float(input("Расстояние(км): "))
        is_express = float(input("Как быстро доставить?(1 - Стандарт, 2 - Экспресс): "))
    
    def run(self,weight,distance,is_express):
        while True:
            print("\n--- Добро пожаловать в Logistics Corp! ---\nМы доставим ваш груз куда угодно.")
            choice = input("Выберите способ отправки (road / sea / air): ")
            if choice == 'road':
                processor = Truck()
            elif choice == '2':
                processor = Ship()
            elif choice == '3':
                processor = Plane()
            else:
                print("Неверный выбор! Попробуйте снова.")
                continue
            weight = float(input("Вес груза(кг): "))
            distance = float(input("Расстояние(км): "))
            is_express = float(input("Как быстро доставить?(1 - Стандарт, 2 - Экспресс): "))

            service = LogisticsService(self.repository, processor)
            price = service.calculate_price(distance,weight,is_express)
            print(f"Расчетная стоимость: {price} руб.")
            ans = input("Оформить заказ? (y/n)")
            if ans == 'n':
                print("Операция отменена. До свидания.")
            if ans == 'y':
                comm = input("Оставьте комментарий к заказу: ")
                service.confirm_order(distance,weight,price,is_express,comm)
            
            input("\nНажмите Enter для продолжения...")