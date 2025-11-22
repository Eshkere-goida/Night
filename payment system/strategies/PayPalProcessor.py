from strategies.interfaces.IPaymentProcessor import IPaymentProcessor

class PayPalProcessor(IPaymentProcessor):
    def pay(self, amount):
        email = input("Введите ваш email: ")
        if '@' not in email:
            print("Неверный email!")
            return False
        else:
            commission = amount * 0.05
            total = amount + commission
            print(f"Списано {total} рубля, из них комиссия {commission} руб")
            return True