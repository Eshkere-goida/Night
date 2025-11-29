from repositories.MySQLLogisticsRepository import MySQLLogisticsRepository
from services.LogisticsService import LogisticsService

class AppController:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin', 
            'database': 'test' 
        }
        self.repository = MySQLLogisticsRepository(**self.db_config)
    
    def run(self):
        while True:
            print("\n--- Добро пожаловать в Logistics Corp! ---")
            print("Мы доставим ваш груз куда угодно.")
            
            try:
                choice = input("Выберите способ отправки (road / sea / air): ").strip().lower()
                
                
                service = LogisticsService(self.repository)
                service.set_transport(choice)
                
               
                weight = float(input("Вес груза(кг): "))
                distance = float(input("Расстояние(км): "))
                express_choice = input("Как быстро доставить?(1 - Стандарт, 2 - Экспресс): ")
                is_express = (express_choice == "2")
                
                
                price = service.calculate_price(distance, weight, is_express)
                print(f"Расчетная стоимость: {price:.2f} руб.")
                
                
                ans = input("Оформить заказ? (y/n): ").strip().lower()
                if ans == 'n':
                    print("Операция отменена. До свидания.")
                    break
                elif ans == 'y':
                    comm = input("Оставьте комментарий к заказу: ")
                    service.confirm_order(distance, weight, price, is_express, comm)
                
                continue_choice = input("Хотите оформить еще один заказ? (y/n): ").strip().lower()
                if continue_choice == 'n':
                    print("До свидания!")
                    break
                    
            except ValueError as e:
                print(f"❌ Ошибка ввода данных: {e}")
            except Exception as e:
                print(f"❌ Произошла ошибка: {e}")
            
            input("\nНажмите Enter для продолжения...")