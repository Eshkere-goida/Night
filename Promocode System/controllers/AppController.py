from repositories.MySQLLogisticsRepository import MySQLLogisticsRepository
from repositories.MySQLPromoCodeRepository import MySQLPromoCodeRepository
from services.LogisticsService import LogisticsService
from domain.Plane import Plane
from domain.Truck import Truck
from domain.Ship import Ship
from domain.ChinaAdapter import ChinaAdapter
from domain.listeners.DriverDBListener import DriverDBListener
from domain.listeners.ManageDBListener import ManagerDBListener
from domain.listeners.LogListener import LogListener
from datetime import datetime, timedelta


class AppController:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin',
            'database': 'test'
        }
        self.repository = MySQLLogisticsRepository(**self.db_config)
        self.promo_repository = MySQLPromoCodeRepository(**self.db_config)
        
        
        self._initialize_promo_codes()
        
        self.driver_listener = DriverDBListener(self.repository)
        self.manager_listener = ManagerDBListener(self.repository)
        self.log_listener = LogListener()

    def _initialize_promo_codes(self):
        """Инициализация тестовых промокодов"""
        from domain.PromoCode import PercentagePromoCode, FixedAmountPromoCode
        
        
        test_promos = [
            PercentagePromoCode("WELCOME10", 10, datetime.now() + timedelta(days=30)),
            PercentagePromoCode("SUMMER20", 20, datetime.now() + timedelta(days=15)),
            FixedAmountPromoCode("FREESHIP", 500, datetime.now() + timedelta(days=60), min_order_amount=2000),
            FixedAmountPromoCode("FIRSTORDER", 300, datetime.now() + timedelta(days=90))
        ]
        
        for promo in test_promos:
    
            existing = self.promo_repository.get_promo_code(promo.get_code())
            if not existing:
                self.promo_repository.add_promo_code(promo)

    def run(self):
        while True:
            print("=" * 50)
            print("Добро пожаловать в Logistics Corp!")
            print("Мы доставим ваш груз куда угодно.")
            
    
            print("\nАктивные промокоды:")
            active_promos = self.promo_repository.get_all_active_promo_codes()
            if active_promos:
                for promo in active_promos:
                    code, discount_type, value = promo
                    desc = f"{value}%" if discount_type == 'percentage' else f"{value} руб."
                    print(f"  - {code}: Скидка {desc}")
            else:
                print("  Нет активных промокодов")
            print("=" * 50)
            
            print("\nВведите данные для доставки:")
            from_city = input("Откуда (город, страна): ")
            to_city = input("Куда (город, страна): ")
            
            print("\nВыберите способ доставки:")
            print("1. Грузовик (road)")
            print("2. Корабль (sea)")
            print("3. Самолет (air)")
            print("4. Доставка ChinaDragonLogistics (china)")
            
            choice = input("Ваш выбор (1/2/3/4 или road/sea/air/china): ").lower()
            
            if choice == '1' or choice == 'road':
                processor = Truck()
                transport_type = "road"
            elif choice == '2' or choice == 'sea':
                processor = Ship()
                transport_type = "sea"
            elif choice == '3' or choice == 'air':
                processor = Plane()
                transport_type = "air"
            elif choice == '4' or choice == 'china':
                processor = ChinaAdapter()
                transport_type = "china"
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
            
            service = LogisticsService(self.repository, processor, self.promo_repository)
            
            service.events.subscribe(self.driver_listener)
            service.events.subscribe(self.manager_listener)
            service.events.subscribe(self.log_listener)
            
            original_price = service.calculate_price(distance, weight, is_express)
            final_price = original_price
            
            
            promo_choice = input("\nХотите применить промокод? (y/n): ").lower()
            promo_code = None
            discount_amount = 0
            
            if promo_choice == 'y':
                promo_code_input = input("Введите промокод: ").strip().upper()
                
                if promo_code_input:
                    success, message, discounted_price = service.apply_promo_code(promo_code_input, original_price)
                    print(message)
                    
                    if success:
                        discount_amount = original_price - discounted_price
                        final_price = discounted_price
                        promo_code = promo_code_input
            
            print(f"\n{'='*50}")
            print("РАСЧЕТ СТОИМОСТИ")
            print(f"Маршрут: {from_city} -> {to_city}")
            print(f"Расстояние: {distance} км")
            print(f"Вес: {weight} кг")
            print(f"Тип доставки: {'Экспресс' if is_express else 'Стандарт'}")
            print(f"Исходная стоимость: {original_price:.2f} руб.")
            
            if discount_amount > 0:
                print(f"Скидка: -{discount_amount:.2f} руб.")
                print(f"Промокод: {promo_code}")
            
            print(f"ИТОГОВАЯ стоимость: {final_price:.2f} руб.")
            print(f"{'='*50}")
            
            ans = input("\nОформить заказ? (y/n): ").lower()
            if ans == 'n':
                print("Операция отменена.")
                service.clear_promo_code()
                continue
            
            comment = input("Оставьте комментарий к заказу: ")
            service.confirm_order(
                transport_type, from_city, to_city, distance, weight, 
                original_price, final_price, discount_amount, promo_code, 
                is_express, comment
            )
            
            another = input("\nОформить еще один заказ? (y/n): ").lower()
            if another != 'y':
                print("Спасибо за использование Logistics Corp! До свидания.")
                break