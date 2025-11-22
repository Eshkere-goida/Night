from strategies.interfaces.IPaymentProcessor import IPaymentProcessor

class PayPalProcessor(IPaymentProcessor):
    def pay(self,amount):
        email = input("Введите ваш email: ")
        if '@' not in email:
            print("Неверный email!")
            return False
        else:
            print(f"Списано {amount+amount*0.05} рубля, из них коммисия {amount*0.05} руб")
            return True