from repositories.MySQLTransactionRepository import MySQLTransactionRepository
from services.PaymentService import PaymentService
from strategies.CreditCardProcessor import CreditCardProcessor
from strategies.PayPalProcessor import PayPalProcessor
from strategies.CryptoProcessor import CryptoProcessor

class PaymentController:
    def __init__(self):
       
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin', 
            'database': 'payment_system'
        }
        self.repository = MySQLTransactionRepository(**self.db_config)
    
    def show_menu(self):
        print("\n=== Платежная система ===")
        print("1. Карта")
        print("2. PayPal")
        print("3. Криптовалюта")
        print("0. Выход")
    
    def get_amount(self):
        try:
            amount = float(input("Введите сумму платежа: "))
            return amount
        except ValueError:
            print("Ошибка: Введите числовое значение!")
            return None
    
    def run(self):
        while True:
            self.show_menu()
            choice = input("Выберите способ оплаты: ")
            
            if choice == '0':
                print("До свидания!")
                break
            
            amount = self.get_amount()
            if amount is None:
                continue
            
            processor = None
            
            if choice == '1':
                processor = CreditCardProcessor()
            elif choice == '2':
                processor = PayPalProcessor()
            elif choice == '3':
                processor = CryptoProcessor()
            else:
                print("Неверный выбор! Попробуйте снова.")
                continue
            
    
            service = PaymentService(self.repository, processor)
            service.process_order(amount)
            
            input("\nНажмите Enter для продолжения...")