from strategies.interfaces.IPaymentProcessor import IPaymentProcessor

class CreditCardProcessor(IPaymentProcessor):
    def pay(self, amount):
        if amount > 5000:
            pin = input("Введите пин-код: ")
            if pin != '1111':
                print("Неверный пин-код")
                return False
            else:
                commission = amount * 0.02
                total = amount + commission
                print(f"Списано {total} рубля(крупный платеж), из них комиссия {commission} руб")
                return True
        else:
            commission = amount * 0.02
            total = amount + commission
            print(f"Списано {total} рубля, из них комиссия {commission} руб")
            return True