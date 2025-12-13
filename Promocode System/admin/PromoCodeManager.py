import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories.MySQLPromoCodeRepository import MySQLPromoCodeRepository
from domain.PromoCode import PercentagePromoCode, FixedAmountPromoCode
from datetime import datetime, timedelta

class PromoCodeManager:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin',
            'database': 'test'
        }
        self.repository = MySQLPromoCodeRepository(**self.db_config)
    
    def run(self):
        while True:
            print("МЕНЕДЖЕР ПРОМОКОДОВ")
           
            print("1. Создать промокод")
            print("2. Просмотреть все промокоды")
            print("3. Деактивировать промокод")
            print("4. Выход")
            
            choice = input("\nВыберите действие: ")
            
            if choice == '1':
                self.create_promo_code()
            elif choice == '2':
                self.view_promo_codes()
            elif choice == '3':
                self.deactivate_promo_code()
            elif choice == '4':
                print("Выход из менеджера промокодов...")
                break
            else:
                print("Неверный выбор!")
    
    def create_promo_code(self):
        print("\nСоздание нового промокода:")
        code = input("Код промокода: ").upper().strip()
        
        print("Тип скидки:")
        print("1. Процентная скидка")
        print("2. Фиксированная сумма")
        
        type_choice = input("Выберите тип (1/2): ")
        
        if type_choice == '1':
            try:
                percentage = float(input("Процент скидки (например, 10 для 10%): "))
                days_valid = int(input("Срок действия (в днях, 0 - без срока): "))
                
                valid_until = None
                if days_valid > 0:
                    valid_until = datetime.now() + timedelta(days=days_valid)
                
                promo = PercentagePromoCode(code, percentage, valid_until)
                self.repository.add_promo_code(promo)
                print(f"✅ Промокод {code} создан!")
                
            except ValueError:
                print("❌ Ошибка ввода числовых значений!")
        
        elif type_choice == '2':
            try:
                amount = float(input("Сумма скидки (руб.): "))
                min_order = float(input("Минимальная сумма заказа (руб., 0 - без ограничения): "))
                days_valid = int(input("Срок действия (в днях, 0 - без срока): "))
                
                valid_until = None
                if days_valid > 0:
                    valid_until = datetime.now() + timedelta(days=days_valid)
                
                promo = FixedAmountPromoCode(code, amount, valid_until, min_order)
                self.repository.add_promo_code(promo)
                print(f"✅ Промокод {code} создан!")
                
            except ValueError:
                print("❌ Ошибка ввода числовых значений!")
        else:
            print("❌ Неверный выбор!")
    
    def view_promo_codes(self):
        
        print("СПИСОК ПРОМОКОДОВ")
        
        
        try:
            self.repository.cursor.execute("""
                SELECT code, discount_type, discount_value, min_order_amount, 
                       valid_until, is_active, created_at 
                FROM promo_codes 
                ORDER BY created_at DESC
            """)
            
            promos = self.repository.cursor.fetchall()
            
            if not promos:
                print("Нет промокодов в базе данных")
                return
            
            for promo in promos:
                code, discount_type, value, min_order, valid_until, is_active, created_at = promo
                status = "✅ АКТИВЕН" if is_active else "❌ НЕАКТИВЕН"
                valid_info = f"до {valid_until.strftime('%d.%m.%Y')}" if valid_until else "без срока"
                
                if discount_type == 'percentage':
                    desc = f"Скидка {value}%"
                else:
                    desc = f"Скидка {value} руб. (мин. заказ: {min_order} руб.)"
                
                print(f"\nКод: {code}")
                print(f"  {desc}")
                print(f"  Статус: {status}")
                print(f"  Действует: {valid_info}")
                print(f"  Создан: {created_at.strftime('%d.%m.%Y %H:%M')}")
        
        except Exception as e:
            print(f"❌ Ошибка при получении промокодов: {e}")
    
    def deactivate_promo_code(self):
        code = input("\nВведите код промокода для деактивации: ").upper().strip()
        
        confirm = input(f"Вы уверены, что хотите деактивировать промокод {code}? (y/n): ").lower()
        if confirm == 'y':
            self.repository.deactivate_promo_code(code)
            print(f"✅ Промокод {code} деактивирован!")
        else:
            print("❌ Отменено")

if __name__ == "__main__":
    manager = PromoCodeManager()
    manager.run()